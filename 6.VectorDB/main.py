import os
import time

from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_text_splitters import CharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec, PodSpec
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA

use_serverless = True

if __name__ == "__main__":
    print("Hello Vector DB")
    loader = TextLoader("docs.txt", encoding='utf-8')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print(len(texts))

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

    index_name = 'semantic-search-openai'
    spec = ServerlessSpec(cloud="aws", region="us-west-2")
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='euclidean',
            spec=PodSpec(environment='gcp-starter')
        )
        # wait for index to be initialized
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)

    # connect to index
    index = pc.Index(index_name)
    index.describe_index_stats()

    print("upload text doc to pinecone")
    # vectorstore = PineconeVectorStore.from_documents(documents=texts, embedding=embeddings, index_name=index_name)
    vectorstore = PineconeVectorStore(embedding=embeddings, index_name=index_name)
    print("Retrieve")
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever= vectorstore.as_retriever()
    )
    query = "Technical challenges of using vector db ?"
    result = qa.run(query)
    print(f"result = {result}")


