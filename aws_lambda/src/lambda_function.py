import json
import os
import requests
import datetime

RAILWAY_APP_URL = os.environ.get("RAILWAY_APP_URL", "https://mini-crm-production-4f5f.up.railway.app")
TARGET_ENDPOINT = "/emails/send-emails"

def lambda_handler(event: dict, context: dict) -> dict:
    """
    Função Lambda que será chamada pelo CloudWatch para disparar o envio de e-mails.
    """
    print(f"Evento recebido: {json.dumps(event)}")

    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)

    request_body = {
        "email_template": "discount_cupom",
        "subject": "SaSaLeLe",
        "template_fill_values": {
            "image_name": "discount_banner_1200_by_400.png",
            "email_template": "discount_cupom",
            "discount_value": 10,
            "cupom_code": "descontão",
            "valid_dates_start": today.isoformat(),
            "valid_dates_end": next_week.isoformat()
        }
    }

    url = f"{RAILWAY_APP_URL}{TARGET_ENDPOINT}"
    headers = {"Content-Type": "application/json"}

    print(f"Fazendo requisição POST para: {url}")
    print(f"Corpo da requisição: {json.dumps(request_body, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=request_body)
        response.raise_for_status() # Levanta um HTTPError para 4xx/5xx status codes

        print(f"Requisição bem-sucedida! Status Code: {response.status_code}")
        print(f"Resposta do servidor: {response.json()}")

        return {
            "statusCode": response.status_code,
            "body": response.json()
        }
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
        print(f"Resposta do servidor (erro): {http_err.response.text}")
        return {
            "statusCode": http_err.response.status_code if http_err.response else 500,
            "body": {"message": f"HTTP Error: {http_err}", "details": http_err.response.text}
        }
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Erro de Conexão: {conn_err}")
        return {
            "statusCode": 503, # Service Unavailable
            "body": {"message": f"Connection Error: {conn_err}"}
        }
    except requests.exceptions.Timeout as timeout_err:
        print(f"Erro de Timeout: {timeout_err}")
        return {
            "statusCode": 408, # Request Timeout
            "body": {"message": f"Timeout Error: {timeout_err}"}
        }
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na Requisição: {req_err}")
        return {
            "statusCode": 500,
            "body": {"message": f"Request Error: {req_err}"}
        }
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return {
            "statusCode": 500,
            "body": {"message": f"An unexpected error occurred: {e}"}
        }
