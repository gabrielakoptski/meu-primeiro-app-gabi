import json
from datetime import datetime
from typing import Dict, List, Tuple
import os
import random


class GabiIA:

    def __init__(self, data_dir: str = "gabi_data"):
        self.data_dir = data_dir
        self.user_name = None
        self.user_id = None
        self.conversation_history = []
        self.diary_entries = []

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.crisis_keywords = [
            'quero morrer', 'vou me matar', 'suicidio', 'suicida',
            'nao aguento mais', 'desistir de tudo', 'quero desaparecer'
        ]

        self.gabi_quotes = [
            "Você já sobreviveu a 100% dos seus dias difíceis até aqui.",
            "Um dia de cada vez.",
            "Você não é sua pior escolha. Você é sua decisão de mudar."
        ]

    def check_crisis(self, message: str) -> Tuple[bool, List[str]]:
        message_lower = message.lower()
        detected = [kw for kw in self.crisis_keywords if kw in message_lower]
        return len(detected) > 0, detected

    def get_crisis_response(self) -> str:
        return """
⚠️ **ESTOU PREOCUPADA COM VOCÊ**

📞 188 - CVV (24h, gratuito)
📞 192 - SAMU

Respire. Isso vai passar.
Você não está sozinho.
"""

    def get_emergency_card(self) -> str:
        return """
🆘 **EMERGÊNCIA**

📞 188 - CVV  
📞 192 - SAMU  

Respire. Isso vai passar.
"""

    def _get_random_quote(self) -> str:
        return random.choice(self.gabi_quotes)

    def get_response(self, message: str, user_name=None, user_id=None) -> Dict:

        if user_name:
            self.user_name = user_name

        is_crisis, _ = self.check_crisis(message)

        if is_crisis:
            return {
                "type": "crisis",
                "response": self.get_crisis_response(),
                "alert_level": "HIGH"
            }

        return {
            "type": "normal",
            "response": f"""
💚 Estou aqui com você.

Você disse: "{message}"

✨ {self._get_random_quote()}
""",
            "alert_level": "NORMAL"
        }


# =========================
# TESTE LOCAL (NÃO AFETA STREAMLIT)
# =========================

if __name__ == "__main__":
    gabi = GabiIA()

    test_cases = [
        ("João", "Oi"),
        ("Maria", "Estou com vontade de usar"),
        ("Pedro", "Quero desistir de tudo")
    ]

    for name, msg in test_cases:
        print(f'👤 {name}: "{msg}"')
        response = gabi.get_response(msg, name)
        print(response["response"])
        print("-" * 50)
