class PromptManager:
    @staticmethod
    def generate_prompt(column_name, row):
        if column_name == "punchlines":
            return (
                f"Texto humorístico: {row['corrected_transcription']}\n"
                f"Identifique os punchlines (explicação: {PromptManager.get_punchline_definition()})."
            )
        elif column_name in ["funny", "humor", "nonsense", "wit", "irony", "satire", "sarcasm", "cynicism"]:
            return (
                f"Texto humorístico: {row['corrected_transcription']}\n"
                f"O texto contém o estilo cômico '{column_name}'? Explique com base na seguinte definição: {PromptManager.get_style_definition(column_name)}"
            )
        elif column_name == "joke_explanation":
            return (
                f"Texto humorístico: {row['corrected_transcription']}\n"
                f"Explique o que torna a piada engraçada."
            )
    
    @staticmethod
    def get_punchline_definition():
        return (
            "Punchline é o elemento chave do humor em piadas, que provoca uma mudança abrupta de significado ou perspectiva, "
            "resultando na resolução de uma incongruência estabelecida anteriormente no texto."
        )
    
    @staticmethod
    def get_style_definition(style):
        style_definitions = {
            "funny": "A definição completa de 'funny' vai aqui.",
            # Adicione as demais definições conforme necessário
        }
        return style_definitions.get(style, "Definição não encontrada.")
