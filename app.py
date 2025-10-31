import base64
import requests

# HMRC Sandbox Credentials (replace with your own if needed)
CLIENT_ID = "CcpDjlMuq3UOvHrIft1zztMQ5E6f"
CLIENT_SECRET = "7f185020-4ccc-47da-8c0a-32d58a592f38"

def get_auth_header():
    token = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    return {
        "Accept": "application/vnd.hmrc.1.0+json",
        "Authorization": f"Basic {token}"
    }

def check_vat_insolvency(vrn: str):
    url = f"https://test-api.service.hmrc.gov.uk/organisations/vat/check-vat-number/insolvency-proceedings/{vrn}"
    response = requests.get(url, headers=get_auth_header())

    print(f"Status Code: {response.status_code}")
    try:
        print(response.json())
    except:
        print(response.text)

# Test VAT numbers published by HMRC for sandbox
test_vrns = ["243553782", "123456789"]

for vrn in test_vrns:
    print(f"\nChecking VAT Number: {vrn}")
    check_vat_insolvency(vrn)
