import streamlit as st
import numpy as np
import pandas as pd
import pickle
import plotly.express as px
from PIL import Image
import json
import os

from profile_page import show_profile

from login_utils import authenticate, login_user, logout_user, get_current_user, register_user

# Page configuration
st.set_page_config(layout="wide")

# Custom CSS to change sidebar background color
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: 	#578FCA; /* 👈 تغییر رنگ سایدبار اینجاست */
        }
    </style>
""", unsafe_allow_html=True)

# بررسی وضعیت ورود
user = get_current_user()

if user is None:
    st.title("🔐 Authentication")

    auth_choice = st.radio("Select Action", ["Login", "Register"])

    if auth_choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            auth_user = authenticate(username, password)
            if auth_user:
                login_user(auth_user)
                st.success(f"Welcome, {auth_user['username']}! Please refresh the page.")
            else:
                st.error("Invalid username or password.")

    elif auth_choice == "Register":
        with st.form("register_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            submitted_register = st.form_submit_button("Register")

        if submitted_register:
            if not new_username or not new_password:
                st.warning("Please fill in both fields.")
            else:
                success = register_user(new_username, new_password)
                if success:
                    st.success("Registration successful. Please log in.")
                else:
                    st.error("Username already exists.")

    st.stop()
    if user['role'] == 'admin':
        # Show admin-specific UI or controls
        st.sidebar.markdown("### Admin Panel")
        if st.sidebar.button("View All Prediction History"):
            # Load and show all users' prediction history
            with open("prediction_history.json", "r") as f:
                history = json.load(f)
            st.write(history)

        # You could add more admin controls here

    else:
        # Normal user UI
        st.sidebar.markdown(f"Welcome, {user['username'].capitalize()}!")


else:
    with st.sidebar:
        with st.container():
            st.markdown("""
                <style>
                    .profile-box {{
                        background-color: #f7f7f7;
                        padding: 12px 16px;
                        border-radius: 12px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        margin-bottom: 15px;
                    }}
                    .username-role {{
                        display: flex;
                        align-items: center;
                        margin-bottom: 12px;
                    }}
                    .username-role-icon {{
                        font-size: 32px;
                    }}
                    .username-role-text {{
                        font-size: 16px;
                        padding-left: 10%;
                    }}
                </style>
                <div class="profile-box">
                    <div class="username-role">
                        <div class="username-role-icon">🙍🏻‍♂️</div>
                        <div class="username-role-text">
                            <strong>{}</strong><br>
                            <span style="color: gray; font-size: 13px;">Role: {}</span>
                        </div>
                    </div>
            """.format(user['username'].capitalize(), user['role'].capitalize()), unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Profile"):
                    st.session_state["page"] = "profile"
            with col2:
                if st.button("🚪 Logout"):
                    logout_user()
                    st.success("You have been logged out.")
                    st.stop()

            st.markdown("</div>", unsafe_allow_html=True)

# Handle profile page routing
if "page" not in st.session_state:
    st.session_state["page"] = "main"

if st.session_state["page"] == "profile":
    show_profile(user)
    st.stop()


# --- تابع برای خواندن کاربر لاگین‌شده از فایل ---
def load_current_user():
    if os.path.exists("current_user.json"):
        try:
            with open("current_user.json", "r") as f:
                data = json.load(f)
                return data.get("username"), data.get("role")
        except json.JSONDecodeError:
            return None, None
    return None, None

# --- استفاده در بالای main.py ---
username, role = load_current_user()

if not username or not role:
    st.warning("No user is logged in. Please log in first using the authentication app.")
    st.stop()

# Load your pre-trained model
with open('linear_model.pkl', 'rb') as f:
    lm2 = pickle.load(f)

# Load feature importance from an Excel file
def load_feature_importance(file_path):
    return pd.read_excel(file_path)

# Load the feature importance DataFrame
final_fi = load_feature_importance("feature_importance.xlsx")  # Replace with your file path

# Sidebar setup
image_sidebar = Image.open('images/Pic 1.jpg')  # Replace with your image file
st.sidebar.image(image_sidebar, use_container_width=True)
st.sidebar.header('Vehicle Features')

# Feature selection on sidebar
def get_user_input():
    horsepower = st.sidebar.number_input('Horsepower (No)', min_value=0, max_value=1000, step=1, value=300)
    torque = st.sidebar.number_input('Torque (No)', min_value=0, max_value=1500, step=1, value=400)
    
    make = st.sidebar.selectbox('Make', ['Aston Martin', 'Audi', 'BMW', 'Bentley', 'Ford', 'Mercedes-Benz', 'Nissan'])
    body_size = st.sidebar.selectbox('Body Size', ['Compact', 'Large', 'Midsize'])
    body_style = st.sidebar.selectbox('Body Style', [
        'Cargo Minivan', 'Cargo Van', 'Convertible', 'Convertible SUV', 'Coupe', 'Hatchback', 
        'Passenger Minivan', 'Passenger Van', 'Pickup Truck', 'SUV', 'Sedan', 'Wagon'
    ])
    engine_aspiration = st.sidebar.selectbox('Engine Aspiration', [
        'Electric Motor', 'Naturally Aspirated', 'Supercharged', 'Turbocharged', 'Twin-Turbo', 'Twincharged'
    ])
    drivetrain = st.sidebar.selectbox('Drivetrain', ['4WD', 'AWD', 'FWD', 'RWD'])
    transmission = st.sidebar.selectbox('Transmission', ['automatic', 'manual'])
    
    user_data = {
        'Horsepower_No': horsepower,
        'Torque_No': torque,
        f'Make_{make}': 1,
        f'Body Size_{body_size}': 1,
        f'Body Style_{body_style}': 1,
        f'Engine Aspiration_{engine_aspiration}': 1,
        f'Drivetrain_{drivetrain}': 1,
        f'Transmission_{transmission}': 1,
    }
    return user_data

# Top banner
image_banner = Image.open('images/Pic 2.png')  # Replace with your image file
st.image(image_banner,use_container_width=True)

# Centered title
st.markdown("<h1 style='text-align: center;'>Car Price Prediction App</h1>", unsafe_allow_html=True)

# Split layout into two columns
left_col, right_col = st.columns(2)

# Left column: Feature Importance Interactive Bar Chart
with left_col:
    st.header("Feature Importance")
    
    # Sort feature importance DataFrame by 'Feature Importance Score'
    final_fi_sorted = final_fi.sort_values(by='Feature Importance Score', ascending=True)
    
    # Create interactive bar chart with Plotly
    fig = px.bar(
        final_fi_sorted,
        x='Feature Importance Score',
        y='Variable',
        orientation='h',
        title="Feature Importance",
        labels={'Feature Importance Score': 'Importance', 'Variable': 'Feature'},
        text='Feature Importance Score',
        color_discrete_sequence=["#3674B5"]  # Custom bar color
    )
    fig.update_layout(
        xaxis_title="Feature Importance Score",
        yaxis_title="Variable",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Right column: Prediction Interface
with right_col:
    st.header("Predict Vehicle Price")
    
    # User inputs from sidebar
    user_data = get_user_input()

    # Transform the input into the required format
    def prepare_input(data, feature_list):
        input_data = {feature: data.get(feature, 0) for feature in feature_list}
        return np.array([list(input_data.values())])

    # Feature list (same order as used during model training)
    features = [
        'Horsepower_No', 'Torque_No', 'Make_Aston Martin', 'Make_Audi', 'Make_BMW', 'Make_Bentley',
        'Make_Ford', 'Make_Mercedes-Benz', 'Make_Nissan', 'Body Size_Compact', 'Body Size_Large',
        'Body Size_Midsize', 'Body Style_Cargo Minivan', 'Body Style_Cargo Van', 
        'Body Style_Convertible', 'Body Style_Convertible SUV', 'Body Style_Coupe', 
        'Body Style_Hatchback', 'Body Style_Passenger Minivan', 'Body Style_Passenger Van',
        'Body Style_Pickup Truck', 'Body Style_SUV', 'Body Style_Sedan', 'Body Style_Wagon',
        'Engine Aspiration_Electric Motor', 'Engine Aspiration_Naturally Aspirated',
        'Engine Aspiration_Supercharged', 'Engine Aspiration_Turbocharged',
        'Engine Aspiration_Twin-Turbo', 'Engine Aspiration_Twincharged', 
        'Drivetrain_4WD', 'Drivetrain_AWD', 'Drivetrain_FWD', 'Drivetrain_RWD', 
        'Transmission_automatic', 'Transmission_manual'
    ]

    # Predict button
    if st.button("Predict"):
        input_array = prepare_input(user_data, features)
        prediction = lm2.predict(input_array)
        
        st.subheader("Predicted Price")
        st.write(f"${prediction[0]:,.2f}")

        # --- Save prediction to history ---
        log_entry = {
            "username": user["username"],
            "input": user_data,
            "predicted_price": round(float(prediction[0]), 2)
        }

        history_file = "prediction_history.json"
        
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        else:
            history = []

        history.append(log_entry)

        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)


# streamlit run main.py
