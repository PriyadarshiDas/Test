# test_faiss_langchain.py

from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Use any Hugging Face embedding model
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Your input texts
texts = [
    "User withdrew ₹500 from ATM",
    "Customer deposited ₹1000 into savings",
    "The tiger roamed the jungle",
    "ATM withdrawal with receipt captured"
]

# Create FAISS vector store
db = FAISS.from_texts(texts=texts, embedding=embedding)

# Save to disk
db.save_local("faiss_test_index")

# Load it back and run a query
db = FAISS.load_local("faiss_test_index", embedding)
query = "cash withdrawal from ATM"
results = db.similarity_search(query, k=2)

print("\nTop matching documents:")
for i, doc in enumerate(results):
    print(f"{i+1}. {doc.page_content}")
