import yaml
import openai
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class ModelRunner:
    def __init__(self, config_path):
        self.models = self._load_config(config_path)

    def _load_config(self, path):
        with open(path, 'r') as file:
            config = yaml.safe_load(file)
        return config["models"]

    def run_prompt(self, model_name, prompt, parameters):
        model_config = next((m for m in self.models if m["name"] == model_name), None)
        if not model_config:
            raise ValueError(f"Modelo {model_name} não encontrado.")

        if model_config["type"] == "api":
            return self._run_api(model_config, prompt, parameters)
        elif model_config["type"] == "local":
            return self._run_local(model_config, prompt, parameters)
        else:
            raise ValueError(f"Tipo de modelo {model_config['type']} inválido.")

    def _run_api(self, model_config, prompt, parameters):
        if model_config["provider"] == "OpenAI":
            openai.api_key = model_config["api_key"]
            response = openai.Completion.create(
                engine=model_config["name"],
                prompt=prompt,
                **parameters
            )
            return response["choices"][0]["text"].strip()
        else:
            raise NotImplementedError("Somente OpenAI API é suportado no momento.")

    def _run_local(self, model_config, prompt, parameters):
        tokenizer = AutoTokenizer.from_pretrained(model_config["model_path"])
        model = AutoModelForCausalLM.from_pretrained(model_config["model_path"])
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=parameters["max_tokens"], temperature=parameters["temperature"])
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
