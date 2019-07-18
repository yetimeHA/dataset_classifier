import json
import requests

import Config


def get_jwt() -> str:
    url = "https://christine-uat.dev.hyperanna.com/userservice/auth"
    data = {"userKey": Config.USEREMAIL,
            "password": Config.USERPASS}

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


def get_column_unique_values(dataset_id, user_id, jwt="") -> dict:
    """Queries MetaMeta Service to retrieve a dictonary of column-unique-values"""
    if jwt == "":
        jwt = get_jwt()
    url = Config.METAMETA_URL + "/dataset/"+str(dataset_id)+"/column-unique-values"
    request_params = {"userId": str(user_id)}
    request_headers = {"x-auth-token": jwt}

    col_uniques_result = requests\
        .get(url, params=request_params, headers=request_headers)\
        .json()

    return col_uniques_result