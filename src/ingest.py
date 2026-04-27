import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    print(f"Loading PDF: {PDF_PATH}")
    docs = PyPDFLoader(str(PDF_PATH)).load()
    print(f"  {len(docs)} page(s) loaded")

    print("Splitting into chunks...")
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150, add_start_index=False).split_documents(docs)
    if not splits:
        print("No content found in PDF. Exiting.")
        raise SystemExit(0)
    print(f"  {len(splits)} chunk(s) generated")

    print("Enriching metadata...")
    enriched = enriche_pdf(splits)
    ids = [f"doc-{i}" for i in range(len(enriched))]

    print("Initializing embeddings model...")
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"))

    print("Connecting to database...")
    store = store_pdf(embeddings)

    print(f"Embedding and storing {len(enriched)} chunk(s) into PostgreSQL...")
    store.add_documents(documents=enriched, ids=ids)
    print("Ingestion completed successfully!")



def enriche_pdf(splits):
    return [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]

def store_pdf(embeddings):
    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

if __name__ == "__main__":
    ingest_pdf()