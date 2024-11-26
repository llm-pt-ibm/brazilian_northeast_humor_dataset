from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, GenerationConfig

class BodeModel:

    def __init__(self):
        self.model_name = "recogna-nlp/bode-7b-alpaca-pt-br"
        self.config = PeftConfig.from_pretrained(self.model_name)
        self.model = self.create_model()
        self.tokenizer = self.create_tokenizer()

    def get_model_name(self):
        return self.model_name

    def create_model(self):

        base_model_config = BitsAndBytesConfig(
            load_in_4bit = True
        )

        base_model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-2-7b-chat-hf",
            quantization_config = base_model_config
        )

        bode_model = PeftModel.from_pretrained(base_model, self.model_name)
        bode_model.to('cuda')
        bode_model = bode_model.eval()

        return bode_model
    
    def create_tokenizer(self):
        bode_tokenizer = AutoTokenizer.from_pretrained(self.config.base_model_name_or_path)

        return bode_tokenizer

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
        input_ids = inputs["input_ids"].cuda()
        input_ids = input_ids.to('cuda')

        generation_output = self.model.generate(
            input_ids=input_ids,
            generation_config = generation_config,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens = 100
        )

        final_output = ''
        for s in generation_output.sequences:
            final_output += ' ' + self.tokenizer.decode(s).strip()
        
        return final_output.split('### Resposta:')[1].strip()