import faiss
from phi.agent import Agent
from phi.model.groq import Groq
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain.docstore import InMemoryDocstore
from transformers import AutoTokenizer
import gradio as gr
import warnings
from langchain.prompts import PromptTemplate
import os
import dotenv
dotenv.load_dotenv()

# Initialize Groq
groq_agent = Agent(
    model=Groq(id="llama-3.3-70B-versatile")
)

# Define the Aristotle prompt template
ARISTOTLE_SYSTEM_PROMPT = """You are Aristotle, the great philosopher from Ancient Greece. 
            You should respond in a wise, philosophical tone, using phrases like 'O wise one,' and incorporate historical wisdom.
            Analyze the provided context and question carefully, then respond as Aristotle would.

            Context:
            {context}

            Question:
            {question}

            Respond as Aristotle, maintaining a philosophical and wise tone throughout your answer. Dont speak too much, because the wise never do. to explain a student, if he or she is wise, a action is enough. O wise one! dont be boring, bitch.
            no shit talks. make the conversation simple
            """

# Initialize tokenizer and other components
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
dim = 384
index = faiss.IndexFlatL2(dim)

def preprocess_query(query):
    """Preprocess the query to add Aristotelian flair."""
    if not query or not isinstance(query, str):
        return "What wisdom do you seek, O curious one?"
    return f"O wise one, {query.strip().capitalize()}? Please share your wisdom."

def process_pdf(pdf):
    """Process PDF and extract text chunks."""
    pdf_reader = PdfReader(pdf)
    raw_text = ''
    
    for page in pdf_reader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    
    return [Document(page_content=text, metadata={"source": f"chunk_{i}"}) for i, text in enumerate(texts)]

pdf_file="for-llama-aristotle.pdf"

def output(query):
    try:
        if not query or not query.strip():
            return "O seeker of knowledge, please pose a question for contemplation."

        if not os.path.exists(pdf_file):
            return "Alas, the sacred scroll (PDF file) cannot be found. Please check the path in your .env file."

        with open(pdf_file, 'rb') as file:
            # Process query and documents
            processed_query = preprocess_query(query.strip())
            documents = process_pdf(file)
            
            # Set up FAISS
            docstore = InMemoryDocstore({i: doc for i, doc in enumerate(documents)})
            index_to_docstore_id = {i: i for i in range(len(documents))}
            faiss_store = FAISS(
                index=index,
                embedding_function=embeddings_model,
                docstore=docstore,
                index_to_docstore_id=index_to_docstore_id
            )
            faiss_store.add_documents(documents)
            
            # Get relevant documents
            docs = faiss_store.similarity_search(processed_query, k=2)
            
            if not docs:
                return "O wise one, I regret to inform you that no relevant scrolls were found..."
            
            # Prepare context from relevant documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Format prompt for Groq
            formatted_prompt = ARISTOTLE_SYSTEM_PROMPT.format(
                context=context,
                question=processed_query
            )
            
            # Get response from Groq and extract only the content
            response = groq_agent.run(formatted_prompt)
            
            # Extract just the content from the response
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, str):
                return response
            elif hasattr(response, '__str__'):
                # If it's an object with a string representation
                return str(response).split("content='")[1].split("'")[0]
            else:
                return "Alas, I could not format the response properly."

    except Exception as e:
        return f"Alas, an error has befallen us: {str(e)}"
    
    
# Create Gradio interface
app = gr.Interface(
    fn=output,
    inputs=[gr.Textbox(lines=2, label="Chat with Aristotle")],
    outputs="text",
    title="Ask Aristotle",
    description="Seeking wisdom? dont worry! Aristotle is here!",
    examples=[
        ["What is the nature of wisdom?"],
        ["How should one pursue knowledge?"]
    ],
    theme="default"
)

if __name__ == "__main__":
    app.launch()
