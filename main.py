import streamlit as st

# ---------------- CONFIG ------------------
st.set_page_config(page_title="ChildCare+ App", page_icon="🌿", layout="wide")

import base64
import growth
import vaccine
import medicine
import location
import mood

# ------------- CSS Styling -----------------
def inject_global_css():
    st.markdown("""
        <style>
        .block-container {
            
            background: linear-gradient(to right, #fceabb, #f8b500); /* Adding background color */
        }
        .login-title {
            text-align: center;
            font-size: 2rem;
            color: #333;
            margin-top: 2rem;
        }
        .login-box {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 20px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-box input {
            width: 250px;  # Set width of input box
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .login-box button {
            width: 250px;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .login-box button:hover {
            background-color: #45a049;
        }
        .start-button {
            text-align: center;
        }
        .main-title {
            text-align: center;
            font-size: 2rem;
            color: #333;
            margin-top: 3rem;
        }
        .description {
            font-size: 1.1rem;
            text-align: center;
            color: #333;
        }
        .feature-list {
            text-align: center;
            font-size: 1.1rem;
            color: #333;
        }
        .key-feature-row {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        }
        .key-feature-text {
            font-size: 16px;
            margin-right: 10px;
        }
        .key-feature-button {
            width: 150px;
        }
        .gif-center img {
            width: 200px;
            display: block;
            margin: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------- Starter Page ----------------

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/gif;base64,{encoded}"

def starter_page():
    inject_global_css()

    st.markdown("<h1 class='main-title'>🌿 ChildCare+ Pediatric Health Companion</h1>", unsafe_allow_html=True)

    # Main layout: GIF left, content right
    col1, col2 = st.columns([1, 2])
    with col1:
        # Add some empty space above the GIF to move it down
        st.markdown("<br>" * 2, unsafe_allow_html=True)  # Adds 5 empty lines (adjust as needed)

        gif_data_url = get_base64_image("kid-739_256.gif")
        st.markdown(f"""
            <img src="{gif_data_url}" width="300">
        """, unsafe_allow_html=True)


    with col2:
        st.markdown("<div class='description'>", unsafe_allow_html=True)
        st.markdown("""Caring for your child's health with technology & love.
        **ChildCare+** is an intelligent pediatric care system that empowers parents and doctors 
        to monitor growth, manage vaccinations, handle emergencies, and ensure safe medication.
        """, unsafe_allow_html=True)
        #st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='feature-list'>", unsafe_allow_html=True)
        st.markdown("""
        - 🤖 AI-Powered Health Prediction  
        - 💉 Digital Vaccination Cards  
        - 😊 Mood & Behavior Analysis  
        - 🚨 Emergency Response System  
        - 💊 Safe Medicine Alerts  
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Centered Start button
    # Create columns to move the button to the right
    col1, col2, col3 = st.columns([1, 2,4])  # Adjust the column ratio as needed
    st.markdown("<br>" * 2, unsafe_allow_html=True)
    # Add the button to col2 (which is the center column)
    with col3:
        if st.button("🚀 Start to Explore"):
            st.session_state.page = 'login'


# login page

def login_page():
    inject_global_css()

    # Title
    st.markdown("<h2 class='login-title'>🔐 Login to ChildCare+</h2>", unsafe_allow_html=True)

    # Centering the login form using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Login Form with a unique key for the text_input element
        pin = st.text_input("Enter your PIN", type="password", key="pin_input")  # Added unique key
        if st.button("Enter"):
            if pin == "2814":
                st.success("✅ Access granted!")
                st.session_state.page = "dashboard"
            else:
                st.error("❌ Incorrect PIN. Try again.")

# ------------- Dashboard Page ----------------
def dashboard_page():
    inject_global_css()

    st.markdown("<h1 class='main-title'>📊 Welcome to ChildCare+ Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    # Left Column: GIF
    with col1:
        gif_data_url = get_base64_image("campfire-7349_256.gif")
        st.markdown(f"<img src='{gif_data_url}' width='300'>", unsafe_allow_html=True)

    # Right Column: Buttons with descriptions
    with col2:
        st.markdown("### 🌟 Key Modules")

        # --- Growth ---
        if st.button("✅ AI-Powered Growth Tracking"):
            st.session_state.page = "growth"
        st.markdown("""
        <div style='margin-left: 10px; color: #444;'>
        Predict child's future height using Random Forest based on age, height, weight, and BMI.<br>
        Compares prediction with WHO standards to identify under/overgrowth with visual insights.
        </div><hr>""", unsafe_allow_html=True)

        # --- Vaccine ---
        if st.button("💉 Digital Vaccination Records"):
            st.session_state.page = "vaccine"
        st.markdown("""
        <div style='margin-left: 10px; color: #444;'>
        Generates personalized vaccination schedules based on age and medical history.<br>
        Exports QR-coded immunization cards for easy verification and record-keeping.
        </div><hr>""", unsafe_allow_html=True)

        # --- Medicine ---
        if st.button("💊 Safe Medicine Reminders"):
            st.session_state.page = "medicine"
        st.markdown("""
        <div style='margin-left: 10px; color: #444;'>
        Tracks pediatric medicines, expiry dates, and interactions with QR/barcode scanning.<br>
        Offers camera-based scanning, interaction checker, and downloadable inventory.
        </div><hr>""", unsafe_allow_html=True)

        # --- Mood ---
        if st.button("😊 Mood & Behavior Logs"):
            st.session_state.page = "mood"
        st.markdown("""
        <div style='margin-left: 10px; color: #444;'>
        Analyzes journal entries using sentiment analysis to detect child mood trends.<br>
        Logs mood, sleep, appetite, and screen time with charts and animation feedback.
        </div><hr>""", unsafe_allow_html=True)

        # --- Location ---
        if st.button("🚑 Emergency Location Tracking"):
            st.session_state.page = "location"
        st.markdown("""
        <div style='margin-left: 10px; color: #444;'>
        Simulates emergency alert system with one-tap SOS and fake live location tracking.<br>
        Displays nearby hospitals and logs emergency triggers with timestamp history.
        </div><hr>""", unsafe_allow_html=True)
        
# ------------- Main Routing Logic ----------------
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'starter'

    if st.session_state.page == 'starter':
        starter_page()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == "growth":
        growth.main()
    elif st.session_state.page == "vaccine":
        vaccine.show()
    elif st.session_state.page == "medicine":
        medicine.show()
    elif st.session_state.page == "location":
        location.show()
    elif st.session_state.page == "mood":
        mood.show()

# ------------- Run the App ----------------
if __name__ == '__main__':
    main()
