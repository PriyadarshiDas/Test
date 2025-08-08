import os
import json
import boto3
from dotenv import load_dotenv
from chromadb import Client
from chromadb.config import Settings

# Your chunking function (you can paste your semantic_chunking here)
from your_chunking_module import semantic_chunking  

# Load environment variables (AWS creds etc.)
load_dotenv()

# Initialize AWS Bedrock client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Initialize ChromaDB client
client = Client(Settings(persist_directory="./chroma_store"))
collection = client.get_or_create_collection(name="bank_policies")

# Titan embedding batch function
def get_titan_embeddings_batch(text_list):
    """
    Sends a batch of text chunks to Amazon Titan Embeddings v2 and returns their vectors.
    text_list: list of strings (each ≤ 8192 tokens)
    """
    body = json.dumps({"inputText": text_list})
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        contentType="application/json",
        accept="application/json",
        body=body
    )
    result = json.loads(response["body"].read())
    return result["embedding"]  # list of vectors in same order

# Main embedding + storage function
def embed_and_store(document_text, batch_size=10):
    # Step 1: Chunk the document
    chunks = semantic_chunking(document_text)

    # Step 2: Loop in batches
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vectors = get_titan_embeddings_batch(batch)

        # Step 3: Store each chunk + vector in Chroma
        ids = [f"chunk-{i+j}" for j in range(len(batch))]
        collection.add(
            ids=ids,
            documents=batch,
            embeddings=vectors
        )

    print(f"✅ Embedded and stored {len(chunks)} chunks in ChromaDB.")

# Example usage
if __name__ == "__main__":
    sample_text = """
    CUSTOMER DUE DILIGENCE
    1. All customers must provide valid identification documents before account opening.
    2. For corporate customers, incorporation certificate and board resolution are mandatory.
    • High-risk customers require enhanced due diligence.
    • Any deposit above ₹10 lakh must be reported to compliance within 24 hours.

    LOAN PROCESSING GUIDELINES
    1. Loan applications must be reviewed within 7 working days.
    2. Collateral verification is mandatory for loans above ₹50 lakh.
    """
    
    embed_and_store(sample_text, batch_size=10)
