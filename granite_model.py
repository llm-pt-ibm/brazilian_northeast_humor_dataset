import os
from transformers import AutoModelForCausalLM, AutoTokenizer

class GraniteModel:

    def __init__(self):
        self.model_name = 'granite-3.0-1b-a400m-instruct'
        self.model_path = os.path.join(os.getcwd(), 'models', self.model_name)
        self.model = self.create_model()
        self.tokenizer = self.create_tokenizer()

    def get_model_name(self):
        return self.model_name

    def create_model(self):
        model = AutoModelForCausalLM.from_pretrained(self.model_path, device_map='auto')
        model = model.eval()

        return model
    
    def create_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_path)

        return tokenizer

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

    def evaluate(self, instruction, input = None):
        chat = [
            {"role": "user",
            "content": self.generate_prompt(instruction, input)}
        ]

        chat = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        input_tokens = self.tokenizer(chat, return_tensors="pt").to('cuda')
        output = self.model.generate(**input_tokens, max_new_tokens=150)
        output = self.tokenizer.batch_decode(output)

        return output[0].strip().split('<|start_of_role|>assistant<|end_of_role|>')[1].strip().strip('<|end_of_text|>').strip()