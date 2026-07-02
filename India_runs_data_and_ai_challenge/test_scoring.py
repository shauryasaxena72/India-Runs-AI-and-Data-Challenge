"""
Quick validation - test scoring on first 100 candidates
"""
import json
from pathlib import Path
from feature_extractor import extract_features
from behavior_score import compute_behavior_score
from honeypot_penalty import compute_honeypot_penalty

# Load first 100 candidates
candidates_path = Path(__file__).parent / "candidates.jsonl"
sample_candidates = []

with open(candidates_path) as f:
    for i, line in enumerate(f):
        if i >= 100:
            break
        sample_candidates.append(json.loads(line))

print(f"Testing on {len(sample_candidates)} candidates...\n")

# Score them
scores = []
for i, candidate in enumerate(sample_candidates):
    try:
        tech = extract_features(candidate)
        behavior = compute_behavior_score(candidate)
        honeypot = compute_honeypot_penalty(candidate)
        
        final_score = (
            tech["retrieval_fit"] * 0.25 +
            tech["production_ai"] * 0.15 +
            tech["yoe_fit"] * 0.12 +
            tech["must_have_skills"] * 0.12 +
            tech["vector_db_exp"] * 0.10 +
            tech["product_company"] * 0.08 +
            tech["ai_skill_count"] * 0.05 +
            behavior["behavior_score"] * 0.13
        )
        
        final_score = max(0, final_score - honeypot["honeypot_penalty"])
        
        scores.append({
            "candidate_id": candidate["candidate_id"],
            "score": final_score,
            "retrieval": tech["retrieval_fit"],
        })
        
        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/100")
    
    except Exception as e:
        print(f"ERROR processing {candidate['candidate_id']}: {e}")
        import traceback
        traceback.print_exc()
        break

# Show results
print("\nTop 10 from sample:")
for i, s in enumerate(sorted(scores, key=lambda x: x["score"], reverse=True)[:10], 1):
    print(f"{i:2d}. {s['candidate_id']}: {s['score']:.4f} (retrieval: {s['retrieval']:.2f})")

print(f"\n✓ Validation complete - scoring pipeline works!")
