
import streamlit as st
st.set_page_config(page_title="University Academic Policy Chatbot", layout="centered")

from dotenv import load_dotenv

# Import LangChain components
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Import your custom utility functions and configurations

from config import TOP_K_RETRIEVAL
from utils import get_vector_store, get_llm_for_rag

# Initialization
# Load environment variables from .env file
load_dotenv()




@st.cache_resource  # This decorator caches the return value of the function
def initialize_chatbot_components():
    """Initializes the vector store and LLM chain globally, and caches them."""
    print("Initializing components for the Academic Policy Chatbot...")

    try:
        # Load the existing vector store
        vector_store = get_vector_store()
        print("Vector store loaded.")

        # Initialize the LLM which will be Groq via API
        llm = get_llm_for_rag()
        print("LLM initialized.")

        # prompt template for the RAG chain
        template = """You are an intelligent Academic Policy Assistant for a university.
        Your task is to answer student questions based solely on the provided context from the university's academic manual.
        Be concise, accurate, and directly address the student's question.
        If the answer is not explicitly available in the provided context, state that you cannot find the answer in the document and suggest they contact the academic advising office.
        Do not make up information.

        Context:
        {context}

        Question: {question}

        Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Creating the RetrievalQA chain
        llm_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": TOP_K_RETRIEVAL}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
        print("Chatbot components initialized successfully!")
        return llm_chain  # Return the initialized chain

    except Exception as e:
        st.error(f"Error during chatbot initialization: {e}. Please check your API keys and configuration.")
        print(f"FATAL ERROR during chatbot initialization: {e}")
        return None


# Initialize the chatbot components cached by Streamlit
if 'llm_chain' not in st.session_state:
    st.session_state.llm_chain = initialize_chatbot_components()

#  Streamlit UI Layout
st.title("📚 University Academic Policy Chatbot")
st.markdown(
    "Ask questions about the university's academic policies and get answers directly from the academic manual. Powered by Groq.")

# Text input for user query
user_query = st.text_area("Your Question:", placeholder="e.g., What is the policy for withdrawing from a course?",
                          height=100)

if st.button("Get Answer"):
    if st.session_state.llm_chain is None:
        st.error("Chatbot is not ready. Please ensure your environment is set up correctly and restart the app.")
    elif not user_query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Fetching answer..."):
            try:
                # Invoke the RAG chain
                result = st.session_state.llm_chain.invoke({"query": user_query})

                answer = result["result"]
                source_documents = result.get("source_documents", [])

                st.subheader("Answer:")
                st.write(answer)

                if source_documents:
                    st.subheader("Sources:")
                    for i, doc in enumerate(source_documents):
                        st.markdown(
                            f"**{i + 1}. Page {doc.metadata.get('page', 'N/A')}**, Source: `{doc.metadata.get('source', 'Academic Manual')}`")
                        # Truncate content for display
                        source_content_snippet = doc.page_content.strip()
                        if len(source_content_snippet) > 300:
                            source_content_snippet = source_content_snippet[:300] + "..."
                        st.code(source_content_snippet, language='text')  # Use st.code for snippets

            except Exception as e:
                st.error(f"An error occurred while getting the answer: {e}. Please try again or check server logs.")
                print(f"Error processing query in Streamlit: {e}")