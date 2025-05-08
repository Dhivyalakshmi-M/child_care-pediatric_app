import streamlit as st
import pandas as pd
import qrcode
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def show():
    st.markdown("""
        <style>
        .block-container {
            background: linear-gradient(to right, #d4fc79, #96e6a1);

        }</style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 6, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "dashboard"

    st.markdown("<h1 style='text-align: center; color: black;'>🌟 Welcome to the Smart Vaccination Scheduler 🌟</h1>", unsafe_allow_html=True)

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/619/619034.png", width=100)
    st.sidebar.title("🧒 Enter Child Details")

    name = st.sidebar.text_input("👶 Name")
    age = st.sidebar.number_input("🎂 Age (Months)", min_value=0, max_value=216, value=6)
    gender = st.sidebar.selectbox("⚧️ Gender", ["Male", "Female"])
    medical_conditions = st.sidebar.text_area("🩺 Medical History (optional)", placeholder="E.g., egg allergy, asthma...")

    vaccine_data = [
        {"Vaccine": "Hepatitis B", "Dose": "Birth Dose", "DueMonth": 0},
        {"Vaccine": "OPV", "Dose": "0 Dose", "DueMonth": 0},
        {"Vaccine": "BCG", "Dose": "Single Dose", "DueMonth": 0},
        {"Vaccine": "Pentavalent", "Dose": "1st Dose", "DueMonth": 6},
        {"Vaccine": "Pentavalent", "Dose": "2nd Dose", "DueMonth": 10},
        {"Vaccine": "Pentavalent", "Dose": "3rd Dose", "DueMonth": 14},
        {"Vaccine": "IPV", "Dose": "1st Dose", "DueMonth": 14},
        {"Vaccine": "Rotavirus", "Dose": "1st Dose", "DueMonth": 6},
        {"Vaccine": "Rotavirus", "Dose": "2nd Dose", "DueMonth": 10},
        {"Vaccine": "Rotavirus", "Dose": "3rd Dose", "DueMonth": 14},
        {"Vaccine": "PCV", "Dose": "1st Dose", "DueMonth": 6},
        {"Vaccine": "PCV", "Dose": "2nd Dose", "DueMonth": 10},
        {"Vaccine": "PCV", "Dose": "3rd Dose", "DueMonth": 14},
        {"Vaccine": "MMR", "Dose": "1st Dose", "DueMonth": 9},
        {"Vaccine": "JE Vaccine", "Dose": "1st Dose", "DueMonth": 9},
        {"Vaccine": "DTP Booster", "Dose": "1st Booster", "DueMonth": 18},
        {"Vaccine": "OPV Booster", "Dose": "Booster", "DueMonth": 18},
        {"Vaccine": "MMR", "Dose": "2nd Dose", "DueMonth": 24},
        {"Vaccine": "Typhoid", "Dose": "1st Dose", "DueMonth": 24},
        {"Vaccine": "DTP Booster", "Dose": "2nd Booster", "DueMonth": 60},
    ]
    df = pd.DataFrame(vaccine_data)

    def generate_schedule(age_in_months, medical_history):
        schedule_df = df[df["DueMonth"] >= age_in_months].copy()
        if "egg" in medical_history.lower():
            schedule_df = schedule_df[~schedule_df["Vaccine"].str.contains("MMR", case=False)]
        schedule_df["VaccineDate"] = schedule_df["DueMonth"].apply(
            lambda m: (datetime.now() + relativedelta(months=m)).strftime("%Y-%m-%d")
        )
        return schedule_df.reset_index(drop=True)

    def create_qr_card(name, age, gender, schedule_df):
        qr_folder = "qr_codes"
        os.makedirs(qr_folder, exist_ok=True)
        data = {
            "name": name,
            "age_months": age,
            "gender": gender,
            "schedule": schedule_df.to_dict(orient="records"),
            "generated_on": datetime.now().strftime("%Y-%m-%d")
        }
        qr_data = json.dumps(data, indent=2)
        qr = qrcode.make(qr_data)
        filename = f"{name.replace(' ', '_')}_qr.png"
        qr_path = os.path.join(qr_folder, filename)
        qr.save(qr_path)
        return qr_path

    st.markdown("---")
    st.markdown("🔒 **Data Source**: WHO Immunization Guidelines | 📱 QR-based card & reminder system coming soon!")

    if st.button("📅 Generate Vaccination Schedule"):
        if name:
            schedule = generate_schedule(age, medical_conditions)
            st.success(f"📋 Vaccination Schedule for {name} ({age} months)")
            st.dataframe(schedule, use_container_width=True)
            qr_path = create_qr_card(name, age, gender, schedule)
            st.image(qr_path, caption="Scan to Verify", width=200)
            with open(qr_path, "rb") as file:
                st.download_button(
                    label="📥 Download QR Immunization Card",
                    data=file,
                    file_name=os.path.basename(qr_path),
                    mime="image/png"
                )
        else:
            st.warning("Please enter the child's name to proceed.")
