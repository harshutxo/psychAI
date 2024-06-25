import requests

def get_response_from_huggingface(user_input):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": f"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"}  # Replace with your Hugging Face API key

    payload = {
        "inputs": user_input,
        "parameters": {
            "max_length": 150,
        },
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].strip()
    else:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

