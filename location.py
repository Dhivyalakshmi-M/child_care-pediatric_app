import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ------------------------ Settings ------------------------
#st.set_page_config(page_title="🆘 Emergency Response", page_icon="🚨", layout="centered")
def show():
    # ------------------------ Title ------------------------
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "dashboard"
    st.markdown("""
        <style>
        .block-container {
           
            background: linear-gradient(to right, #DAE2F8, #D6A4A4);


        }</style>
    """, unsafe_allow_html=True)
            
    st.markdown("""
        <style>
            .header {
                text-align: center;
                color: red;
                font-size: 3rem;
                font-weight: bold;
                font-family: 'Arial';
                display: inline-block;  /* Aligns title text in a straight line */
                margin-bottom: 20px;
            }
        </style>
        <div class="header">
            🚨 Smart Emergency Response System
        </div>
    """, unsafe_allow_html=True)

    # ------------------------ Subtitle ------------------------
    st.markdown("<h3 style='text-align: center; color: #ff5733;'>📍 One-tap SOS with live location and instant alerts</h3>", unsafe_allow_html=True)

    # ------------------------ Add Background Color ------------------------
    st.markdown("""
        <style>
            .stApp {
                background-color: light green;  /* Light grey background color */
                height: 100vh;
            }
        </style>
    """, unsafe_allow_html=True)

    # ------------------------ Simulated GPS Location ------------------------
    def get_fake_location():
        locations = [
            {"lat": 12.9716, "lon": 77.5946, "place": "Bangalore"},
            {"lat": 28.6139, "lon": 77.2090, "place": "Delhi"},
            {"lat": 19.0760, "lon": 72.8777, "place": "Mumbai"},
            {"lat": 13.0827, "lon": 80.2707, "place": "Chennai"},
            {"lat": 22.5726, "lon": 88.3639, "place": "Kolkata"}
        ]
        return random.choice(locations)

    # ------------------------ Simulated Hospitals ------------------------
    def get_nearby_hospitals(location):
        hospitals = {
            "Bangalore": ["Manipal Hospital", "Rainbow Children’s Hospital", "Sakra World Hospital"],
            "Delhi": ["Apollo Hospital", "Fortis Healthcare", "Max Super Specialty"],
            "Mumbai": ["Lilavati Hospital", "Hiranandani Hospital", "Wockhardt Hospital"],
            "Chennai": ["Global Hospitals", "Kauvery Hospital", "MIOT International"],
            "Kolkata": ["AMRI Hospital", "Belle Vue Clinic", "ILS Hospitals"]
        }
        return hospitals.get(location["place"], [])

    # ------------------------ Emergency Trigger ------------------------
    # Centered Emergency Alert Button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🆘 Tap to Send Emergency Alert", key="emergency_button"):
            st.warning("📡 Sending emergency alert...")
            location = get_fake_location()
            hospitals = get_nearby_hospitals(location)

            st.success(f"✅ Alert sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"**🌍 Location:** {location['place']} ({location['lat']}, {location['lon']})")
            
            st.markdown("### 🏥 Notified Hospitals & Pediatricians:")
            for h in hospitals:
                st.markdown(f"- 🚑 {h}")

            st.balloons()

    # ------------------------ Sample Emergency History ------------------------
    st.markdown("---")
    st.markdown("### 📋 Past Emergency Triggers")
    sample_history = pd.DataFrame({
        "Date & Time": ["2025-05-05 14:32", "2025-04-21 18:10", "2025-03-11 09:45"],
        "Location": ["Delhi", "Bangalore", "Chennai"],
        "Hospitals Notified": ["Apollo Hospital", "Manipal Hospital", "Global Hospitals"]
    })
    st.dataframe(sample_history)

    # ------------------------ Footer ------------------------
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: gray;'>Developed with ❤️ for Child Safety</div>", unsafe_allow_html=True)

