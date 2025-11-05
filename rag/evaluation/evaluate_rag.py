"""
RAG Evaluation for E-Commerce Agentic RAG
"""
import json
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Import your RAG components
from rag.retrieval.vector_store import PineconeVectorStore
from rag.retrieval.retriever import Retriever
from rag.agents.agentic_controller import AgenticRAGController
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Initialize RAG components
def build_controller():
    vector_store = PineconeVectorStore(index_name="ecommerce-agentic-rag")
    embedder = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    retriever = Retriever(vector_store, embedder)
    return AgenticRAGController(retriever)

# Build once
controller = build_controller()

# Load golden dataset
GOLDEN_PATH = "rag/evaluation/data/my_ecommerce.jsonl"
with open(GOLDEN_PATH) as f:
    my_ecom = [json.loads(line) for line in f]

# Run inference
results = []
print(f"Evaluating {len(my_ecom)} queries...")

for i, item in enumerate(my_ecom):
    print(f"[{i+1}/{len(my_ecom)}] Query: {item['query'][:60]}...")
    try:
        output = controller.query(item["query"])
        
        # Extract retrieved contexts (from internal state or pass through)
        # Note: Add retrieved_docs to controller.query() return if missing
        retrieved_docs = getattr(output, "retrieved_docs", [])
        if not retrieved_docs:
            # Fallback: re-retrieve to get docs
            docs = controller.retriever.retrieve(item["query"], top_k=5)
            retrieved_docs = [{"text": d["text"]} for d in docs]

        results.append({
            "question": item["query"],
            "answer": output["answer"],
            "contexts": [d["text"] for d in retrieved_docs],
            "ground_truth": item["answer"],
            "tool_calls": [t["tool"] for t in output.get("tool_calls", [])],
            "expected_tools": item["tools"],
            "confidence": output.get("confidence", 0.0),
            "hops": output.get("hops", 1)
        })
    except Exception as e:
        print(f"Error on query {i}: {e}")
        results.append({
            "question": item["query"],
            "answer": f"[ERROR] {str(e)}",
            "contexts": [],
            "ground_truth": item["answer"],
            "tool_calls": [],
            "expected_tools": item["tools"]
        })

# Convert to Dataset
dataset = Dataset.from_pandas(pd.DataFrame(results))

# RAGAS Evaluation
print("Running RAGAS evaluation...")
scores = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

# Custom Metrics
def tool_call_accuracy(results):
    correct = sum(
        len(set(r["tool_calls"]) & set(r["expected_tools"])) == len(r["expected_tools"])
        for r in results
        if r["expected_tools"]
    )
    total = sum(1 for r in results if r["expected_tools"])
    return correct / total if total > 0 else 1.0

custom_score = {
    "tool_call_accuracy": tool_call_accuracy(results),
    "avg_confidence": sum(r.get("confidence", 0) for r in results) / len(results),
    "avg_hops": sum(r.get("hops", 1) for r in results) / len(results)
}

# Final Report
report = {**scores, **custom_score}
print("\n" + "="*50)
print("RAG EVALUATION REPORT")
print("="*50)
for k, v in report.items():
    print(f"{k:20}: {v:.4f}")
print("="*50)

# Save
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f"rag/evaluation/results/report_{timestamp}.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"Report saved: rag/evaluation/results/report_{timestamp}.json")