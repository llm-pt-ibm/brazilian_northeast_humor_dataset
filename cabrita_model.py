from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig

class CabritaModel:

    def __init__(self):
        self.model_name = '22h/open-cabrita3b'
        self.model = self.create_model()
        self.tokenizer = self.create_tokenizer()

    def get_model_name(self):
        return self.model_name

    def create_model(self):

        base_model_config = BitsAndBytesConfig(
            load_in_4bit = True
        )

        cabrita_model = AutoModelForCausalLM.from_pretrained(self.model_name, quantization_config = base_model_config)
        cabrita_model = cabrita_model.eval()
        cabrita_model.to('cuda')

        return cabrita_model
    
    def create_tokenizer(self):
        cabrita_tokenizer = AutoTokenizer.from_pretrained('22h/open-cabrita3b', use_fast = False)

        return cabrita_tokenizer

    def generate_prompt(self, instruction, input=None):
        if input:
            return f"""Abaixo está uma instrução que descreve uma tarefa, juntamente com uma entrada que fornece mais contexto. Escreva uma resposta que complete adequadamente o pedido.

    ### Instrução:
    {instruction}

    ### Entrada:
    {input}

    ### Resposta:"""
        else:
            return f"""Abaixo está uma instrução que descreve uma tarefa. Escreva uma resposta que complete adequadamente o pedido.

    ### Instrução:
    {instruction}

    ### Resposta:"""
        
    def evaluate(self, instruction, input=None):
        
        generation_config = GenerationConfig(
        temperature=0.5,
        top_p=0.75,
        num_beams=2,
        do_sample=True)

        prompt = self.generate_prompt(instruction, input)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs['input_ids'].cuda()
        input_ids = input_ids.to('cuda')

        generation_output = self.model.generate(
            input_ids=input_ids,
            generation_config = generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens = 64
        )

        for s in generation_output.sequences:
            output = self.tokenizer.decode(s)
            return output.strip()