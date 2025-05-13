import streamlit as st
import pandas as pd
from twilio.rest import Client
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

st.set_page_config(page_title="WA Mass Sender", layout="centered")
st.title("📨 WhatsApp Mass Sender")

uploaded_file = st.file_uploader("Upload file CSV yang berisi data kontak", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Preview Data")
    st.dataframe(df.head())

    col_number = st.selectbox("Pilih kolom nomor WhatsApp", df.columns)
    col_name = st.selectbox("Pilih kolom nama", df.columns)

    default_message = "Selamat siang {nama}, bagaimana kabarmu?"
    message_template = st.text_area("Tulis pesan (gunakan {nama} sebagai placeholder)", value=default_message)

    if st.button("🚀 Kirim Pesan"):
        if not all([ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER]):
            st.error("⚠️ TWILIO credentials belum diset!")
        else:
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            for index, row in df.iterrows():
                name = str(row[col_name])
                number = str(row[col_number])
                personalized_message = message_template.replace("{nama}", name)

                try:
                    client.messages.create(
                        body=personalized_message,
                        from_=FROM_NUMBER,
                        to=f"whatsapp:{number}"
                    )
                    st.success(f"✅ Terkirim ke {name} ({number})")
                except Exception as e:
                    st.error(f"❌ Gagal kirim ke {name} ({number}): {e}")
