import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore

load_dotenv()
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


def generate_suggestions(job_description):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
    )
    query = f"Given a job description {job_description} what changes should one make to this resume to make it more compatible for this job"
    #query = f"Given a job description {job_description} Change the resume with the recommended changes. Only output the resume , nothing else."
    vector_store = PineconeVectorStore(
        index_name=os.environ.get("INDEX_NAME"), embedding=embeddings
    )
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vector_store.as_retriever(), combine_docs_chain=combine_docs_chain
    )
    result = retrieval_chain.invoke(input={"input": query})
    print(result["answer"])
    return result["answer"]


if __name__ == "__main__":
    suggestion = """About the jobInsight Global is looking for a Java Angular Developer to support an IT Consulting client in Santa Ana, CA.


This individual will be is responsible for the design, development and maintenance of large system software solutions and applications to meet business needs. Candidate is expected to be familiar with all phases of Software Development Life Cycle (SDLC) including gathering requirements, analyzing business requirements, designing, prototyping, development, testing, deployment, support, and documentation. Candidate is expected to lead the upgrade of Angular from version 11 to latest version.


Position: Java/Angular Developer
Location: Santa Ana, CA 92701
Schedule: FULLY ONSITE, 8-5 M-F, 9/80 schedule (Every other Friday off)
Duration: 6 month contract, likelihood for extensions
Contract: Sponsorship eligible


**Candidate must be able to pass a 5-panel drug screen (no THC) and live scan fingerprinting background check**


Required Skills & Experience:

5+ years or more of Java Configuration and Development experience
3+ years Angular handling application upgrades


Nice to Have Skills & Experience:

C and C++
Experience refactoring code to meet new stands and practices introduced in newer Angular versions
Strong JavaScript and TypeScript skills is essential
Experience in managing and upgrading dependencies and third-party libraries
Solid understanding of object-oriented programming concepts and design patterns.
Experience in Client-Server and N-tier web applications development, deployment and maintenance using Java, J2EE, Spring Batch, XML, HTML, CSS, JavaScript, Web Services"""
    generate_suggestions(suggestion)
