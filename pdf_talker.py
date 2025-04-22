import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

from langchain_openai.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template


def get_conversation_chain(vectorstore, model):
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=128
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def get_vectorstor(text_chunks, model, device):
    embeddings = OpenAIEmbeddings()
    vectorstor = FAISS.from_texts(
        texts=text_chunks,   
        embedding=embeddings
        )
    return vectorstor


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks


def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(reversed(st.session_state.chat_history)):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():      
    st.set_page_config(page_title='Chat PDF',
                       page_icon=':books:')
    
    st.write(css, unsafe_allow_html=True)
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header('Chat w/ PDF :books:')
    usr_question = st.text_input('Ask here')
    if usr_question:
        handle_user_input(usr_question)

    

    with st.sidebar:
        st.subheader('your docs')
        pdf_docs = st.file_uploader(
            'upload pdf -> process', 
            accept_multiple_files=True,

            )
        device = st.selectbox('device', options=['cpu', 'mps'])
        model = st.selectbox('model', options=['openai', 'local'])

        if st.button('process :beers:'):
            with st.spinner('digesting...', show_time=True):
                raw_text = get_pdf_text(pdf_docs)   
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstor(text_chunks, model=model, device=device)
                
                st.session_state.conversation = get_conversation_chain(vectorstore, model)
    

if __name__ == "__main__":
    main()