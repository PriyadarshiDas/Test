import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def semantic_chunking(text, chunk_size=1000, chunk_overlap=150):
    """
    Splits banking policy text semantically based on headings, bullet points, and clauses.
    """
    # Step 1: Split on section markers (headings, numbered clauses, bullets)
    sections = re.split(
        r"(?m)(?=^([A-Z][A-Z\s]+|[0-9]+\.\s|[•\-]\s))",  # headings, clauses, bullets
        text
    )

    # Step 2: Merge small sections together until chunk size limit is reached
    merged_sections = []
    buffer = ""
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue

        if len(buffer) + len(sec) <= chunk_size:
            buffer += " " + sec
        else:
            merged_sections.append(buffer.strip())
            buffer = sec
    if buffer:
        merged_sections.append(buffer.strip())

    # Step 3: If any section is still too big, do recursive splitting
    final_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )

    for section in merged_sections:
        if len(section) > chunk_size:
            final_chunks.extend(splitter.split_text(section))
        else:
            final_chunks.append(section)

    return final_chunks

# Example
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
    chunks = semantic_chunking(sample_text)
    for i, chunk in enumerate(chunks, 1):
        print(f"--- Chunk {i} ---\n{chunk}\n")
