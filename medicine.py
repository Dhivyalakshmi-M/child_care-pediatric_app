import os
import json
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import numpy as np

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

    # ------------------ Configuration ------------------
    MEDICINE_FILE = "medicine_data.csv"
    today = datetime.now().date()

    # ------------------ Load Medicine Data ------------------
    @st.cache_data
   
    def load_data():
        if os.path.exists(MEDICINE_FILE):
            df = pd.read_csv(MEDICINE_FILE)
            if not df.empty:
                return df

        # Sample data to auto-fill if file is empty or missing
        sample_data = pd.DataFrame([
            {
                "Medicine Name": "Amoxicillin",
                "Expiry Date": "2025-12-31",
                "Dosage": "5ml twice daily",
                "Purpose": "Antibiotic",
                "Doctor": "Dr. Smith"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Expiry Date": "2024-10-15",
                "Dosage": "100mg after meal",
                "Purpose": "Pain relief",
                "Doctor": "Dr. Meena"
            },
            {
                "Medicine Name": "Cough Syrup",
                "Expiry Date": "2025-03-01",
                "Dosage": "10ml at bedtime",
                "Purpose": "Cough treatment",
                "Doctor": "Dr. Arjun"
            },
            {
                "Medicine Name": "Vitamin D",
                "Expiry Date": "2025-06-20",
                "Dosage": "1 tab daily",
                "Purpose": "Supplement",
                "Doctor": "Dr. Kavya"
            },
            {
                "Medicine Name": "Paracetamol",
                "Expiry Date": "2024-09-30",
                "Dosage": "250mg twice a day",
                "Purpose": "Fever",
                "Doctor": "Dr. Ramesh"
            },
            {
                "Medicine Name": "Cetirizine",
                "Expiry Date": "2025-01-10",
                "Dosage": "5ml once daily",
                "Purpose": "Allergy",
                "Doctor": "Dr. Nisha"
            }
        ])
        sample_data.to_csv(MEDICINE_FILE, index=False)
        return sample_data


    df = load_data()

    # ------------------ CSS ------------------
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                color: #4CAF50;
                font-weight: bold;
            }
            .subtitle {
                text-align: center;
                font-size: 20px;
                color: #555;
                margin-bottom: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ------------------ Title ------------------
    st.markdown("<h1 class='main-title'>🩺 Pediatric Medicine Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Track expiry dates, interactions & more!</p>", unsafe_allow_html=True)

    # ------------------ Function to Decode QR ------------------
    def decode_qr_data(image):
        if isinstance(image, Image.Image):
            image = np.array(image.convert("RGB"))
        decoded_objects = decode(image)
        for obj in decoded_objects:
            try:
                data = json.loads(obj.data.decode("utf-8"))
                return data
            except Exception as e:
                st.error(f"❌ Invalid QR code: {e}")
                return None
        return None

    # ------------------ Upload QR Code ------------------
    # Function to load data from CSV
    def load_data():
        try:
            return pd.read_csv(MEDICINE_FILE)
        except FileNotFoundError:
            return pd.DataFrame(columns=["Medicine Name", "QR Data"])

    # Initialize session state to store scanned QR data
    if "scanned_qrs" not in st.session_state:
        st.session_state.scanned_qrs = []

    # Initialize data from the file or create a new one
    df = load_data()

    # ------------------ QR Code Upload Section ------------------
    st.subheader("📷 Upload or Scan QR Code")
    uploaded_img = st.file_uploader("Upload QR Code (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_img:
        image = Image.open(uploaded_img)
        qr_data = decode_qr_data(image)  # Function for decoding QR data

        if qr_data:
            # Add new data to DataFrame and save to CSV
            df = pd.concat([df, pd.DataFrame([qr_data])], ignore_index=True)
            df.to_csv(MEDICINE_FILE, index=False)
            st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} added from uploaded QR!")

    # ------------------ Camera Scanner Section ------------------
    use_camera = st.checkbox("📸 Use Camera to Scan QR")

    if use_camera:
        st.info("Camera will auto-close after each scan.")
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
                # Add new entry to DataFrame and save to CSV
                new_entry = pd.DataFrame([qr_data])
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_csv(MEDICINE_FILE, index=False)

                # Store scanned QR data in session state to avoid reprocessing the same QR code
                st.session_state.scanned_qrs.append(qr_data)

                st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} scanned and added!")
                st.snow()  # Add snow effect

                # Stop camera and clear frame after scan
                cam.release()
                cv2.destroyAllWindows()
                stframe.empty()
                scanned = True
                break

        if not scanned:
            cam.release()
            cv2.destroyAllWindows()

    # Reload data from file after camera scan
    df = load_data()

    # ------------------ Add New Medicine ------------------
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

    # ------------------ Delete Medicine ------------------
    st.sidebar.header("🗑️ Delete Medicine")
    if not df.empty:
        del_name = st.sidebar.selectbox("Select to Delete", df["Medicine Name"].unique())
        if st.sidebar.button("Delete"):
            df = df[df["Medicine Name"] != del_name]
            df.to_csv(MEDICINE_FILE, index=False)
            st.sidebar.success(f"✅ {del_name} deleted!")

    # ------------------ Display Medicines ------------------
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

    # ------------------ Check Drug Interactions ------------------
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

    # ------------------ Download CSV ------------------
    with open(MEDICINE_FILE, "rb") as f:
        st.download_button("⬇️ Download Medicine List", f, file_name="medicine_data.csv", mime="text/csv")import os
import json
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from PIL import Image
import cv2

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

    # ------------------ Configuration ------------------
    MEDICINE_FILE = "medicine_data.csv"
    today = datetime.now().date()

    # ------------------ Load Medicine Data ------------------
    @st.cache_data
   
    def load_data():
        if os.path.exists(MEDICINE_FILE):
            df = pd.read_csv(MEDICINE_FILE)
            if not df.empty:
                return df

        # Sample data to auto-fill if file is empty or missing
        sample_data = pd.DataFrame([
            {
                "Medicine Name": "Amoxicillin",
                "Expiry Date": "2025-12-31",
                "Dosage": "5ml twice daily",
                "Purpose": "Antibiotic",
                "Doctor": "Dr. Smith"
            },
            {
                "Medicine Name": "Ibuprofen",
                "Expiry Date": "2024-10-15",
                "Dosage": "100mg after meal",
                "Purpose": "Pain relief",
                "Doctor": "Dr. Meena"
            },
            {
                "Medicine Name": "Cough Syrup",
                "Expiry Date": "2025-03-01",
                "Dosage": "10ml at bedtime",
                "Purpose": "Cough treatment",
                "Doctor": "Dr. Arjun"
            },
            {
                "Medicine Name": "Vitamin D",
                "Expiry Date": "2025-06-20",
                "Dosage": "1 tab daily",
                "Purpose": "Supplement",
                "Doctor": "Dr. Kavya"
            },
            {
                "Medicine Name": "Paracetamol",
                "Expiry Date": "2024-09-30",
                "Dosage": "250mg twice a day",
                "Purpose": "Fever",
                "Doctor": "Dr. Ramesh"
            },
            {
                "Medicine Name": "Cetirizine",
                "Expiry Date": "2025-01-10",
                "Dosage": "5ml once daily",
                "Purpose": "Allergy",
                "Doctor": "Dr. Nisha"
            }
        ])
        sample_data.to_csv(MEDICINE_FILE, index=False)
        return sample_data


    df = load_data()

    # ------------------ CSS ------------------
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                color: #4CAF50;
                font-weight: bold;
            }
            .subtitle {
                text-align: center;
                font-size: 20px;
                color: #555;
                margin-bottom: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ------------------ Title ------------------
    st.markdown("<h1 class='main-title'>🩺 Pediatric Medicine Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Track expiry dates, interactions & more!</p>", unsafe_allow_html=True)

    # ------------------ Function to Decode QR ------------------
    def decode_qr_data(image):
        if isinstance(image, Image.Image):
            image = np.array(image.convert("RGB"))
        decoded_objects = decode(image)
        for obj in decoded_objects:
            try:
                data = json.loads(obj.data.decode("utf-8"))
                return data
            except Exception as e:
                st.error(f"❌ Invalid QR code: {e}")
                return None
        return None

    # ------------------ Upload QR Code ------------------
    # Function to load data from CSV
    def load_data():
        try:
            return pd.read_csv(MEDICINE_FILE)
        except FileNotFoundError:
            return pd.DataFrame(columns=["Medicine Name", "QR Data"])

    # Initialize session state to store scanned QR data
    if "scanned_qrs" not in st.session_state:
        st.session_state.scanned_qrs = []

    # Initialize data from the file or create a new one
    df = load_data()

    # ------------------ QR Code Upload Section ------------------
    st.subheader("📷 Upload or Scan QR Code")
    uploaded_img = st.file_uploader("Upload QR Code (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if uploaded_img:
        image = Image.open(uploaded_img)
        qr_data = decode_qr_data(image)  # Function for decoding QR data

        if qr_data:
            # Add new data to DataFrame and save to CSV
            df = pd.concat([df, pd.DataFrame([qr_data])], ignore_index=True)
            df.to_csv(MEDICINE_FILE, index=False)
            st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} added from uploaded QR!")

    # ------------------ Camera Scanner Section ------------------
    use_camera = st.checkbox("📸 Use Camera to Scan QR")

    if use_camera:
        st.info("Camera will auto-close after each scan.")
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
                # Add new entry to DataFrame and save to CSV
                new_entry = pd.DataFrame([qr_data])
                df = pd.concat([df, new_entry], ignore_index=True)
                df.to_csv(MEDICINE_FILE, index=False)

                # Store scanned QR data in session state to avoid reprocessing the same QR code
                st.session_state.scanned_qrs.append(qr_data)

                st.success(f"✅ {qr_data.get('Medicine Name', 'Medicine')} scanned and added!")
                st.snow()  # Add snow effect

                # Stop camera and clear frame after scan
                cam.release()
                cv2.destroyAllWindows()
                stframe.empty()
                scanned = True
                break

        if not scanned:
            cam.release()
            cv2.destroyAllWindows()

    # Reload data from file after camera scan
    df = load_data()

    # ------------------ Add New Medicine ------------------
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

    # ------------------ Delete Medicine ------------------
    st.sidebar.header("🗑️ Delete Medicine")
    if not df.empty:
        del_name = st.sidebar.selectbox("Select to Delete", df["Medicine Name"].unique())
        if st.sidebar.button("Delete"):
            df = df[df["Medicine Name"] != del_name]
            df.to_csv(MEDICINE_FILE, index=False)
            st.sidebar.success(f"✅ {del_name} deleted!")

    # ------------------ Display Medicines ------------------
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

    # ------------------ Check Drug Interactions ------------------
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

    # ------------------ Download CSV ------------------
    with open(MEDICINE_FILE, "rb") as f:
        st.download_button("⬇️ Download Medicine List", f, file_name="medicine_data.csv", mime="text/csv")
