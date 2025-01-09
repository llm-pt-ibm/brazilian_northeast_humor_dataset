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
            "funny": "Diversão. A diversão (brincadeira) tem como objetivo espalhar o bom humor e o bom companheirismo. Pessoas que usam esse estilo cômico são consideradas sociais, joviais e também agradáveis. Em situações da vida cotidiana, eles usam provocações (travessuras) com amigos e pessoas acostumadas com assuntos obscenos. Eles podem se considerar brincalhões engraçados e gostar de fazer piadas maliciosas. Eles pregam peças inofensivas nos amigos e gostam de brincar e agir como palhaços.",
            "humor": "Humor. O humor (também conhecido como humor benevolente) visa despertar simpatia e compreensão para as incongruências da vida, as imperfeições do mundo, as deficiências dos semelhantes e os próprios contratempos e erros. Pessoas com humor são observadores realistas das fraquezas humanas, mas tratam-nas com benevolência, muitas vezes incluindo-se a si mesmas no julgamento, em vez de direcioná-lo exclusivamente aos outros. Há compreensão da humanidade em todas as fragilidades, que são observadas e compartilhadas com um público jovial, descontraído e contemplativo. O humor vem “do coração” e reflete uma atitude tolerante e amorosa para com os outros, que inclui a aceitação das suas deficiências. Uma pessoa com humor nesse sentido sabe que, tanto em grande como em pequena escala, o mundo não é perfeito. Ainda assim, com uma visão humorística do mundo, até mesmo as adversidades da vida podem ser divertidas e motivo de sorrisos. Quem utiliza esse estilo cômico consegue despertar compreensão e simpatia pelas imperfeições e pela condição humana por meio do humor.",
            "nonsense": "Nonsense / Absurdo. O absurdo, enquanto diversão intelectual, lúdica e alegre, visa expor o ridículo do puro sentido, embora basicamente sem qualquer propósito. Pessoas que gostam de bobagens se descrevem como brincalhonas e alegres. Eles deixam a mente brincar, por exemplo, sendo criativos com a linguagem e brincando com o sentido e o absurdo. Para eles, as incongruências não precisam ser resolvidas, mas o oposto é verdadeiro; isto é, quanto mais absurdo e mais engraçado. Eles criam um mundo de cabeça para baixo, usam a linguagem em suas imperfeições e acham divertidas histórias bizarras e fantásticas.",
            "wit": "Engenhosidade / Espirituosidade / Sagacidade. A sagacidade pretende iluminar como uma lanterna, normalmente com uma piada surpreendente que usa combinações incomuns criadas na hora. Uma pessoa que usa a inteligência brinca com palavras e pensamentos, e pode ser insensível, maliciosa e geralmente sem simpatia pelas “vítimas”, a fim de maximizar o impacto engraçado. Produzir inteligência requer habilidades: envolve ler situações rapidamente e abordar assuntos não óbvios de uma forma engraçada. Eles surpreendem os outros com comentários engraçados e julgamentos precisos sobre questões atuais, que lhes ocorrem espontaneamente. Eles estabelecem relações entre ideias ou pensamentos desconexos e, assim, criam um efeito cômico de forma rápida e incisiva. Pessoas espirituosas podem ser tensas, vaidosas, levar-se a sério e procurar uma sociedade educada que aprecie declarações breves e diretas como um público ideal.",
            "irony": "Ironia. A ironia, conforme expressa nas interações, visa criar um sentimento mútuo de superioridade em relação aos outros, dizendo as coisas de maneira diferente do que elas querem dizer. Não implica mentir, pois pressupõe-se que as pessoas inteligentes compreenderão o que realmente se quis dizer, independentemente do que foi dito. Pessoas irônicas estão cortejando e deixando entrar os inteligentes, ao mesmo tempo em que zombam dos estúpidos. A ironia é um meio de confundir os não-insiders e descobrir quem é um insider bem informado. Outros podem vê-los como presunçosos, superiores e frequentemente críticos negativos.",
            "satire": "Sátira. A sátira (ou humor corretivo) compartilha com o sarcasmo e o cinismo a detecção de fraquezas e é agressivo. No entanto, isso está associado a tentativas de bondade. Isto envolve não apenas depreciar os maus e tolos, mas também a intenção de melhorar o mundo e corrigir os semelhantes. Um satírico toma o mundo ético como uma medida do mundo real e tenta melhorar as condições revelando as verdadeiras circunstâncias. O satírico é crítico, muitas vezes negativo, tenso e superior, mas prefere que o mundo seja moral e usa o ridículo para melhorá-lo. Embora a tendência agressiva seja o elemento comum, a zombaria não é feita com base no puro prazer, mas está alicerçada numa crítica de base moral. Pessoas com mentalidade crítica normalmente aprovam a sátira. A bondade da sátira apela à mudança de comportamentos ou mentalidades inadequadas sem prejudicar seriamente as relações interpessoais.",
            "sarcasm": "Sarcasmo. O sarcasmo visa ferir os outros. A pessoa sarcástica é descrita, entre outros, como sendo hostil e zombeteira e como alguém que usa a exposição implacável para destacar o mundo corrupto. O público ideal consiste em pessoas subordinadas e dependentes. Pessoas com pontuação alta se considerariam malignas e críticas ao condenar a corrupção, a depravação, o vício ou o mal. Eles são propensos ao desprezo e à mágoa.",
            "cynicism": "Cinismo. O cinismo visa desvalorizar valores comumente reconhecidos. Os cínicos exibem uma atitude negativa e destrutiva. Eles usam a desilusão e a zombaria para destacar as fraquezas do mundo. Os cínicos não carecem de valores morais em geral, mas desprezam certas normas e conceitos morais comuns e os consideram ridículos."
        }
        return style_definitions.get(style, "Definição não encontrada.")
