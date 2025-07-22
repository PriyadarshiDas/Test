import chromadb
from chromadb.utils import embedding_functions

# Set up ChromaDB client and default embedder
client = chromadb.Client()
embed_fn = embedding_functions.DefaultEmbeddingFunction()

# Create collection
collection = client.create_collection("test_docs", embedding_function=embed_fn)

# Add documents
docs = [
    "User withdrew ₹500 from ATM",
    "Customer deposited ₹1000",
    "Tiger in the jungle"
]
collection.add(documents=docs, ids=["1", "2", "3"])

# Query
results = collection.query(query_texts=["ATM withdrawal"], n_results=2)

# Output
for i, doc in enumerate(results["documents"][0]):
    print(f"{i+1}. {doc}")
