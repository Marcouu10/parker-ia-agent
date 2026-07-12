#se cargan todas las librerias necesarias para el funcionamiento del proyecto
import streamlit as st
#import os

#from dotenv import load_dotenv
#from langchain_community.document_loaders import PyPDFLoader
#from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain_community.vectorstores import FAISS
#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.chains import create_stuff_documents_chain
#from langchain_core.prompts import ChatPromptTemplate


#cargar las credenciales del archivo .env

#configuración basica de la pagina web
st.set_page_config(page_title="Agente Parker", page_icon="🕷️"  )
st.title("🕷️ Agente de viajes Parker")
st.write("Bienvenido al agente de viajes Parker, tu asistente virtual para planificar tus aventuras. Parker está diseñado para ayudarte a encontrar información sobre nuestros paquetes de viaje, destinos y servicios. Simplemente ingresa tu consulta y Parker te proporcionará respuestas precisas y útiles.")