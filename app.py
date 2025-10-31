import base64
import requests
import streamlit as st

# HMRC Dev Hub Credentials (Sandbox)
client_id = "CcpDjlMuq3UOvHrIft1zztMQ5E6f"
client_secret = "7f185020-4ccc-47da-8c0a-32d58a592f38"

def generate_auth_token(client_id, client_secret):
    return base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

def check_vat(vrn):
    token = generate_auth_token(client_id, client_secret)
    headers = {
        "Accept": "application/vnd.hmrc.1.0+json",
        "Authorization": f"Basic {token}"
    }
    url = f"https://test-api.service.hmrc.gov.uk/organisations/vat/check-vat-number/lookup/{vrn}"
    return requests.get(url, headers=headers)

# Streamlit UI
st.title("HMRC VAT Registration Checker (Sandbox)")
vrn = st.text_input("Enter VAT Registration Number:", "243553782")

if st.button("Check VAT"):
    response = check_vat(vrn)
    if response.status_code == 200:
        st.success("Found VAT record ✅")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        try:
            st.json(response.json())
        except:
            st.write(response.text)
