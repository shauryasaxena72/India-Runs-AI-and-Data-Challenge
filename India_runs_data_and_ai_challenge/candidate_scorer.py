print("Script started")
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

sample_file = BASE_DIR / "sample_candidates.json"

with open(r"D:\Portfolio\Data Science Projects\INDIA Run Hackathon\[PUB] India_runs_data_and_ai_challenge\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\sample_candidates.json",
          "r",
          encoding="utf-8") as f:
    candidates = json.load(f)

print("File loaded")
print("Candidates:", len(candidates))

import re

POSITIVE_KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "embeddings",
    "vector",
    "search",
    "relevance",
    "information retrieval",
    "ndcg",
    "mrr",
    "map",
    "ab testing",
    "a/b testing",
    "python",
    "llm",
    "rag"
]

NEGATIVE_KEYWORDS = [
    "computer vision",
    "robotics",
    "speech only",
    "academic research"
]

def technical_score(candidate):

    text_parts = []

    text_parts.append(
        candidate["profile"]["headline"]
    )

    text_parts.append(
        candidate["profile"]["summary"]
    )

    for job in candidate["career_history"]:
        text_parts.append(job["description"])

    text = " ".join(text_parts).lower()

    score = 0

    for kw in POSITIVE_KEYWORDS:
        if kw in text:
            score += 1

    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 1

    return score

print("Candidates loaded:", len(candidates))

for i in range(5):
    c = candidates[i]

    score = technical_score(c)

    print(
        c["candidate_id"],
        "|",
        c["profile"]["current_title"],
        "| Score:",
        score
    )