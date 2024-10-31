import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Cargar el archivo .env para obtener la API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Función para hacer la solicitud a la API de OpenAI
def openai_request(prompt):
    if not api_key:
        raise ValueError("API key is missing. Please add your OpenAI API key in the .env file.")
    
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'prompt': prompt,
        'model': 'dall-e-3',
        'size': '1792x1024',
        'n': 1
    }

    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        st.error(f"Error generating image: {response.status_code} - {response.json().get('error', {}).get('message', 'Unknown error')}")
        return None
    else:
        image_url = response.json()['data'][0]['url']
        return image_url

# Función para descargar la imagen generada
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Configuración de la aplicación de Streamlit
st.set_page_config(page_title="AI Image Generator by Emanuel Diaz", page_icon="🤖", layout="centered")

# Elementos de la interfaz de usuario
st.image("images/full.jpg", use_column_width=True)
st.title("AI Image Generator by Emanuel Diaz")
description = st.text_area("Prompt")

# Botón para generar imagen
if st.button("Generate Image"):
    if description.strip() == "":
        st.error("Please enter a description for the image.")
    else:
        with st.spinner("Generating your image..."):
            url = openai_request(description)
            if url:
                filename = "AI_images/image_generator.png"
                download_image(url, filename)
                st.image(filename, use_column_width=True)
                with open(filename, "rb") as f:
                    image_data = f.read()
                st.download_button(label="Download Image", data=image_data, file_name="image_generated.jpg")



    
    
