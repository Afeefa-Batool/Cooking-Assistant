import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io
import os

# Page Config
st.set_page_config(
    page_title="AI Cooking Assistant",
    page_icon="🍳",
    layout="centered"
)

# Title
st.title("🍳 AI Cooking Assistant")
st.write("Upload ingredients image and get recipe suggestions")

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Please add GROQ_API_KEY in Hugging Face Secrets")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)


# Convert Image to Base64
def image_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


# File Uploader
uploaded_file = st.file_uploader(
    "Upload Image of Ingredients",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    # Show Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("🍽️ Generate Recipe"):

        with st.spinner("Analyzing ingredients..."):

            # Convert image
            img_base64 = image_to_base64(image)

            # Prompt
            prompt = """
            You are a professional chef AI.
            Look at the image and identify ingredients.
            Then suggest:
            1. Dish name
            2. Ingredients list
            3. Step-by-step recipe
            4. Cooking tips
            """

            # Call LLaMA Vision Model
            response = client.chat.completions.create(
# model="llama-3.2-90b-vision-preview",
               model = "meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800
            )

            result = response.choices[0].message.content

            # Display Output
            st.subheader("🍲 Suggested Recipe")
            st.write(result)
