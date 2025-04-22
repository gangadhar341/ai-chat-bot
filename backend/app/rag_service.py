import os
from flask import current_app as app
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Set environment variables (optional: move to a secure location like dotenv or config)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "Mozilla/5.0")

class RAGService:
    @staticmethod
    def fetch_dynamic_page(url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        driver.quit()

        # Extract visible text
        text = soup.get_text(separator=" ", strip=True)

        # Extract metadata
        meta_description = soup.find("meta", attrs={"name": "description"})
        description = meta_description["content"] if meta_description else "No description found"

        title_tag = soup.find("title")
        title = title_tag.text if title_tag else "No title"

        return Document(
            page_content=text,
            metadata={
                "source": url,
                "title": title,
                "description": description
            }
        )

    @staticmethod
    def format_doc(docs):
        return "\n".join(doc.page_content for doc in docs)

    @staticmethod
    def ask_gpt(data={}):
        question = data.get("question", "").strip()
        if not question:
            return "Question is missing from the input."

        # Load static content
        loader = WebBaseLoader(web_paths=["https://sphotalabs.com/"])
        sphota_docs = loader.load()

        # Load dynamic content
        dynamic_doc = RAGService.fetch_dynamic_page("https://invoiceparser.io/")
        docs = sphota_docs + [dynamic_doc]

        # Chunk text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        # Embed and store in vector DB
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

        # Load prompt from Langchain Hub
        prompt = hub.pull("rlm/rag-prompt")

        # Set up LLM
        llm = ChatOpenAI(temperature=0)

        # RAG pipeline
        rag_chain = (
            {"context": retriever | RAGService.format_doc, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Run RAG
        result = rag_chain.invoke(question)
        print("Result from RAG Chain:", result)

        return result
