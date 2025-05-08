import os
import json
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd 
import cv2
import numpy as np
from PIL import Image

def show():
    st.markdown("""
        <style>
            .block-container {
                background: linear-gradient(to right, #00d2ff, #3a7bd5);
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "dashboard"

    MEDICINE_FILE = "medicine_data.csv"
    today = datetime.now().date()

    @st.cache_data
    def load_data():
        if os.path.exists(MEDICINE_FILE):
            df = pd.read_csv(MEDICINE_FILE)
            if not df.empty:
                return df
        sample_data = pd.DataFrame([
            {"Medicine Name": "Amoxicillin", "Expiry Date": "2025-12-31", "Dosage": "5ml twice daily", "Purpose": "Antibiotic", "Doctor": "Dr. Smith"},
            {"Medicine Name": "Ibuprofen", "Expiry Date": "2024-10-15", "Dosage": "100mg after meal", "Purpose": "Pain relief", "Doctor": "Dr. Meena"},
            {"Medicine Name": "Cough Syrup", "Expiry Date": "2025-03-01", "Dosage": "10ml at bedtime", "Purpose": "Cough treatment", "Doctor": "Dr. Arjun"},
            {"Medicine Name": "Vitamin D", "Expiry Date": "2025-06-20", "Dosage": "1 tab daily", "Purpose": "Supplement", "Doctor": "Dr. Kavya"},
            {"Medicine Name": "Paracetamol", "Expiry Date": "2024-09-30", "Dosage": "250mg twice a day", "Purpose": "Fever", "Doctor": "Dr. Ramesh"},
            {"Medicine Name": "Cetirizine", "Expiry Date": "2025-01-10", "Dosage": "5ml once daily", "Purpose": "Allergy", "Doctor": "Dr. Nisha"}
        ])
        sample_data.to_csv(MEDICINE_FILE, index=False)
        return sample_data

    df = load_data()

    def decode_qr_data(image):
        detector = cv2.QRCodeDetector()
        if isinstance(image, Image.Image):
            image = np.array(image.convert("RGB"))
        elif isinstance(image, np.ndarray):
            pass
        else:
            st.error("Unsupported image format.")
            return None

        data, bbox, _ = detector.detectAndDecode(image)
        if data:
            try:
                return json.loads(data)
            except Exception as e:
                st.error(f"❌ Invalid QR code format: {e}")
        return None

    st.subheader("📷 Upload or Scan QR Code")
    uploaded_img = st.file_uploader("Upload QR Code (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_img:
        image = Image.open(uploaded_img)
        qr_data = decode_qr_data(image)

        if qr_data:
            df = pd.concat([df, pd.DataFrame([qr_data])], ignore_index=True)
            df.to_csv(MEDICINE_FILE, index=False)
            st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} added from uploaded QR!")

    use_camera = st.checkbox("📸 Use Camera to Scan QR")

    if 'scanned_qrs' not in st.session_state:
        st.session_state.scanned_qrs = []

    if use_camera:
        st.info("Camera will auto-close after one scan.")
        stframe = st.empty()
        cam = cv2.VideoCapture(0)
        scanned = False

        while cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                break

            stframe.image(frame, channels="BGR", use_container_width=True)
            qr_data = decode_qr_data(frame)
            if qr_data and qr_data not in st.session_state.scanned_qrs:
                df = pd.concat([df, pd.DataFrame([qr_data])], ignore_index=True)
                df.to_csv(MEDICINE_FILE, index=False)
                st.session_state.scanned_qrs.append(qr_data)
                st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} scanned and added!")
                st.snow()
                cam.release()
                stframe.empty()

                scanned = True
                break

        if not scanned:
            cam.release()
            cv2.destroyAllWindows()

    df = load_data()

    st.sidebar.header("➕ Add New Medicine")
    with st.sidebar.form("add_medicine"):
        name = st.text_input("Medicine Name")
        expiry = st.date_input("Expiry Date")
        dose = st.text_input("Dosage")
        purpose = st.text_input("Purpose")
        doctor = st.text_input("Prescribed By")
        submit = st.form_submit_button("Add")
        if submit and name:
            new_row = pd.DataFrame([{
                "Medicine Name": name,
                "Expiry Date": expiry.strftime('%Y-%m-%d'),
                "Dosage": dose,
                "Purpose": purpose,
                "Doctor": doctor
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(MEDICINE_FILE, index=False)
            st.sidebar.success(f"✅ {name} added!")

    st.sidebar.header("🗑️ Delete Medicine")
    if not df.empty:
        del_name = st.sidebar.selectbox("Select to Delete", df["Medicine Name"].unique())
        if st.sidebar.button("Delete"):
            df = df[df["Medicine Name"] != del_name]
            df.to_csv(MEDICINE_FILE, index=False)
            st.sidebar.success(f"✅ {del_name} deleted!")

    st.subheader("📦 Medicine Inventory")
    def highlight_expiry(row):
        try:
            exp = datetime.strptime(row["Expiry Date"], "%Y-%m-%d").date()
            if exp < today:
                return ['background-color: #f8d7da; color: #721c24'] * len(row)
            elif exp <= today + timedelta(days=30):
                return ['background-color: #fff3cd'] * len(row)
        except:
            return [''] * len(row)
        return [''] * len(row)

    if not df.empty:
        st.dataframe(df.style.apply(highlight_expiry, axis=1), use_container_width=True)
    else:
        st.info("No medicines found. Use the sidebar to add or scan.")

    st.subheader("⚠️ Check for Drug Interactions")
    interactions = {
        "Amoxicillin": ["Warfarin"],
        "Ciprofloxacin": ["Antacids"],
        "Ibuprofen": ["Aspirin"],
        "Paracetamol": [],
    }

    selected = st.multiselect("Select Medicines to Check", df["Medicine Name"].unique())
    if selected:
        warnings = []
        for med in selected:
            for check in selected:
                if check in interactions.get(med, []) and med != check:
                    warnings.append(f"{med} may interact with {check}")
        if warnings:
            st.warning("🚨 Interactions Found:\n" + "\n".join(warnings))
        else:
            st.success("✅ No known interactions.")

    with open(MEDICINE_FILE, "rb") as f:
        st.download_button("Download Medicine Data", f, file_name="medicine_data.csv")
