import streamlit as st
import webbrowser
import json
import os
from datetime import datetime
from fpdf import FPDF
import io

LINK_BASE = "https://www.studywithcare.com/cv/P"
HISTORY_FILE = "search_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            data = json.load(file)
    else:
        data = {"date": "", "history": []}
    return data

def save_history(data):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(data, file)

def create_pdf(history, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Search History for {date}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    if not history:
        pdf.cell(0, 10, "No searches recorded today.", ln=True)
    else:
        for i, item in enumerate(history, 1):
            pdf.cell(0, 10, f"{i}. {LINK_BASE}{item}", ln=True)

    pdf_str = pdf.output(dest='S').encode('latin1')
    pdf_bytes = io.BytesIO(pdf_str)
    pdf_bytes.seek(0)
    return pdf_bytes

st.set_page_config(page_title="Topic Details Link", layout="centered")
st.title("📄 Topic Link Details")

today = datetime.now().strftime("%Y-%m-%d")
history_data = load_history()

if history_data["date"] != today:
    history_data = {"date": today, "history": []}
    save_history(history_data)

user_input = st.text_input("Enter ID", placeholder="e.g., 12345")

if st.button("Open Link"):
    user_input = user_input.strip()
    if user_input:
        full_url = f"{LINK_BASE}{user_input}"
        st.success(f"Click the link to open: {full_url}")
        webbrowser.open(full_url)

        if user_input in history_data["history"]:
            history_data["history"].remove(user_input)
        history_data["history"].insert(0, user_input)
        save_history(history_data)
    else:
        st.warning("Please enter a valid ID.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Clear Today's History"):
        history_data["history"] = []
        save_history(history_data)
        st.success("History cleared for today!")

with col2:
    pdf_file = create_pdf(history_data["history"], today)
    st.download_button(
        label="⬇️ Export History to PDF",
        data=pdf_file,
        file_name=f"search_history_{today}.pdf",
        mime="application/pdf"
    )

if history_data["history"]:
    st.markdown("### 🔍 Today's Search History (Latest First):")
    for idx, item in enumerate(history_data["history"], 1):
        st.markdown(f"{idx}. [{LINK_BASE}{item}]({LINK_BASE}{item})")

footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6;
    color: #444444;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    opacity: 0.7;
}
</style>
<div class="footer">
    Made by Akashdeep Dam (Freelance Data Analyst, PGDCA (IGNOU), MCA (IGNOU), Certificate in Data Science, Ex-Software Developer)
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
