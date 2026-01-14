import fitz
from dotenv import load_dotenv
 
from langchain_huggingface  import HuggingFaceEndpoint,ChatHuggingFace

load_dotenv()

#-------------------------------CHAT MODEL SETUP------------------------------------
llm=HuggingFaceEndpoint(
    repo_id='mistralai/Mistral-7B-Instruct-v0.2',
    task='text-generation'
)
model=ChatHuggingFace(llm=llm)
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def ask_openai(prompt):
    """
    Send prompt to Gemini and return response
    """
    response = model.invoke(prompt)
    return response.content
