import requests
import time
import base64
from PIL import Image
from io import BytesIO

class hCaptchaToken:
    def __init__(self, apikey_file):
        self.apikey_file = apikey_file
        self.token_api = "https://token.nocaptchaai.com/token"
        self.headers = {"Content-Type": "application/json",
                        "apikey": None}
        self.token = None  # Initialize token attribute
        self.solved = False  # Initialize solved attribute

    def read_api_key(self):
        with open(self.apikey_file, "r") as file:
            return file.read().strip()

    def solve(self, payload):
        self.headers["apikey"] = self.read_api_key()
        response = requests.post(
            self.token_api, json=payload, headers=self.headers)
        response_json = response.json()
        startTime = time.time()

        print("task status: ", response_json)
        print("waiting 7sec for response...")
        time.sleep(7)

        while True:
            sts = requests.get(
                response_json["url"], headers=self.headers).json()
            if sts["status"] == "processed" or sts["status"] == "failed":
                print(
                    f'time since request:- {int(time.time() - startTime)} seconds')
                print(f'status: {sts["status"]}\n{sts["token"]}')
                self.token = sts["token"]
                if sts["status"] == "processed":
                    with open("test.txt", "w") as file:
                        file.write(sts["token"])
                    self.solved = True
                break

            print(f"{sts}")
            print("status: ", sts["status"])
            time.sleep(2)

class OCR:
    def __init__(self, apikey_file):
        self.apikey = self.read_api_key(apikey_file)
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.apikey
        }

    def read_api_key(self, apikey_file):
        with open(apikey_file, "r") as file:
            return file.read().strip()

    def image_to_base64(self, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        return base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    def solve(self, image_url):
        payload = {
            "method": "ocr",
            "image": self.image_to_base64(image_url)
        }

        try:
            response = requests.post(
                "https://pro.nocaptchaai.com/solve", json=payload, headers=self.headers)
            data = response.json()
            print(data['solution'])
        except Exception as error:
            print(f"Fetch error: {error}")
