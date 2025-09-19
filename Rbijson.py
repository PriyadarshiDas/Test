import json
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- Import your retriever setup (assuming you already built embeddings + vectorstore) ---
# For example:
# from retriever_setup import rbi_chunks, retriever
# rbi_chunks: list of RBI text chunks (strings)
# retriever: vectorstore retriever built on Axis Bank docs

from retriever_setup import rbi_chunks, retriever

# --- 1. Setup Bedrock Claude LLM ---
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # You can swap for opus/haiku
    region_name="us-east-1",   # Change if your Bedrock is in a different region
    temperature=0
)

# --- 2. Define Prompt for JSON Comparison ---
comparison_prompt = PromptTemplate(
    template="""
You are a compliance analyst AI. 
Compare an RBI policy clause with Axis Bank’s internal policy clause.

RBI Clause:
{rbi_text}

Axis Clause:
{axis_text}

Rules:
- If both clauses cover the same requirement in the same way → "aligned".
- If both cover the same topic but differ in thresholds, timelines, or process → "partial_alignment".
- If Axis has no matching clause → "missing".

Respond ONLY in this JSON format:
{{
  "rbi_chunk_summary": "...",
  "axis_chunk_summary": "...",
  "status": "aligned/partial_alignment/missing",
  "explanation": "..."
}}
""",
    input_variables=["rbi_text", "axis_text"],
)

comparison_chain = LLMChain(llm=llm, prompt=comparison_prompt)

# --- 3. Run Comparison for All RBI Chunks ---
json_results = []

for rbi_chunk in rbi_chunks:
    # Retrieve top 2 matching Axis chunks
    axis_candidates = retriever.get_relevant_documents(rbi_chunk)
    
    if not axis_candidates:
        # No match found at all
        no_match_json = {
            "rbi_chunk_summary": rbi_chunk[:300],  # small preview of RBI text
            "axis_chunk_summary": "No equivalent clause found.",
            "status": "missing",
            "explanation": "RBI clause has no matching policy in Axis docs."
        }
        json_results.append(no_match_json)
        continue

    for axis_doc in axis_candidates:
        try:
            response = comparison_chain.run(
                rbi_text=rbi_chunk,
                axis_text=axis_doc.page_content
            )

            # Parse JSON safely
            result = json.loads(response)
            json_results.append(result)

        except Exception as e:
            print("Error parsing response:", response, e)

# --- 4. Save Final JSON File ---
with open("rbi_axis_gap_results.json", "w") as f:
    json.dump(json_results, f, indent=2)

print("✅ Gap analysis JSON saved to rbi_axis_gap_results.json")
