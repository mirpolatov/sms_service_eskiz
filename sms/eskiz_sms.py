import requests

ESKIZ_EMAIL = ""
ESKIZ_PASSWORD = ""
BASE_URL = "https://notify.eskiz.uz/api/"

class EskizSMS:
    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        url = f"{BASE_URL}auth/login"
        payload = {
            "email": ESKIZ_EMAIL,
            "password": ESKIZ_PASSWORD
        }
        response = requests.post(url, data=payload)
        data = response.json()
        token = data.get("data", {}).get("token", "")
        if not token:
            raise Exception("Failed to retrieve token from Eskiz: " + str(data))
        return token

    def send_sms(self, phone, message):
        url = f"{BASE_URL}message/sms/send"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {
            "mobile_phone": phone,
            "message": message,
            "from": "Eskiz.uz"
        }
        response = requests.post(url, headers=headers, data=payload)
        return response.json()
