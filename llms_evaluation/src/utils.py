import yaml

def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def log(message):
    print(f"[LOG] {message}")
