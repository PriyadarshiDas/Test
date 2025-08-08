import boto3
import json
from chromadb import Client
from chromadb.config import Settings

# AWS Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_titan_embedding(text):
    body = json.dumps({
        "inputText": text
    })
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",  # or your chosen version
        contentType="application/json",
        accept="application/json",
        body=body
    )
    result = json.loads(response["body"].read())
    return result["embedding"]

# Example: store embeddings in Chroma
client = Client(Settings(persist_directory="./chroma_store"))
collection = client.get_or_create_collection(name="bank_policies")

# Your chunking logic from above
chunks = semantic_chunking(sample_text)

# Loop and embed
for i, chunk in enumerate(chunks):
    vector = get_titan_embedding(chunk)
    collection.add(
        ids=[f"chunk-{i}"],
        documents=[chunk],
        embeddings=[vector]
    )

print("All chunks embedded and stored.")
