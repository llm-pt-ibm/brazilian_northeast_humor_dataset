from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, AutoConfig
import requests

class LLMInterface:
    def __init__(self, model_config):
        self.name = model_config["name"]
        self.type = model_config["type"]
        if self.type == "hf":
            config = AutoConfig.from_pretrained(model_config["model_name"])
            if config.architectures[0] in ["T5ForConditionalGeneration", "BartForConditionalGeneration"]:
                self.model = AutoModelForSeq2SeqLM.from_pretrained(model_config["model_name"])
            else:
                self.model = AutoModelForCausalLM.from_pretrained(model_config["model_name"])
            self.tokenizer = AutoTokenizer.from_pretrained(model_config["model_name"])
        elif self.type == "api":
            self.endpoint = model_config["endpoint"]
            self.api_key = model_config["api_key"]
    
    def generate(self, prompt, params):
        if self.type == "hf":
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=params.get("max_tokens", 256))
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        elif self.type == "api":
            headers = {"Authorization": f"Bearer {self.api_key}"}
            data = {"model": self.name, "messages": [{"role": "system", "content": prompt}], **params}
            response = requests.post(self.endpoint, headers=headers, json=data)
            return response.json()["choices"][0]["message"]["content"]
