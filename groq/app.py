# import streamlit as st
# import os
# import time

# from langchain_groq import ChatGroq
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_classic.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_classic.chains import create_retrieval_chain
# from langchain_community.vectorstores import FAISS



# from dotenv import load_dotenv
# load_dotenv()

# #load the groq api key
# groq_api_key = os.getenv("GROQ_API_KEY")

# if "vector" not in st.session_state:
#     st.session_state.embeddings= OllamaEmbeddings(model="nomic-embed-text")
#     st.session_state.loader = WebBaseLoader("https://docs.langchain.com/")
#     st.session_state.docs = st.session_state.loader.load()

#     st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
#     st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

# st.title("ChatGroq")
# llm = ChatGroq(groq_api_key = groq_api_key,
#                model_name="llama-3.3-70b-versatile")

# prompt = ChatPromptTemplate.from_template(
#     """
#     Answer the question based on provided context only.
#     Please provide the most accurate response based on the question.
#     <context>
#     {context}
#     </context>
#     Questions: {input} 

# """
# )

# document_chain = create_stuff_documents_chain(llm, prompt)
# retriever = st.session_state.vectors.as_retriever()
# retriever_chain = create_retrieval_chain(retriever, document_chain)

# prompt = st.text_input("Input your prompt here.")

# if prompt:
#     start=time.process_time()
#     response = retriever_chain.invoke({"input": prompt})
#     print("Response time : ", time.process_time()-start)
#     st.write(response['answer'])

#     # With a streamlit expander
#     with st.expander("Document Similarity Search"):
#         # Find the relevant chunks
#         for i, doc in enumerate(response["context"]):
#             st.write(doc.page_content)
#             st.write("--------------------------------")






# import streamlit as st
# import os
# import time

# from langchain_groq import ChatGroq
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS

# from dotenv import load_dotenv
# load_dotenv()

# # Load API Key
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Initialize session state (FIXED: vectors key)
# if "vectors" not in st.session_state:
#     st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
#     # 
#     st.session_state.loader = WebBaseLoader("https://en.wikipedia.org/wiki/Main_Page")
#     st.session_state.docs = st.session_state.loader.load()

#     st.session_state.text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )

#     st.session_state.final_documents = st.session_state.text_splitter.split_documents(
#         st.session_state.docs
#     )

#     st.session_state.vectors = FAISS.from_documents(
#         st.session_state.final_documents,
#         st.session_state.embeddings
#     )

# # UI Title
# st.title("ChatGroq with RAG")

# # LLM
# llm = ChatGroq(
#     groq_api_key=groq_api_key,
#     model_name="llama-3.3-70b-versatile"
# )

# # Retriever
# retriever = st.session_state.vectors.as_retriever()

# # User Input
# user_prompt = st.text_input("💬 Ask your question:")

# # Main Logic
# if user_prompt:

#     start = time.time()

#     with st.spinner("🤖 Thinking..."):

#         # Step 1: Retrieve documents
#         docs = retriever.invoke(user_prompt)

#         # Step 2: Build context
#         context = "\n\n".join([doc.page_content for doc in docs])

#         formatted_prompt = f"""
#         You are a helpful assistant.
#         Answer the question based on provided context only.
#         Please provide the most accurate response based on the question.

#         <context>
#         {context}
#         </context>

#         Question: {user_prompt}
#         """

#         # Step 3: Streaming response
#         response_placeholder = st.empty()
#         full_response = ""

#         for chunk in llm.stream(formatted_prompt):
#             if chunk.content:
#                 full_response += chunk.content
#                 response_placeholder.markdown(full_response + "▌")

#         response_placeholder.markdown(full_response)

#     end = time.time()

#     # ✅ Response Time
#     st.write(f"⏱ Response time: {end - start:.2f} seconds")

#     # ✅ Snippet Viewer
#     with st.expander("📄 Top Retrieved Context (Snippets)"):
#         for i, doc in enumerate(docs[:3]):  # Top 3 chunks
#             st.markdown(f"**Snippet {i+1}:**")
#             st.write(doc.page_content[:500])  # Limit size
#             st.write("---")






import streamlit as st
import os
import time

from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

# -------------------- CONFIG --------------------
st.set_page_config(page_title="ChatGroq RAG", page_icon="🤖", layout="wide")

# Custom CSS for better UI
# st.markdown("""
# <style>
# .chat-user {
#     background-color: #DCF8C6;
#     padding: 10px;
#     border-radius: 10px;
#     margin-bottom: 10px;
# }
# .chat-bot {
#     background-color: #F1F0F0;
#     padding: 10px;
#     border-radius: 10px;
#     margin-bottom: 10px;
# }
# </style>
# """, unsafe_allow_html=True)


st.markdown("""
<style>
.chat-user {
    background: linear-gradient(135deg, #4FACFE, #00F2FE);
    color: white;
    padding: 12px;
    border-radius: 15px 15px 0 15px;
    margin-bottom: 10px;
    max-width: 75%;
    margin-left: auto;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    font-weight: 500;
}

.chat-bot {
    background: linear-gradient(135deg, #FBC2EB, #A6C1EE);
    color: #333;
    padding: 12px;
    border-radius: 15px 15px 15px 0;
    margin-bottom: 10px;
    max-width: 75%;
    margin-right: auto;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    font-weight: 500;
}

/* Optional smooth hover effect */
.chat-user:hover, .chat-bot:hover {
    transform: scale(1.02);
    transition: 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# -------------------- API --------------------
groq_api_key = os.getenv("GROQ_API_KEY")

# -------------------- SESSION INIT --------------------
if "vectors" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    loader = WebBaseLoader("https://en.wikipedia.org/wiki/Main_Page")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_docs = splitter.split_documents(docs)

    st.session_state.vectors = FAISS.from_documents(final_docs, st.session_state.embeddings)

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------- MAIN UI --------------------
st.title("🤖 ChatGroq RAG")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# Input box
user_prompt = st.chat_input("Ask anything...")

# -------------------- LLM --------------------
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

retriever = st.session_state.vectors.as_retriever()

# -------------------- MAIN LOGIC --------------------
if user_prompt:
    
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # ✅ Show user message instantly (before processing)
    st.markdown(f"<div class='chat-user'>🧑 {user_prompt}</div>", unsafe_allow_html=True)

    start = time.time()

    with st.spinner("🤖 Thinking..."):

        # Retrieve docs
        docs = retriever.invoke(user_prompt)
        context = "\n\n".join([doc.page_content for doc in docs])

        # Include chat history
        history_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:]]
        )

        formatted_prompt = f"""
        You are a helpful assistant.
        Answer the question based on provided context only.
        Please provide the most accurate response based on the question.

Chat History:
{history_text}

Context:
{context}

Question:
{user_prompt}
"""

        # Streaming response
        response_placeholder = st.empty()
        full_response = ""

        for chunk in llm.stream(formatted_prompt):
            if chunk.content:
                full_response += chunk.content
                response_placeholder.markdown(
                    f"<div class='chat-bot'>🤖 {full_response}▌</div>",
                    unsafe_allow_html=True
                )

        response_placeholder.markdown(
            f"<div class='chat-bot'>🤖 {full_response}</div>",
            unsafe_allow_html=True
        )

    end = time.time()

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Response time
    st.caption(f"⏱ Response time: {end - start:.2f} sec")

    # # Snippets
    # with st.expander("📄 Retrieved Context"):
    #     for i, doc in enumerate(docs[:3]):
    #         st.markdown(f"**Snippet {i+1}:**")
    #         st.write(doc.page_content[:400])
    #         st.write("---")