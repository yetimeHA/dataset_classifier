import json
import requests

import Config


def get_jwt() -> str:
    url = "https://christine-uat.dev.hyperanna.com/userservice/auth"
    data = {"userKey": "demo@hyperanna.com",
            "password": "abc123"}

    request_headers = {"Content-type": "application/json"}

    response = requests\
        .post(url, data=json.dumps(data), headers=request_headers, verify=False)
    return response.text


def list_datasets(jwt: str = "") -> dict:
    if jwt == "":
        jwt = get_jwt()
    url = "https://" + Config.HOST + "/api/users/simpleme"
    request_headers = {"x-auth-token": jwt}

    simpleme_results = requests \
        .get(url, headers=request_headers, verify=False) \
        .json()

    datasets = simpleme_results["datasets"]

    return {ds['id']: ds['name'] for ds in datasets}
