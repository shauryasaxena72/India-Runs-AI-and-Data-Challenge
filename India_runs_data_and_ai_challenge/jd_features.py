"""
Phase 2: Convert JD Into Features
Extract key requirements from the job description
"""

# Based on the Redrob JD for AI Engineer / Search & Ranking specialist

# MUST HAVE SKILLS
must_have = [
    "retrieval",
    "ranking",
    "recommendation",
    "embeddings",
    "vector database",
    "python",
    "machine learning",
    "nlp",
]

# NICE TO HAVE SKILLS / NICE TO HAVE EXPERIENCE
good_to_have = [
    "llm",
    "lora",
    "peft",
    "fine-tuning",
    "distributed systems",
    "hr tech",
    "rag",
]

# NEGATIVE SIGNALS - candidates with ONLY these (no production AI) should score lower
negative = [
    "pure research",
    "consulting only",
    "computer vision only",
    "speech only",
    "theoretical",
    "academic only",
]

# JOB DESCRIPTION SIGNALS
JD_SIGNALS = {
    "yoe_ideal_min": 5,
    "yoe_ideal_max": 9,
    "yoe_acceptable_min": 3,
    "yoe_acceptable_max": 15,
    
    "notice_period_preferred": 30,  # days
    
    "sector_positive": [
        "startup",
        "saas",
        "product",
        "fintech",
        "ai",
        "tech",
        "software",
    ],
    
    "sector_negative": [
        "tcs",
        "infosys",
        "wipro",
        "cognizant",
        "accenture",
        "capgemini",
    ],
    
    # These are explicitly mentioned in JD as traps
    "honeypot_keywords": [
        "keyword extraction",
        "keyword counter",
        "text analysis",
        "document processing",
    ],
}

# VECTOR DATABASE TECHNOLOGIES
vector_databases = [
    "pinecone",
    "milvus",
    "weaviate",
    "faiss",
    "qdrant",
    "elasticsearch",
    "opensearch",
    "vector",
]

# PRODUCTION AI INDICATORS
production_keywords = [
    "production",
    "deployed",
    "scale",
    "real users",
    "pipelines",
    "serving",
    "inference",
    "latency",
    "throughput",
    "millions",
]

# RETRIEVAL & RANKING CORE KEYWORDS
core_retrieval_keywords = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "vector",
    "embedding",
    "semantic",
    "relevance",
    "reranking",
    "information retrieval",
]

print("JD Features Extracted:")
print(f"Must Have Skills ({len(must_have)}): {must_have}")
print(f"Good To Have Skills ({len(good_to_have)}): {good_to_have}")
print(f"Negative Signals ({len(negative)}): {negative}")
print(f"Vector Databases ({len(vector_databases)}): {vector_databases}")
print(f"Production Keywords ({len(production_keywords)}): {production_keywords}")
print(f"Core Retrieval Keywords ({len(core_retrieval_keywords)}): {core_retrieval_keywords}")
