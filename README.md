# child_care-pediatric_app
"A smart medicine management app using Streamlit, OpenCV, and QR code scanning. Add medicines via QR upload or live camera, store details in CSV, and prevent duplicate entries using session tracking. Simple UI for child care or pharmacy use."

📘 README.md
markdown
Copy
Edit
# 🌿 ChildCare+ Pediatric Health Companion

**ChildCare+** is a comprehensive Streamlit-based web application designed to assist parents and pediatricians in tracking child health through AI, real-time alerts, mood analytics, vaccination management, and medicine safety.

---

## 🚀 Project Overview

ChildCare+ is a unified pediatric care solution that combines smart algorithms, health data visualization, and safety utilities in a child-friendly digital environment. It aims to assist caregivers in making informed decisions while creating a joyful digital health journal for kids.

---

## ✨ Key Features

| Module        | Description |
|---------------|-------------|
| 📊 **AI Growth Predictor** (`growth.py`) | Uses Random Forest Regression to forecast a child's height based on age, weight, and BMI. Compares predictions with WHO growth charts to detect abnormalities. |
| 💉 **Vaccination Scheduler** (`vaccine.py`) | Dynamically generates vaccine schedules based on child’s age and medical history. Outputs scannable QR-code cards for secure access and verification. |
| 💊 **Medicine Tracker** (`medicine.py`) | Tracks pediatric medicines, allows QR/barcode-based additions, checks for interactions, and provides expiry warnings with visual indicators. |
| 😊 **Mood & Behavior Tracker** (`mood.py`) | Uses AI (TextBlob) to analyze mood from daily journals and logs sleep, screen time, and appetite. Includes trend graphs and animated Lottie feedback. |
| 🚨 **Emergency Location System** (`location.py`) | Simulates a one-click emergency alert system, generates fake GPS location, notifies local hospitals, and records emergency history. |
| 🏠 **Main Dashboard** (`main.py`) | Manages routing, user login, dashboard UI, and links all features into a single web interface with secure PIN login and animated onboarding. |

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/childcare-plus.git
cd childcare-plus
2. Create a Virtual Environment (Optional)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Required Packages
bash
Copy
Edit
## System Packages Required

This app uses `pyzbar` for QR code decoding, which depends on the `zbar` shared library.

If deploying to **Streamlit Cloud**, add the following to a file named `apt-packages.txt`:

libzbar0

perl
Copy
Edit

This ensures the app installs the required system package during deployment.
pip install -r requirements.txt
4. Run the Application
bash
Copy
Edit
streamlit run main.py
🧾 File Structure
bash
Copy
Edit
childcare-plus/
│
├── main.py                # Core routing and dashboard UI
├── growth.py              # Growth prediction using ML
├── vaccine.py             # Vaccination schedule generator
├── medicine.py            # Medicine management with QR scanning
├── mood.py                # Mood tracker and sentiment analysis
├── location.py            # Emergency alert with location simulation
├── requirements.txt       # Python package dependencies
└── README.md              # Project documentation
🔐 Login
The app uses a simple PIN-based login.

Default PIN: 2814

You can change this in main.py inside the login_page() function.

📦 Requirements
See requirements.txt, or install directly:

bash
Copy
Edit
pip install streamlit pandas numpy scikit-learn plotly textblob streamlit-lottie qrcode opencv-python Pillow pyzbar python-dateutil
📸 Screenshots
Include screenshots or animated GIFs here if needed.

🪪 License
This project is licensed under the MIT License:

sql
Copy
Edit
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included       
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📬 Contact
Created by [Your Name] – feel free to reach out via [your email or GitHub profile link].






