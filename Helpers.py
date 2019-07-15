import json
import requests


def get_jwt() -> str:
    url = "https://christine-uat.dev.hyperanna.com/userservice/auth"
    data = {"userKey": "demo@hyperanna.com",
            "password": "abc123"}

    request_headers = {"Content-type": "application/json"}

    response = requests\
        .post(url, data=json.dumps(data), headers=request_headers, verify=False)
    return response.text
