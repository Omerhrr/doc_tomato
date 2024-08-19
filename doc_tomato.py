import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import requests
from io import BytesIO

# Configure the page
st.set_page_config(page_title="Doctor Tomato", page_icon="🍅", layout="wide")

# Configure the Google Gemini API
genai.configure(api_key='AIzaSyDrsZmufmokYwsxK5MLypkdSB6SPdioHAo')

# Set up the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to analyze image
def analyze_image(image):
    response = model.generate_content([
        "Analyze this image and identify if there's any pest or disease affecting the tomato plant. If a pest or disease is detected, provide its name, the organism that caused it, description, and mitigation steps. If it's not a tomato plant, respond with 'This model only targets tomato pests'. Include any other relevant information about factors affecting tomatoes. **Note: be sure, precise and accurate, stick to your answer**",
        image
    ])
    return response.text

# Function to get pest image
def get_pest_image(pest_name):
    response = requests.get(f"https://api.unsplash.com/search/photos?query={pest_name}&client_id={os.getenv('i-bk4-m6en_gNF3TqByHRycaE3iq0_UMU7YUIsb7SGI')}")
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['small']
    return None

# Custom CSS for styling
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Sidebar for theme toggle
st.sidebar.title("Settings")
if st.sidebar.checkbox("Dark Mode"):
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
st.title("🍅 Doctor Tomato")
st.subheader("Upload an image of your tomato plant for pest and disease analysis")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Analyze"):
        with st.spinner("Analyzing image..."):
            result = analyze_image(image)
        
        st.subheader("Analysis Result")
        st.write(result)
        
        # Check if a pest was detected and display its image
        if "This model only targets tomato pests" not in result:
            pest_name = result.split('\n')[0]  # Assume the first line contains the pest name
            pest_image_url = get_pest_image(pest_name)
            if pest_image_url:
                response = requests.get(pest_image_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=f"Image of {pest_name}", use_column_width=True)

# Additional information section
st.markdown("---")
st.header("About Doctor Tomato")
st.write("""
Doctor Tomato is your go-to tool for identifying pests and diseases affecting your tomato plants. 
Simply upload an image of your plant, and our AI-powered system will analyze it to provide you with 
valuable insights and mitigation strategies.

Remember, early detection is key to maintaining a healthy tomato crop!
""")

# Tips section
st.markdown("---")
st.header("Tomato Care Tips")
st.write("""
1. Water deeply and regularly, especially during fruit set and development.
2. Provide support for your plants with stakes or cages.
3. Prune suckers to promote better air circulation and fruit development.
4. Monitor for pests regularly and address issues promptly.
5. Fertilize with a balanced, tomato-specific fertilizer.
""")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Doctor Tomato Team")