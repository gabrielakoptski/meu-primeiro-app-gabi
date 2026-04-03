"""
🕊️ GABI - IA de Apoio à Recuperação
Inspirada na história de Gabriella Bogo da Silva (@umaadictagabi)
3 anos limpa, conselheira de dependentes químicos e codependentes

Autor: [Seu Nome]
Data: 2026
Versão: 1.0

===========================================================
AVISO LEGAL E DE RESPONSABILIDADE
===========================================================

Esta IA é uma ferramenta de APOIO EMOCIONAL e NÃO substitui:
- Terapia profissional
- Tratamento médico especializado
- Grupos de apoio (AA, NA, Al-Anon, etc.)
- Atendimento de emergências psiquiátricas

Em caso de CRISE SUICIDA ou EMERGÊNCIA:
📞 Ligue 188 - CVV (Centro de Valorização da Vida) - 24h, gratuito
📞 Ligue 192 - SAMU

===========================================================
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
import os


class GabiIA:
    """
    Inteligência Artificial de apoio emocional para recuperação de 
    dependentes químicos e codependentes.

    Funcionalidades:
    - Detecção de crises e direcionamento emergencial
    - Técnicas de coping para craving, ansiedade e culpa
    - Suporte para codependentes
    - Diário de recuperação
    - Histórico de conversas
    """

    def __init__(self, data_dir: str = "gabi_data"):
        """
        Inicializa a Gabi IA.

        Args:
            data_dir: Diretório para salvar dados dos usuários
        """
        self.data_dir = data_dir
        self.user_name = None
        self.user_id = None
        self.conversation_history = []
        self.diary_entries = []

        # Cria diretório de dados se não existir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Palavras-chave de crise (detecção de risco suicida)
        self.crisis_keywords = [
            'quero morrer', 'vou me matar', 'suicidio', 'suicida', 'acabar com tudo',
            'nao aguento mais', 'desistir de tudo', 'nada faz sentido',
            'quero desaparecer', 'nao quero viver', 'machucar', 'me cortar',
            'me matar', 'morrer', 'acabar comigo', 'desistir da vida'
        ]

        # Recursos de emergência
        self.emergency_resources = {
            'cvv': {
                'numero': '188', 
                'nome': 'CVV - Centro de Valorização da Vida', 
                'descricao': 'Atendimento emocional 24h, gratuito e sigiloso',
                'site': 'www.cvv.org.br'
            },
            'samu': {
                'numero': '192', 
                'nome': 'SAMU', 
                'descricao': 'Emergências médicas'
            },
            'policia': {
                'numero': '190', 
                'nome': 'Polícia Militar', 
                'descricao': 'Emergências de segurança'
            },
            'bombeiros': {
                'numero': '193', 
                'nome': 'Corpo de Bombeiros', 
                'descricao': 'Emergências e resgates'
            },
            'caps': {
                'nome': 'CAPS', 
                'descricao': 'Centro de Atenção Psicossocial - procure o mais próximo'
            }
        }

        # Técnicas de recuperação organizadas por necessidade
        self.recovery_techniques = {
            'craving': {
                'titulo': 'Técnicas para Craving (Vontade Intensa de Usar)',
                'tecnicas': [
                    {
                        'nome': 'Respiração 4-7-8',
                        'descricao': 'Inspire por 4s, segure 7s, expire 8s. Repita 4 vezes.',
                        'duracao': '2 minutos'
                    },
                    {
                        'nome': 'Técnica do Gelo',
                        'descricao': 'Segure cubos de gelo nas mãos até derreter. Foco físico imediato.',
                        'duracao': '5 minutos'
                    },
                    {
                        'nome': 'Mudança de Ambiente',
                        'descricao': 'Saia do lugar imediatamente. Caminhe 10 minutos em outro lugar.',
                        'duracao': '10 minutos'
                    },
                    {
                        'nome': 'Ligação de Segurança',
                        'descricao': 'Ligue para alguém da sua rede de apoio AGORA. Não mande mensagem, ligue.',
                        'duracao': '15 minutos'
                    },
                    {
                        'nome': 'Regra dos 15 Minutos',
                        'descricao': 'O craving passa. Aguarde 15 minutos fazendo outra coisa e reavalie.',
                        'duracao': '15 minutos'
                    }
                ],
                'frase_gabi': 'O craving é só uma onda. Se eu surfar, passa. Se eu lutar, afundo.'
            },

            'ansiedade': {
                'titulo': 'Técnicas para Ansiedade e Pânico',
                'tecnicas': [
                    {
                        'nome': 'Técnica 5-4-3-2-1',
                        'descricao': 'Identifique: 5 coisas que vê, 4 que ouve, 3 que toca, 2 que cheira, 1 que prova',
                        'duracao': '3 minutos'
                    },
                    {
                        'nome': 'Grounding (Ancoragem)',
                        'descricao': 'Pés no chão. Sinta o contato com o solo. Você está aqui, agora, seguro.',
                        'duracao': '2 minutos'
                    },
                    {
                        'nome': 'Rotação de Olhos',
                        'descricao': 'Mova os olhos horizontalmente por 30 segundos (ativação bilateral)',
                        'duracao': '1 minuto'
                    },
                    {
                        'nome': 'Água Consciente',
                        'descricao': 'Beba um copo d'água lentamente. Foque na sensação de beber.',
                        'duracao': '3 minutos'
                    }
                ],
                'frase_gabi': 'Eu passava dias inteiros ansiosa achando que algo ruim ia acontecer. Quando percebi que estava só vivendo o medo, comecei a praticar voltar pro corpo, pro momento. Um minuto de cada vez.'
            },

            'culpa': {
                'titulo': 'Técnicas para Culpa e Vergonha',
                'tecnicas': [
                    {
                        'nome': 'Carta à Si Mesmo',
                        'descricao': 'Escreva como falaria com um amigo querido na mesma situação',
                        'duracao': '10 minutos'
                    },
                    {
                        'nome': 'Reframe de Perdão',
                        'descricao': 'Diga: "Fiz o melhor que podia com o que sabia na época. Hoje sei mais."',
                        'duracao': '2 minutos'
                    },
                    {
                        'nome': 'Foco no Presente',
                        'descricao': 'Ontem já foi. O que importa é o que você faz HOJE. Liste 3 ações positivas de hoje.',
                        'duracao': '5 minutos'
                    },
                    {
                        'nome': 'Compaixão Prática',
                        'descricao': 'Coloque a mão no coração. Sinta o batimento. Você está vivo. Há esperança.',
                        'duracao': '3 minutos'
                    }
                ],
                'frase_gabi': 'Você não é sua pior escolha. Você é sua decisão de mudar.'
            },

            'codependencia': {
                'titulo': 'Técnicas para Codependência',
                'tecnicas': [
                    {
                        'nome': 'Checklist de Limites',
                        'descricao': 'Antes de ajudar: Estou fazendo isso por mim ou por ele? Estou me sacrificando?',
                        'duracao': '2 minutos'
                    },
                    {
                        'nome': 'Frases de Limites',
                        'descricao': 'Pratique: "Eu te amo e não posso fazer isso por você" / "Preciso cuidar de mim"',
                        'duracao': '5 minutos'
                    },
                    {
                        'nome': 'Respiração de Liberação',
                        'descricao': 'Inspire a responsabilidade que é sua, expire a que é do outro',
                        'duracao': '5 minutos'
                    }
                ],
                'frase_gabi': 'Você não abandona quem ama quando estabelece limites. Você se salva para poder amar de verdade.'
            }
        }

        # Mensagens motivacionais da Gabriella
        self.gabi_quotes = [
            "Você já sobreviveu a 100% dos seus dias difíceis até aqui.",
            "A recuperação é feita de dias ruins que a gente sobreviveu mesmo assim.",
            "Não existe vencedor na dependência química, existe sobrevivente. E você está sobrevivendo.",
            "Um dia de cada vez. Às vezes, um minuto de cada vez.",
            "Você não é sua pior escolha. Você é sua decisão de mudar.",
            "A culpa quer que você fique pequeno. A recuperação quer que você cresça.",
            "O craving é só uma onda. Se eu surfar, passa. Se eu lutar, afundo.",
            "Codependência é amar até se perder. Recuperação é amar e se manter inteiro.",
            "Não existe recaída de graça. Cada uma ensina algo se você estiver disposto a aprender.",
            "Você importa. Sua recuperação importa. Você não está sozinho."
        ]

    def check_crisis(self, message: str) -> Tuple[bool, List[str]]:
        """
        Detecta sinais de crise suicida ou grave na mensagem.

        Args:
            message: Texto da mensagem do usuário

        Returns:
            Tuple[bool, List[str]]: (é_crise, lista_de_palavras_detectadas)
        """
        message_lower = message.lower()
        detected = [kw for kw in self.crisis_keywords if kw in message_lower]
        return len(detected) > 0, detected

    def get_crisis_response(self) -> str:
        """
        Gera resposta imediata para situações de crise.
        Prioriza segurança e direcionamento profissional.
        """
        return """
⚠️ **ESTOU PREOCUPADA COM VOCÊ** ⚠️

Percebi que você pode estar passando por um momento muito difícil.

**VOCÊ NÃO ESTÁ SOZINHO. NÃO ESTÁ SOZINHA.**

🆘 **LIGUE AGORA (gratuito, 24h, sigiloso):**
📞 **188** - CVV (Centro de Valorização da Vida)
📞 **192** - SAMU (se necessário)
📞 **190** - Polícia Militar

**Respire comigo agora:**
1. Inspire fundo... 2... 3... 4...
2. Segure... 2... 3... 4... 5... 6... 7...
3. Solte devagar... 2... 3... 4... 5... 6... 7... 8...

Você já sobreviveu a 100% dos seus dias difíceis até aqui.
Essa crise vai passar. **Não tome decisões permanentes em momentos temporários.**

Posso continuar conversando, mas por favor, ligue para o 188.
Eles são especialistas e vão te ouvir sem julgamento.

Você importa. Sua recuperação importa. 💚

---
*Se não puder ligar agora, continue conversando comigo, mas busque ajuda profissional assim que possível.*
        """

    def identify_intent(self, message: str) -> str:
        """
        Identifica a intenção/intensão emocional da mensagem.

        Args:
            message: Texto da mensagem

        Returns:
            String com a categoria identificada
        """
        message_lower = message.lower()

        # Dicionário de palavras-chave por intenção
        intents = {
            'craving': ['vontade', 'querer usar', 'craving', 'tentação', 'quero droga', 
                       'beber', 'usar', 'maconha', 'cocaína', 'pó', 'bebida', 'álcool',
                       'quero usar', 'vontade de', 'tentado', 'tentada'],
            'ansiedade': ['ansioso', 'ansiosa', 'nervoso', 'nervosa', 'agonia', 'pânico', 
                         'medo', 'angustia', 'angustiado', 'angustiada', 'apreensivo',
                         'preocupado', 'preocupada', 'aflição'],
            'culpa': ['culpa', 'culpado', 'culpada', 'vergonha', 'me odeio', 'estraguei', 
                     'ruim', 'inútil', 'merda', 'lixo', 'não mereço', 'errado', 'erro'],
            'greeting': ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 
                        'hey', 'e aí', 'eae', 'salve', 'hello'],
            'gratitude': ['gratidão', 'obrigado', 'obrigada', 'valeu', 'ajudou', 
                         'funcionou', 'melhorou', 'grato', 'grata', 'muito obrigado'],
            'codependencia': ['codependente', 'codependência', 'salvar', 'controlar', 
                             'limite', 'relacionamento', 'parceiro', 'parceira', 'marido', 
                             'esposa', 'namorado', 'namorada', 'familiar', 'mãe', 'pai'],
            'diary': ['diário', 'diario', 'registrar', 'hoje eu', 'meu dia', 'check-in', 'checkin']
        }

        # Verifica cada intenção
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent

        return 'general'

    def get_response(self, message: str, user_name: str = None, user_id: str = None) -> Dict:
        """
        Processa mensagem e gera resposta completa.

        Args:
            message: Texto do usuário
            user_name: Nome do usuário (opcional)
            user_id: ID único do usuário (opcional)

        Returns:
            Dict com resposta completa e metadados
        """
        # Atualiza informações do usuário
        if user_name:
            self.user_name = user_name
        if user_id:
            self.user_id = user_id
            self._load_user_data(user_id)

        # VERIFICAÇÃO DE CRISE (PRIORIDADE MÁXIMA)
        is_crisis, crisis_words = self.check_crisis(message)
        if is_crisis:
            response_data = {
                'type': 'crisis',
                'response': self.get_crisis_response(),
                'timestamp': datetime.now().isoformat(),
                'alert_level': 'HIGH',
                'crisis_words_detected': crisis_words,
                'disclaimer': 'ATENÇÃO: Esta mensagem indica possível risco de suicídio. Direcionamento emergencial ativado.'
            }
            self._save_conversation(message, response_data)
            return response_data

        # Identifica intenção e gera resposta
        intent = self.identify_intent(message)
        response_text = self._generate_response(intent, message)

        response_data = {
            'type': intent,
            'response': response_text,
            'timestamp': datetime.now().isoformat(),
            'alert_level': 'NORMAL',
            'techniques_suggested': self._get_techniques(intent),
            'quote_of_moment': self._get_random_quote(),
            'disclaimer': 'Esta IA é ferramenta de apoio e não substitui tratamento profissional.'
        }

        # Salva conversa
        self._save_conversation(message, response_data)

        return response_data

    def _generate_response(self, intent: str, original_message: str) -> str:
        """Gera resposta baseada na intenção identificada."""

        responses = {
            'greeting': self._greeting_response(),
            'craving': self._craving_response(),
            'ansiedade': self._ansiedade_response(),
            'culpa': self._culpa_response(),
            'gratitude': self._gratitude_response(),
            'codependencia': self._codependencia_response(),
            'diary': self._diary_response(),
            'general': self._general_response()
        }

        return responses.get(intent, self._general_response())

    def _greeting_response(self) -> str:
        """Resposta de saudação inicial."""
        name = f", {self.user_name}" if self.user_name else ""
        return f"""
🕊️ **Olá{name}! Sou a Gabi, sua companheira de recuperação.**

Sou inspirada na história da **Gabriella Bogo da Silva** (@umaadictagabi) - 3 anos limpa, conselheira de dependentes químicos e codependentes, e prova viva de que é possível recomeçar.

**Como posso te apoiar hoje?**

💚 Se estiver com vontade de usar (craving)
🧘 Se estiver ansioso ou em pânico  
😔 Se estiver se sentindo culpado ou envergonhado
👥 Se precisar falar sobre codependência
📝 Se quiser fazer check-in do seu dia

**Lembre-se importante:**
Sou uma ferramenta de apoio emocional. **Não substituo terapia, tratamento médico ou grupos de apoio.**

🆘 Em crise, ligue **188** (CVV) - 24h, gratuito, sigiloso.

Como posso te chamar? Qual seu nome?
        """

    def _craving_response(self) -> str:
        """Resposta para momentos de craving/vontade de usar."""
        tecnicas = self.recovery_techniques['craving']

        tecnicas_texto = "\n".join([
            f"**{i+1}. {t['nome']}** ({t['duracao']})\n   {t['descricao']}"
            for i, t in enumerate(tecnicas['tecnicas'])
        ])

        return f"""
💚 **EU TE ENTENDO. E ESSA VONTADE VAI PASSAR.**

A Gabriella já passou por isso muitas vezes nos 3 anos de recuperação. Ela diz: 

> *"{tecnicas['frase_gabi']}"*

**TÉCNICAS IMEDIATAS (escolha UMA e faça AGORA):**

{tecnicas_texto}

**🔴 REGRA DE OURO:**
Não tome decisões quando a vontade está no auge. Espere 15 minutos. Reavalie.

**Você quer contar o que despertou essa vontade?** Às vezes, identificar o gatilho já ajuda a diminuí-lo.

Lembre-se: cada craving que você sobrevive fortalece sua recuperação. 💪
        """

    def _ansiedade_response(self) -> str:
        """Resposta para ansiedade e pânico."""
        tecnicas = self.recovery_techniques['ansiedade']

        tecnicas_texto = "\n".join([
            f"**{i+1}. {t['nome']}** ({t['duracao']})\n   {t['descricao']}"
            for i, t in enumerate(tecnicas['tecnicas'])
        ])

        return f"""
🧘 **RESPIRA. VOCÊ ESTÁ SEGURO AGORA.**

A ansiedade é o medo do futuro. Vamos trazer você de volta para o presente:

**TÉCNICAS DE GROUNDING (Ancoragem):**

{tecnicas_texto}

**💬 LEMBRETE DA GABI:**
> *"{tecnicas['frase_gabi']}"*

**Exercício rápido - Descreva para mim:**
Qual sensação física você está sentindo agora? (ex: "coração acelerado", "tensão no peito", "mãos suadas")

Só nomear o que sente já ajuda o cérebro a processar. Você está seguro aqui. 🌿
        """

    def _culpa_response(self) -> str:
        """Resposta para culpa e vergonha."""
        tecnicas = self.recovery_techniques['culpa']

        tecnicas_texto = "\n".join([
            f"**{i+1}. {t['nome']}** ({t['duracao']})\n   {t['descricao']}"
            for i, t in enumerate(tecnicas['tecnicas'])
        ])

        return f"""
💚 **VOCÊ MERECE COMPAIXÃO, NÃO PUNIÇÃO.**

A culpa na recuperação é normal, mas ela pode nos paralisar. A Gabriella fala muito sobre isso:

**PARA TRANSFORMAR A CULPA EM Crescimento:**

{tecnicas_texto}

**🔄 REFRAME (Mudança de Perspectiva):**
❌ "Eu fiz coisas ruins" 
✅ "Eu fiz coisas ruins E estou me esforçando para ser diferente"

**💬 LEMBRETE DA GABI:**
> *"{tecnicas['frase_gabi']}"*

**A culpa quer que você fique pequeno. A recuperação quer que você cresça.**

O que você aprendeu com o que aconteceu? Como isso pode te fortalecer hoje?
        """

    def _codependencia_response(self) -> str:
        """Resposta para questões de codependência."""
        tecnicas = self.recovery_techniques['codependencia']

        tecnicas_texto = "\n".join([
            f"**{i+1}. {t['nome']}** ({t['duracao']})\n   {t['descricao']}"
            for i, t in enumerate(tecnicas['tecnicas'])
        ])

        return f"""
👥 **CODEPENDÊNCIA: AMAR SEM SE PERDER**

A Gabriella ajuda tanto dependentes quanto codependentes. Ela sabe que codependência também é vício - vício em salvar, controlar, agradar, se sacrificar.

**🚨 SINAIS DE CODEPENDÊNCIA:**
• Sua paz depende do comportamento do outro
• Você diz "sim" quando quer dizer "não"
• Se sacrifica e depois se ressente
• Confunde amar com salvar
• Sente culpa se não resolve problema do outro

**TÉCNICAS:**

{tecnicas_texto}

**💬 LEMBRETE DA GABI:**
> *"{tecnicas['frase_gabi']}"*

**FRASES PARA PRATICAR:**
• "Eu te amo e não posso fazer isso por você"
• "Não concordo, mas respeito sua escolha"
• "Preciso cuidar de mim agora"
• "Não sou responsável pela sua felicidade"

Está difícil estabelecer limite com alguém específico? Me conte. 💙
        """

    def _gratitude_response(self) -> str:
        """Resposta para mensagens de gratidão."""
        return """
🙏 **GRATIDÃO! VOCÊ FORTALECE MINHA MISSÃO.**

Cada mensagem como a sua me lembra por que existo: para ser ponte no momento difícil, para lembrar que ninguém precisa passar por isso sozinho.

A Gabriella sempre diz: 
> *"A recuperação é feita de dias ruins que a gente sobreviveu mesmo assim."*

**Você está fazendo o trabalho. Eu só dou ferramentas. A força é toda sua.** 💚

Volte quando precisar. Estarei aqui, 24h por dia.

E se estiver bem agora, aproveite para fazer algo que te nutre. Você merece.
        """

    def _diary_response(self) -> str:
        """Resposta para solicitação de diário/check-in."""
        return self.get_daily_checkin()

    def _general_response(self) -> str:
        """Resposta genérica quando não identifica intenção específica."""
        return """
💚 **ESTOU AQUI COM VOCÊ.**

Pode me contar mais sobre o que está sentindo? Quanto mais eu entender, melhor posso te direcionar.

**Posso ajudar com:**
• 🌊 Crises de vontade (craving)
• 🧘 Ansiedade e pânico
• 😔 Culpa e vergonha
• 👥 Relacionamentos codependentes
• 📝 Diário de recuperação
• 💬 Simplesmente ouvir

**Ou, se preferir, me conte:**
Como está sua recuperação hoje, de 0 a 10?
(0 = crise total, 10 = tranquilo)

Estou aqui. Sem julgamento. 💙
        """

    def _get_techniques(self, intent: str) -> List[Dict]:
        """Retorna lista de técnicas para a intenção específica."""
        if intent in self.recovery_techniques:
            return self.recovery_techniques[intent]['tecnicas']
        return []

    def _get_random_quote(self) -> str:
        """Retorna uma frase motivacional aleatória da Gabriella."""
        import random
        return random.choice(self.gabi_quotes)

    def get_daily_checkin(self) -> str:
        """
        Gera template de check-in diário para o diário de recuperação.
        """
        return """
📓 **CHECK-IN DIÁRIO - Recuperação**
Data: {data}

**1. Como você está se sentindo hoje? (0-10)**
_0 = crise total | 5 = neutro | 10 = tranquilo_
Resposta: ___

**2. O que foi mais desafiador hoje?**
_________________________________

**3. O que você fez pela sua recuperação hoje?**
(Ex: reunião, leitura, terapia, exercício, descanso)
_________________________________

**4. Uma coisa que te gratificou ou deu esperança:**
_________________________________

**5. Precisa de alguma técnica agora?**
[ ] Respiração para ansiedade
[ ] Técnicas para craving
[ ] Aliviar culpa
[ ] Codependência/limites
[ ] Apenas conversar

**6. Uma afirmação para hoje:**
"_________________________________"

---
💾 *Seu registro fica salvo e ajuda a identificar padrões.*
🤖 *Quer que eu analise seu check-in? Me mande preenchido.*
        """.format(data=datetime.now().strftime("%d/%m/%Y"))

    def analyze_checkin(self, checkin_data: Dict) -> str:
        """
        Analisa dados do check-in e retorna insights.

        Args:
            checkin_data: Dicionário com respostas do check-in

        Returns:
            Análise e sugestões personalizadas
        """
        mood = checkin_data.get('mood', 5)
        challenges = checkin_data.get('challenges', '')
        actions = checkin_data.get('actions', '')

        analysis = []

        # Análise de humor
        if mood <= 3:
            analysis.append("🔴 **Alerta de bem-estar:** Seu humor está baixo. Priorize autocuidado hoje.")
            analysis.append("💡 Sugestão: Use a técnica de grounding e considere ligar para alguém de confiança.")
        elif mood <= 6:
            analysis.append("🟡 **Dia neutro:** Normal na recuperação. Foque em uma pequena vitória hoje.")
        else:
            analysis.append("🟢 **Dia positivo:** Ótimo! Registre o que funcionou para replicar.")

        # Análise de desafios
        if 'craving' in challenges.lower() or 'vontade' in challenges.lower():
            analysis.append("🌊 Craving detectado nos desafios. Você sobreviveu! Isso fortalece.")

        if any(word in challenges.lower() for word in ['relacionamento', 'parceiro', 'família', 'mãe', 'pai']):
            analysis.append("👥 Desafio relacionado a relacionamentos. Codependência pode estar atuando.")

        # Análise de ações
        if not actions or actions.strip() == '':
            analysis.append("⚠️ Nenhuma ação de recuperação registrada. Que tal uma pequena ação hoje?")
        else:
            analysis.append(f"✅ Você praticou: {actions}. Continue!")

        return "\n".join(analysis)

    def get_emergency_card(self) -> str:
        """
        Gera cartão de emergência para salvar no celular.
        """
        return """
╔══════════════════════════════════════════════════════════════╗
║                    🆘 CARTÃO DE EMERGÊNCIA                    ║
║                 SALVE NO SEU CELULAR AGORA                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  EM CRISE, LIGUE IMEDIATAMENTE:                               ║
║  📞 188 - CVV (24h, gratuito, sigiloso)                       ║
║  📞 192 - SAMU (emergência médica)                            ║
║  📞 190 - Polícia Militar                                     ║
║  📞 193 - Corpo de Bombeiros                                  ║
║                                                               ║
║  TÉCNICA RÁPIDA DE RESPIRAÇÃO:                                ║
║  Inspire 4s → Segure 7s → Expire 8s (repita 4x)              ║
║                                                               ║
║  ═══════════════════════════════════════════════════════════ ║
║                                                               ║
║  CONTATOS DE APOIO (preencha):                                ║
║  Padrinho/Madrinha: _________________________                   ║
║  Terapeuta: ________________________________                   ║
║  Grupo de Apoio: ___________________________                   ║
║  Familiar de confiança: ____________________                   ║
║                                                               ║
║  ═══════════════════════════════════════════════════════════ ║
║                                                               ║
║  LEMBRETE DA GABI:                                            ║
║  "Você já sobreviveu a 100% dos seus piores dias.            ║
║   Essa crise também vai passar. Não desista."                ║
║                                                               ║
║  Instagram: @umaadictagabi                                    ║
║  GABI - IA de Apoio à Recuperação                             ║
╚══════════════════════════════════════════════════════════════╝
        """

    def get_resources_guide(self) -> str:
        """
        Guia completo de recursos para recuperação.
        """
        return """
📚 **GUIA DE RECURSOS PARA RECUPERAÇÃO**

**GRUPOS DE APOIO (encontros presenciais e online):**
• AA (Alcoólicos Anônimos) - www.aa.org.br
• NA (Narcóticos Anônimos) - www.na.org.br  
• Al-Anon (para familiares) - www.al-anon.org.br
• CA (Cocaínicos Anônimos)

**ATENDIMENTO PROFISSIONAL:**
• CAPS (Centro de Atenção Psicossocial) - gratuito, SUS
• CRAs (Centros de Referência em Álcool e Drogas)
• Psicólogos e psiquiatras especializados em dependência

**APOIO EMOCIONAL IMEDIATO:**
• CVV - 188 (24h, gratuito, sigiloso)
• Chat CVV: www.cvv.org.br

**APPS DE APOIO:**
• #Sobriety (contador de dias clean)
• I am Sober (comunidade de recuperação)
• Calm/Medito (meditação para ansiedade)

**INSTAGRAMS EDUCATIVOS:**
• @umaadictagabi (Gabriella Bogo - conselheira)
• @institutouniad (pesquisa e tratamento)
• @organizacoesintegracao (reintegração social)

**LEITURAS RECOMENDADAS:**
• "Não Tenho Sapatos Fechados" - Gabriela Manssur
• "O Mundo de Sofia" - Jostein Gaarder (para reflexão)
• "12 Passos e 12 Tradições" - AA/NA

**LEMBRETE:**
Você não precisa fazer isso sozinho. Peça ajuda. 💚
        """

    # Métodos privados de persistência
    def _save_conversation(self, user_msg: str, response_data: Dict):
        """Salva conversa no histórico."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_msg,
            'gabi_response': response_data,
            'alert_level': response_data.get('alert_level', 'NORMAL')
        })

        # Salva em arquivo se tiver user_id
        if self.user_id:
            self._persist_data()

    def _load_user_data(self, user_id: str):
        """Carrega dados históricos do usuário."""
        filepath = os.path.join(self.data_dir, f"{user_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversation_history = data.get('conversations', [])
                self.diary_entries = data.get('diary', [])
                self.user_name = data.get('user_name', None)

    def _persist_data(self):
        """Persiste dados em arquivo JSON."""
        if not self.user_id:
            return

        filepath = os.path.join(self.data_dir, f"{self.user_id}.json")
        data = {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'last_updated': datetime.now().isoformat(),
            'conversations': self.conversation_history,
            'diary': self.diary_entries
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_diary_entry(self, entry: Dict):
        """Adiciona entrada ao diário."""
        entry['timestamp'] = datetime.now().isoformat()
        self.diary_entries.append(entry)
        if self.user_id:
            self._persist_data()


# ============================================================
# EXEMPLO DE USO E TESTES
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🕊️  GABI - IA de Apoio à Recuperação")
    print("Inspirada em Gabriella Bogo da Silva (@umaadictagabi)")
    print("=" * 70)
    print()

    # Inicializa a IA
    gabi = GabiIA()

    # Demonstração de interações
    print("💬 DEMONSTRAÇÃO DE INTERAÇÕES:\n")

    test_cases = [
        ("João", "Oi, tudo bem?"),
        ("Maria", "Estou com muita vontade de usar droga"),
        ("Pedro", "Não aguento mais, quero desistir de tudo"),
        ("Ana", "Me sinto culpada pelo que fiz no passado"),
        ("Carlos", "Minha esposa não para de beber e eu não consigo ajudar"),
        ("Julia", "Obrigada, me ajudou muito a passar pelo craving"),
        ("Lucas", "Quero fazer meu check-in de hoje")
    ]

    for name, msg in test_cases:
        print(f'👤 {name}: "{msg}"')
        print("-" * 50)

        response = gabi.get_response(msg, name, f"user_{name.lower()}")

        if response['alert_level'] == 'HIGH':
            print("🔴 ALERTA DE CRISE DETECTADO - Intervenção emergencial ativada")
            print()

        print(response['response'])
        print()
        print("=" * 70)
        print()

    # Mostra recursos adicionais
    print(gabi.get_emergency_card())
    print()
    print(gabi.get_resources_guide())
