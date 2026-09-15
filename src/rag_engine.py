import chromadb

def init_policy_rag():
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="accounting_policies")
    
    # Ingest enterprise accounting policies
    collection.add(
        documents=[
            "ASC 230: Cash equivalents must represent short-term, highly liquid investments readily convertible to known amounts of cash.",
            "GAAP Audit Policy: Any unadjusted visual reporting variance exceeding $1,000,000 requires CFO notification and a HIGH risk severity rating.",
            "IFRS IAS 7: Statement of Cash Flows requires clear reconciliation between reported cash balance and balance sheet figures."
        ],
        ids=["rule_asc230", "rule_gaap_risk", "rule_ias7"]
    )
    return collection

def query_policy(collection, query_str: str) -> str:
    results = collection.query(query_texts=[query_str], n_results=2)
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        return "\n".join(f"- {d}" for d in docs)
    return "No explicit GAAP policy returned."

if __name__ == "__main__":
    col = init_policy_rag()
    print(" [RAG Engine] Policy search test:")
    print(query_policy(col, "variance exceeding limit risk rating"))
