import streamlit as st
import os
from streamlit_extras.app_logo import add_logo
from dotenv import load_dotenv


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import Dict

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del navegador (Título e ícono de la pestaña)
st.set_page_config(page_title="Agente de viajes Parker 🕷️", page_icon="🕷️")

st.title("🕷️ Agente de viajes en Oaxaca Parker")
st.write("Bienvenido al agente de viajes Parker, tu asistente virtual para planificar tus aventuras en el bello estado de Oaxaca México. Parker está diseñado para ayudarte a encontrar información sobre nuestros paquetes de viaje, destinos y servicios. Simplemente ingresa tu consulta y Parker te proporcionará respuestas precisas y útiles.")

st.image("Oaxaca.jpg", use_container_width=True)

# st.markdown(
#     """
#     <style>
#     [data-testid="stAppViewContainer"] {
#         background-image: linear-gradient(rgba(14, 17, 23, 0.85), rgba(14, 17, 23, 0.85)), 
#                           url("https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Oaxaca_en_la_noche.jpg/1200px-Oaxaca_en_la_noche.jpg");
#         background-size: cover !important;
#         background-position: center !important;
#         background-attachment: fixed !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# Configuración del rag

@st.cache_resource
def inicializar_agente_y_datos():
    # Inicializar tu LLM con Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0, 
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )
    
    # Lista  de archivos PDF 
    archvivos_pdf = [
        "parker_itinerarios_tours.pdf",
        "parker_politicas_empresa.pdf",
        "parker_precios_paquetes.pdf",
        "parker_preguntas_frecuentes.pdf"
    ]
    
    # Carga de archivos
    docs = []
    for file in archvivos_pdf:
        loader = PyPDFLoader(file)
        docs.extend(loader.load())
        
    # Limpiar los documentos eliminando saltos de línea y espacios innecesarios
    clean_docs = [
        Document(
            page_content=" ".join(doc.page_content.replace("-","-").split()),
            metadata=doc.metadata
        )
        for doc in docs
    ]
    
    # Dividir los documentos en fragmentos más pequeños para mejorar la recuperación de información
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1300,
        chunk_overlap=200
    )
    documents = text_splitter.split_documents(clean_docs)
    
    # Inicializar Embeddings de HuggingFace y la base vectorial FAISS
    model_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ) 
    vectorstore = FAISS.from_documents(documents, model_embeddings)
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5},
        search_type="similarity"
    )
    
    #  Prompt para el RAG (Recuperación Augmentada de Generación)
    prompt_rag = ChatPromptTemplate.from_messages([
        ("system", """
Eres el especialista de la empresa Parker la cual es una agencia de turismo en Oaxaca.
Responde de forma clara, natural y sutil usando SOLO el contecto proporcionado

Reglas:
- Si hay información relevante, responde con ella
- Si la información es parcial, responde lo que sí se sabe
- Si no hay nada relevante, di "No tengo esa información"
- No inventes nada
"""),
        ("human", "Contexto:{context}\nPregunta del empleado:{input}")
    ])
    
    # Crear la cadena de combinación de documentos
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_rag)
    
    return retriever, document_chain

# Arrancamos los motores del agente 
retriever, document_chain = inicializar_agente_y_datos()


# Función para buscar respuestas a partir de la pregunta del usuario
def busqueda_de_respuestas(pregunta: str) -> Dict:
    # Se buscan los documentos relacionados con la pregunta
    related_docs = retriever.invoke(pregunta)

    # Si no hay documentos relacionados, se devuelve el mensaje por defecto
    if not related_docs:
        return {"respuesta": "No tengo esa información",
                "documentos_relacionados": [],
                "documentos_encontrados": False}

    # Se genera la respuesta con la cadena y los documentos encontrados
    answer = document_chain.invoke({
        "input": pregunta, 
        "context": related_docs
    })

    if answer.rstrip(".!?") == "No tengo esa información":
        return {
            "respuesta": "No tengo esa información",
            "citaciones": [],
            "documentos_encontrados": False
        }
    
    return {"respuesta": answer,
            "documentos_relacionados": related_docs,
            "documentos_encontrados": True}
    
st.markdown("### 📌 Preguntas Frecuentes ")
col_a, col_b, col_c = st.columns(3)

pregunta_a_ejecutar = None

with col_a:
    if st.button("📋 ¿Cuáles son las políticas?"):
        pregunta_a_ejecutar = "cuales son las politicas de la empresa?"
with col_b:
    if st.button("💰 ¿Precios de paquetes?"):
        pregunta_a_ejecutar = "Cuáles son los precios de los paquetes de tours?"
with col_c:
    if st.button("🗺️ ¿Itinerarios disponibles?"):
        pregunta_a_ejecutar = "Cuáles son los itinerarios de los tours?"

st.write("---")

pregunta_usuario = st.text_input("Haz tu pregunta aquí:", placeholder="¿Cuáles son los precios de los paquetes de tours?")

# Si la caja tiene texto y el usuario presiona Enter, se dispara el agente
if pregunta_usuario:
    pregunta_a_ejecutar = pregunta_usuario
    # Bloque visual de carga (Spinner)
if pregunta_a_ejecutar:
    with st.spinner("Buscando respuestas..."):
        
        resultado = busqueda_de_respuestas(pregunta_a_ejecutar)

    st.markdown("#### 🤖 AGENTE PARKER:")
    st.markdown(resultado['respuesta'])
    # st.markdown(f"### 💬 Tu pregunta: *{pregunta_a_ejecutar}*")
    # st.success(f"**🤖 AGENTE PARKER:**\n\n{resultado['respuesta']}")
      
       

