import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import plotly.graph_objects as go

# Load WHO data
who_boys = pd.read_excel('C:/Users/varma/Downloads/hfa-boys-z-who-2007-exp.xlsx')
who_girls = pd.read_excel('C:/Users/varma/Downloads/hfa-girls-z-who-2007-exp.xlsx')

# ------------------ Streamlit UI Config ------------------
#st.set_page_config(page_title="AI Growth Predictor", page_icon="📈", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            background-color: #f8f9fa;
        }

        .sidebar-content {
            background-color: #e9ecef;
        }

        .stButton > button {
            background-color: #28a745;
            color: white;
            font-size: 16px;
            padding: 8px 18px;
            border-radius: 8px;
            border: none;
        }

        .alert {
            color: white;
            background-color: #dc3545;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }

        .normal {
            color: white;
            background-color: #28a745;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# ------------------ Data Generation ------------------
@st.cache_data
def generate_synthetic_data():
    np.random.seed(42)
    age = np.random.randint(0, 19, size=200)
    gender = np.random.choice(['Male', 'Female'], size=200)
    height = 50 + (age * 5) + np.random.normal(0, 10, size=200)
    weight = 5 + (age * 3) + np.random.normal(0, 5, size=200)
    bmi = weight / (height / 100) ** 2
    data = pd.DataFrame({'age': age, 'height': height, 'weight': weight, 'BMI': bmi, 'gender': gender})
    return data

# ------------------ Model Training ------------------
@st.cache_resource
def train_model(data):
    X = data[['age', 'height', 'weight', 'BMI']]
    y = data['height']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    return model, mae

def get_lms_parameters(age, gender):
    # Convert age from years to months
    age_in_months = age * 12
    
    # Define the valid age range (in months)
    min_age_months = 5 * 12  # 5 years (in months)
    max_age_months = 19 * 12  # 19 years (in months)
    
    # Check if the age is within the valid range
    if age_in_months < min_age_months or age_in_months > max_age_months:
        print(f"Age out of range for WHO data. Valid age range is {min_age_months // 12} to {max_age_months // 12} years.")
        return None, None, None

    # Select the dataset based on gender
    if gender == 'Male':
        data = who_boys
    else:
        data = who_girls

    # Find the corresponding row for the given age in months
    row = data[data['Month'] == age_in_months]
    
    if not row.empty:
        # Extract the L, M, and S values
        L = row['L'].values[0]
        M = row['M'].values[0]
        S = row['S'].values[0]
        return L, M, S
    else:
        print("No data available for the specified age.")
        return None, None, None


def calculate_expected_height_range(age, gender):
    L, M, S = get_lms_parameters(age, gender)
    if L is None:
        return None, None
    z_scores = [-2, 2]  # For ±2 standard deviations
    heights = []
    for z in z_scores:
        if L != 0:
            height = M * ((1 + L * S * z) ** (1 / L))
        else:
            height = M * np.exp(S * z)
        heights.append(height)
    return heights[0], heights[1]

def check_growth_abnormality(predicted_height, age, gender):
    # Calculate the expected height range for the given age and gender
    min_height, max_height = calculate_expected_height_range(age, gender)
    
    # Check if the age is out of range
    if min_height is None:
        return "❌ Age out of range for WHO data. Please provide an age between 6 and 19 years."
    
    # Check for undergrowth
    if predicted_height < min_height:
        return (f"⚠️ Abnormal Growth: Predicted height is {predicted_height:.2f} cm.\n"
                    f"Expected range: {min_height:.2f} - {max_height:.2f} cm.\n"
                    f"🩺 Possible UNDERGROWTH. Please consult a healthcare provider.")
    
    # Check for overgrowth
    elif predicted_height > max_height:
        return (f"⚠️ Abnormal Growth: Predicted height is {predicted_height:.2f} cm.\n"
                    f"Expected range: {min_height:.2f} - {max_height:.2f} cm.\n"
                    f"🩺 Possible OVERGROWTH. Please consult a healthcare provider.")
    
    # Normal growth
    else:
        return (f"✅ Growth is NORMAL: Predicted height is {predicted_height:.2f} cm.\n"
                    f"Within the expected range: {min_height:.2f} - {max_height:.2f} cm.\n"
                    f"👍 Keep up the good growth!")
    
# ------------------ BMI Category ------------------
def bmi_category(bmi):
    if bmi < 14:
        return "Underweight"
    elif 14 <= bmi < 18:
        return "Normal"
    elif 18 <= bmi < 21:
        return "Slightly Overweight"
    else:
        return "Overweight"

# ------------------ Main App ------------------
def main():
    st.markdown("""
        <style>
        .block-container {
           
            background: linear-gradient(to right, #ff9a9e, #fad0c4);

        }</style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 20, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = "dashboard"
            
    st.title("📊 AI-Powered Child Growth Prediction")
    st.subheader("Predict growth trends with BMI using AI and visualize results clearly.")

    # Load data and train model
    data = generate_synthetic_data()
    model, mae = train_model(data)

    st.markdown(f"### 🧪 Model Evaluation - Mean Absolute Error: `{mae:.2f}`")

    # Stylish Sidebar Header
    st.sidebar.markdown("""
        <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            background-color:green;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }
        .sidebar-section {
            margin-top: 20px;
            padding: 10px;
            border-radius: 8px;
        }
        .stNumberInput > label, .stSelectbox > label {
            font-size: 16px !important;
            font-weight: 500 !important;
        }
        </style>
        <div class="sidebar-title">👶 Enter Child Details</div>
    """, unsafe_allow_html=True)

    # Inputs with spacing and emoji
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        age = st.number_input('📅 Age (Years)', min_value=0, max_value=18, value=5)
        height = st.number_input('📏 Current Height (cm)', min_value=50, max_value=200, value=100)
        weight = st.number_input('⚖️ Current Weight (kg)', min_value=5, max_value=100, value=20)
        gender = st.selectbox('🚻 Gender', ['Male', 'Female'])
        st.markdown('</div>', unsafe_allow_html=True)


    bmi = weight / (height / 100) ** 2
    bmi_status = bmi_category(bmi)

    if st.sidebar.button('🔍 Predict Growth'):
        input_data = pd.DataFrame({'age': [age], 'height': [height], 'weight': [weight], 'BMI': [bmi]})
        predicted_height = model.predict(input_data)[0]

        # Display Results
        st.markdown(f"### 📐 **Predicted Height at Age {age + 1}:** `{predicted_height:.2f} cm`")
        st.markdown(f"### 🧮 **BMI:** `{bmi:.2f}`  |  **Status:** `{bmi_status}`")

        # Growth Message
        alert_message = check_growth_abnormality(predicted_height, age, gender)

        if "Abnormal" in alert_message or "❌" in alert_message:
            st.markdown(f'<div class="alert">{alert_message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="normal">{alert_message}</div>', unsafe_allow_html=True)

        # Plotly Chart
        fig = go.Figure()

                # Predicted height marker
        fig.add_trace(go.Scatter(
            x=[age],
            y=[predicted_height],
            mode='markers+text',
            name='Predicted Height',
            marker=dict(color='red', size=14),
            text=[f'{predicted_height:.2f} cm'],
            textposition='top center'
        ))

        fig.update_layout(
            title="📉 Growth Comparison Chart",
            xaxis_title="Age (Years)",
            yaxis_title="Height (cm)",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Use the function to get the expected height range
        min_height, max_height = calculate_expected_height_range(age, gender)

        if min_height is not None and max_height is not None:
            fig.add_trace(go.Scatter(
                x=[age, age],
                y=[min_height, max_height],
                mode='lines',
                name='Expected Height Range',
                line=dict(color='royalblue', dash='dot')
            ))

        # Optional: Display gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=predicted_height,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Predicted Height (cm)"},
            delta={'reference': height},
            gauge={
                'axis': {'range': [height - 20, height + 20]},
                'bar': {'color': "#28a745"},
                'steps': [
                    {'range': [height - 20, height], 'color': "#ffc107"},
                    {'range': [height, height + 20], 'color': "#17a2b8"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': predicted_height
                }
            }
        ))
        st.plotly_chart(fig)

# Run the app
if __name__ == "__main__":
    main()
