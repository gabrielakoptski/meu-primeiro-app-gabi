class GabiIA:
    def get_response(self, message, user_name=None, user_id=None):
        return {
            "response": f"Você disse: {message}",
            "alert_level": "NORMAL"
        }
