import streamlit as st
import requests
import base64

# ──────────────────────────────────────────
#  HMRC Sandbox Credentials
# ──────────────────────────────────────────
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

BASE_URL = "https://test-api.service.hmrc.gov.uk"


def generate_auth_header():
    token = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    return {
        "Accept": "application/vnd.hmrc.1.0+json",
        "Authorization": f"Basic {token}"
    }


def check_vat_insolvency(vrn: str):
    endpoint = f"/organisations/vat/check-vat-number/insolvency-proceedings/{vrn}"
    url = BASE_URL + endpoint
    response = requests.get(url, headers=generate_auth_header())
    return response


# ──────────────────────────────────────────
# Streamlit UI
# ──────────────────────────────────────────
st.title("🔍 HMRC VAT Insolvency Checker (Sandbox)")
st.write("Enter a UK VAT Registration Number to fetch insolvency status.")

# Input
vrn = st.text_input("VAT Registration Number (9 digits):", "243553782")

if st.button("Check Status"):
    if not vrn.isdigit() or len(vrn) != 9:
        st.error("❌ VRN must be exactly 9 digits")
        st.stop()

    response = check_vat_insolvency(vrn)
    st.write(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        insolvent = data.get("insolvencyIndicator", None)

        if insolvent is True:
            st.error("⚠ Insolvency proceedings are in place")
        elif insolvent is False:
            st.success("✅ No insolvency proceedings")
        else:
            st.warning("Unknown status returned:")
            st.json(data)
    else:
        try:
            st.json(response.json())
        except:
            st.write(response.text)

st.markdown("---")
st.caption("HMRC VAT Sandbox API — Basic Auth Mode")
