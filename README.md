🕷️ Challenge Alura - Parker IA Agent (Oaxaca)

Desplegado en OCI en la siguiente dirección: http://159.54.139.0:8501/

🚀 1. Descripción General
Parker IA Agent permite a los usuarios mediantes lenguaje natural para consultar agendas de viajes,cotizaciones y detalles sobre politicas generales, es un agente que da información sobre viajes en el basto estado de Oaxaca México.

Para evitar problemas de alucinación comunes en los modelos de lenguaje tradicionales, el proyecto implementa una arquitectura RAG (Retrieval-Augmented Generation), asegurando respuestas verídicas y contextualizadas.

🏗️ 2. Arquitectura de la Solución
1.- Proceamiento de documentos: Extrae de manera estructurada los archivos en formato PDF con la herramienta pypdf
2.- Base de datos Vectorial: Los bloques de texto se convierten en vectores para posteriormente almacenarlos en FAISS
3.-Orquestación y respuestas: Se captura la pregunta del usuario, FAISS recuera el contexto más importamte y la API de Google Gemini da una respuesta en lenguaje natural

🛠️ 3. Tecnologías y Herramientas usadas
**Lenguaje de programación**: Python 3 para el desarrollo de la lógica
**Frontned**: Streamlit
**LLM**: Google gemini API especificamente gemini-2.5-flash
**Vector DB**: Faiss
**Procesamiento de documentos**: PYPDF,libreria de Python
**Embeddings**: HuggingFace
**Cloud Hosting**:OCI (Oracle Cloud)

💻 4. Guía de Instalación y Ejecución

**ENTORNO**
1.- Crear la carpeta raiz en mis documentos, en esta guarde los archivos PDF, la imagen para el frontend
2.-Abri mi carpeta en vs code con el comando open file
3.- Cree el repositorio de git hub y lo clone con el comando git clone

**CREDENCIALES DE GEMINI API KEY**
1.-Para guardar la contraseña del API cree un archivo llamado .env, donde guarde la contraseña
2.- Para mandar a llamar la API Key de Gemini lo hice con el comando: load_dotenv()

**Instalación de dependencias**
Estos fueron los comandos que use para instalar las dependencias
!pip install --upgrade langchain-google-genai==1.0.8 google-generativeai==0.7.2 -q
!pip install langchain-community==0.2.10 langchain-text-splitters sentence-transformers faiss-cpu -q
Como tenia un entorno virtual para app.py tuve que instalar las dependencias de nuevo desde la terminal

**Ejecución**
Después de esos pasos primero hice las pruebas en mi archivo ipynb y después migre todo a app.py para poder correr streamlit, el cual lo corres con el comando: streamlit run app.py

**Despliegue en OCI**
Por último desplegue mi proyecto en la nube de oracle, cree una instancia, la configure con la dirección que daba y la desplegue de forma permamente, claro que en la terminal de oracle también tuve que instalar las dependencias

5. Ejemplos de interacción del agente
"Hay alguna politica de descuentos?"
Respuesta:
🤖 AGENTE PARKER:

Sí, tenemos políticas de descuentos especiales. Ofrecemos tarifas preferenciales bajo los siguientes criterios, que no son acumulables:

*   **Grupos:** 10% de descuento automático a partir de 8 adultos reservados juntos.
*   **Adultos Mayores:** 15% de descuento presentando credencial vigente de INAPAM (aplica solo en tours de un día).

"Cuáles son los precios de los paquetes de tours?"
Respuesta:
🤖 AGENTE PARKER:

Tenemos dos paquetes completos:

*   El Paquete "Oaxaca Express" (3 Días / 2 Noches) tiene un precio de $5,800 MXN por persona en ocupación doble.
*   El Paquete "Aventura y Tradición" (5 Días / 4 Noches) tiene un precio de $11,200 MXN por persona en ocupación doble.

ADICIONAL: Se hzo una prueba para probar al agente preguntando quien es Leo Messi, a lo que responde:
🤖 AGENTE PARKER:

No tengo esa información

6. Evidencia de funcionamiento en OCI
<img width="942" height="927" alt="image" src="https://github.com/user-attachments/assets/923dd8d1-0264-41e3-a200-bb7ba5b3593e" />

<img width="815" height="788" alt="image" src="https://github.com/user-attachments/assets/e6813231-ee7e-46c9-8eb2-c355f08dfd93" />

<img width="1608" height="797" alt="image" src="https://github.com/user-attachments/assets/c7a57509-917e-4966-b8e5-95be44fa7025" />





