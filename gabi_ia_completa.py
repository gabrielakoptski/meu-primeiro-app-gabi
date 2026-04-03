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

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        self.crisis_keywords = [
            'quero morrer', 'vou me matar', 'suicidio',
            'nao aguento mais', 'desistir de tudo'
        ]

    def check_crisis(self, message: str) -> Tuple[bool, List[str]]:
        message_lower = message.lower()
        detected = [kw for kw in self.crisis_keywords if kw in message_lower]
        return len(detected) > 0, detected

    def get_crisis_response(self) -> str:
        return """
⚠️ PROCURE AJUDA IMEDIATA ⚠️

📞 188 - CVV (24h)
📞 192 - SAMU

Você não está sozinho.
"""

    def get_response(self, message: str, user_name=None, user_id=None) -> Dict:

        is_crisis, _ = self.check_crisis(message)

        if is_crisis:
            return {
                "response": self.get_crisis_response(),
                "alert_level": "HIGH"
            }

        return {
            "response": f"💬 Você disse: {message}",
            "alert_level": "NORMAL"
        }

    def get_emergency_card(self) -> str:
        return """
🆘 EMERGÊNCIA

📞 188 - CVV  
📞 192 - SAMU  

Respire. Isso vai passar.
"""
