import streamlit as st
import pandas as pd
import joblib
from PIL import Image
from pymongo import MongoClient

# Function to load the model
@st.cache_data
def load_model():
    with open('calories_model', 'rb') as file:
        loaded_model = joblib.load(file)
    return loaded_model

# Load your model
loaded_model = load_model()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")  # Local MongoDB connection
db = client['calorie_burn_db']  # Replace with your database name
feedback_collection = db['feedback']  # Feedback collection

# Ensure the database and collection are created
# if not feedback_collection.find_one():  # Check if the collection is empty
#     feedback_collection.insert_one({"name": "Test", "email": "test@example.com", "feedback_type": "General", "feedback_message": "Initial test feedback"})


# Add custom CSS and a background image
st.markdown(
    f"""
    <style>
        body {{
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Arial', sans-serif;
            height: 100vh;
            margin: 0;
            padding: 0;
        }}
        .main-heading {{
            font-size: 3rem;
            font-weight: bold;
            color: #FFA500;
            text-align: center;
            text-shadow: 2px 2px 5px #000000;
            margin-top: 20px;
        }}
        .subheading {{
            font-size: 1.5rem;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 20px;
            animation: fade-in 2s ease-in-out;
        }}
        @keyframes fade-in {{
            from {{opacity: 0;}}
            to {{opacity: 1;}}
        }}
        .sidebar-title {{
            font-weight: bold;
            color: #FFA500;
        }}
        .prediction {{
            font-size: 1.5rem;
            color: #FFFFFF;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px;
            border-radius: 10px;
        }}
    </style>
    """, 
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.markdown('<span class="sidebar-title">Navigation</span>', unsafe_allow_html=True)
options = st.sidebar.selectbox('Select a page:', ['Home', 'Prediction', 'Contact'])

# Home Page
if options == 'Home':
    st.markdown('<div class="main-heading">Smart Calorie Burn Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheading">Welcome to the Smart Calorie Burn Analyzer App!</div>', unsafe_allow_html=True)
    st.write("This app helps you predict the calories burned during physical activities based on your personal inputs like age, weight, height, gender, heart rate, and activity duration.")
    image = Image.open('home2.jpg')  # Adjust the path if needed
    st.image(image, caption='Welcome to the Calorie Burn Prediction App', use_container_width=True)

    st.write("### How it works:")
    st.write("1. Enter your personal details and activity information.")
    st.write("2. Click on 'Predict' to calculate the calories burned.")
    st.write("3. Use the result to track your fitness goals and monitor your progress.")
    image = Image.open('home3.webp')  # Adjust the path if needed
    st.image(image, caption='Welcome to the Calorie Burn Prediction App', use_container_width=True)

# Prediction Page
elif options == 'Prediction':
    st.markdown('<div class="main-heading">Smart Calorie Burn Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheading">Predict your calories burned based on your inputs</div>', unsafe_allow_html=True)

    # User inputs
    gender = st.selectbox('Gender', ['Male', 'Female'])
    age = st.number_input('Age', 1, 100, 25)
    height = st.number_input('Height in cm', 100, 250, 170)
    weight = st.number_input('Weight in kg', 30, 200, 70)
    duration = st.number_input('Duration in minutes', 1, 180, 60)
    heart_rate = st.number_input('Heart Rate', 60, 200, 100)
    body_temp = st.number_input('Body Temperature in Celsius', 35.0, 43.0, 37.0)

    user_inputs = {
        'gender': 0 if gender == 'Male' else 1,
        'age': age,
        'height': height,
        'weight': weight,
        'duration': duration,
        'heart_rate': heart_rate,
        'body_temp': body_temp
    }

    if st.button('Predict'):
        prediction = loaded_model.predict(pd.DataFrame(user_inputs, index=[0]))
        st.markdown(
            f'<div class="prediction">The predicted Calories Burnt is: <strong>{prediction[0]:,.2f}</strong></div>',
            unsafe_allow_html=True
        )

# Contact Page
elif options == 'Contact':
    st.markdown('<div class="main-heading">Contact Us</div>', unsafe_allow_html=True)
    st.write('We would love to hear from you! Whether you have feedback, questions, or need support, feel free to get in touch with us.')

    # Feedback Form
    st.write('### Feedback Form:')
    name = st.text_input('Name')
    email = st.text_input('Email')
    feedback_type = st.selectbox('Feedback Type', ['General', 'Bug Report', 'Feature Request'])
    feedback_message = st.text_area('Feedback Message')

    if st.button('Submit Feedback'):
        if name and email and feedback_message:
            feedback_data = {
                'name': name,
                'email': email,
                'feedback_type': feedback_type,
                'feedback_message': feedback_message
            }
            try:
                feedback_collection.insert_one(feedback_data)
                st.success("Thank you for your feedback! It has been saved.")
            except Exception as e:
                st.error(f"Failed to save feedback: {e}")
        else:
            st.error("Please fill in all fields before submitting.")

    # Display existing feedback
    st.write('### Recent Feedback:')
    try:
        feedbacks = feedback_collection.find().sort('_id', -1).limit(5)
        for feedback in feedbacks:
            st.write(f"**Name:** {feedback['name']}")
            st.write(f"**Type:** {feedback['feedback_type']}")
            st.write(f"**Message:** {feedback['feedback_message']}")
            st.write("---")
    except Exception as e:
        st.error(f"Failed to retrieve feedback: {e}")
    image = Image.open('contact.webp')  # Adjust the path if needed
    st.image(image, caption='Welcome to the Calorie Burn Prediction App', use_container_width=True)
