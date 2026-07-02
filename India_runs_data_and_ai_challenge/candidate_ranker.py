"""
Phase 6: Final Scoring & Ranking
Orchestrate all features and produce final candidate rankings
"""
import json
from pathlib import Path
from feature_extractor import extract_features
from behavior_score import compute_behavior_score
from honeypot_penalty import compute_honeypot_penalty

def compute_final_score(candidate):
    """
    Final Score = weighted combination of all components
    """
    
    # Extract technical features
    tech_features = extract_features(candidate)
    
    # Extract behavior features
    behavior_result = compute_behavior_score(candidate)
    behavior_score = behavior_result["behavior_score"]
    
    # Compute honeypot penalty
    honeypot_result = compute_honeypot_penalty(candidate)
    penalty = honeypot_result["honeypot_penalty"]
    
    # FINAL SCORING FORMULA (optimized for this JD)
    # Weights calibrated for: Retrieval/Ranking Engineer + Production + Product company experience
    final_score = (
        tech_features["retrieval_fit"] * 0.25 +          # Retrieval & ranking is #1 priority
        tech_features["production_ai"] * 0.15 +           # Production systems matter
        tech_features["yoe_fit"] * 0.12 +                 # Experience fit
        tech_features["must_have_skills"] * 0.12 +        # Core skills
        tech_features["vector_db_exp"] * 0.10 +           # Vector DB specialized
        tech_features["product_company"] * 0.08 +         # Product company experience
        tech_features["ai_skill_count"] * 0.05 +          # Overall AI toolkit
        behavior_score * 0.13                             # Engagement & availability
    )
    
    # Apply honeypot penalty
    final_score = max(0, final_score - penalty)
    
    return {
        "candidate_id": candidate["candidate_id"],
        "final_score": final_score,
        "technical_fit": {
            "retrieval_fit": tech_features["retrieval_fit"],
            "production_ai": tech_features["production_ai"],
            "yoe_fit": tech_features["yoe_fit"],
            "must_have_skills": tech_features["must_have_skills"],
            "vector_db_exp": tech_features["vector_db_exp"],
            "product_company": tech_features["product_company"],
            "ai_skill_count": tech_features["ai_skill_count"],
        },
        "behavior_fit": behavior_result["components"],
        "behavior_score": behavior_score,
        "honeypot_penalty": penalty,
        "honeypot_details": honeypot_result["components"],
    }

def rank_candidates(candidates_file="candidates.jsonl"):
    """
    Load all candidates and produce ranked list
    """
    candidates_path = Path(__file__).parent / candidates_file
    
    candidates = []
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))
    
    print(f"Scoring {len(candidates)} candidates...\n")
    
    # Score all candidates
    scored = []
    for i, candidate in enumerate(candidates):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(candidates)}")
        
        score_result = compute_final_score(candidate)
        scored.append(score_result)
    
    # Sort by final score descending
    ranked = sorted(scored, key=lambda x: x["final_score"], reverse=True)
    
    return ranked

def get_top_candidates(ranked, n=20):
    """
    Get top N candidates with scoring breakdown
    """
    return ranked[:n]

if __name__ == "__main__":
    print("="*80)
    print("CANDIDATE RANKING")
    print("="*80)
    
    # Rank all candidates
    ranked = rank_candidates()
    
    print(f"\n{'='*80}")
    print(f"Top 20 Candidates")
    print(f"{'='*80}\n")
    
    top_20 = get_top_candidates(ranked, 20)
    
    for rank, candidate in enumerate(top_20, 1):
        print(f"{rank:2d}. Candidate {candidate['candidate_id']}: {candidate['final_score']:.4f}")
        print(f"    Technical: Retrieval={candidate['technical_fit']['retrieval_fit']:.2f}, " +
              f"Production={candidate['technical_fit']['production_ai']:.2f}, " +
              f"YOE={candidate['technical_fit']['yoe_fit']:.2f}")
        print(f"    Behavior: {candidate['behavior_score']:.2f} | " +
              f"Penalty: {candidate['honeypot_penalty']:.3f}")
        if candidate['honeypot_penalty'] > 0.1:
            print(f"    ⚠️  HONEYPOT FLAGS: {[k for k,v in candidate['honeypot_details'].items() if v > 0.05]}")
        print()
    
    print(f"\n{'='*80}")
    print(f"Score Distribution")
    print(f"{'='*80}\n")
    
    top_scores = [c['final_score'] for c in ranked[:100]]
    print(f"Top 100 candidates:")
    print(f"  Max: {max(top_scores):.4f}")
    print(f"  Min: {min(top_scores):.4f}")
    print(f"  Mean: {sum(top_scores)/len(top_scores):.4f}")
    print(f"  Median: {sorted(top_scores)[len(top_scores)//2]:.4f}")
