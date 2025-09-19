import json
from langchain_aws import ChatBedrock
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.mapreduce import MapReduceDocumentsChain, ReduceDocumentsChain

# --- 1. Load JSON results (your chunk-level comparison file) ---
with open("rbi_axis_gap_results.json", "r") as f:
    comparison_results = json.load(f)

# --- 2. Convert JSON into LangChain Documents ---
docs = []
for item in comparison_results:
    text = (
        f"RBI Policy: {item['rbi_chunk_summary']}\n"
        f"Axis Policy: {item['axis_chunk_summary']}\n"
        f"Status: {item['status']}\n"
        f"Explanation: {item['explanation']}\n"
    )
    docs.append(Document(page_content=text))

# --- 3. Use Bedrock Claude Model ---
# Make sure your AWS credentials are configured (boto3 looks at ~/.aws/credentials or env vars)
llm = ChatBedrock(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # Example model, can use opus/haiku/sonnet
    region_name="us-east-1",  # adjust to your AWS region
    temperature=0
)

# --- 4. Define Prompts ---
map_prompt = PromptTemplate(
    template="""
You are an assistant preparing compliance analysis.

Summarize the following chunk-level comparison into a short finding:
{text}

Respond in structured form:
- Alignment type (aligned/partial/missing)
- Short explanation
""",
    input_variables=["text"],
)

reduce_prompt = PromptTemplate(
    template="""
You are preparing a compliance gap analysis report.

Combine the following findings into a clear summary with 3 sections:
1. Fully aligned policies
2. Partially aligned policies
3. Missing policies

{text}
""",
    input_variables=["text"],
)

# --- 5. Create Chains ---
map_chain = LLMChain(llm=llm, prompt=map_prompt)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=reduce_chain,
    collapse_documents_chain=reduce_chain,
    token_max=3000,
)

map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="text",  # this maps Document.page_content → {text}
)

# --- 6. Run Summarization ---
final_report = map_reduce_chain.run(docs)

print("\n==== Final Gap Analysis Report ====\n")
print(final_report)
