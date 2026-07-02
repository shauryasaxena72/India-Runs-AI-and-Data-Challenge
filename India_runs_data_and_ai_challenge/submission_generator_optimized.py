"""
Phase 9: Generate Submission (Optimized)
Create CSV submission efficiently for 100k candidates
"""
import json
import csv
import heapq
from pathlib import Path
from feature_extractor import extract_features
from behavior_score import compute_behavior_score
from honeypot_penalty import compute_honeypot_penalty
from reasoning_generator import extract_real_signals, generate_reasoning

def compute_final_score(candidate):
    """Compute final score for a candidate"""
    tech_features = extract_features(candidate)
    behavior_result = compute_behavior_score(candidate)
    honeypot_result = compute_honeypot_penalty(candidate)
    
    final_score = (
        tech_features["retrieval_fit"] * 0.25 +
        tech_features["production_ai"] * 0.15 +
        tech_features["yoe_fit"] * 0.12 +
        tech_features["must_have_skills"] * 0.12 +
        tech_features["vector_db_exp"] * 0.10 +
        tech_features["product_company"] * 0.08 +
        tech_features["ai_skill_count"] * 0.05 +
        behavior_result["behavior_score"] * 0.13
    )
    
    final_score = max(0, final_score - honeypot_result["honeypot_penalty"])
    
    return {
        "candidate_id": candidate["candidate_id"],
        "final_score": final_score,
        "tech_features": tech_features,
        "behavior_score": behavior_result["behavior_score"],
        "honeypot_penalty": honeypot_result["honeypot_penalty"],
        "honeypot_details": honeypot_result["components"],
    }

def stream_score_candidates(candidates_file="candidates.jsonl", keep_top=100):
    """
    Stream through candidates file and keep track of top N
    Memory-efficient: uses heap to track only top candidates
    """
    candidates_path = Path(__file__).parent / candidates_file
    
    print(f"Streaming through {candidates_file}...")
    
    # Use a min-heap to track top candidates (we need max, but Python has min heap)
    # Store tuples of (-score, candidate_data)
    top_heap = []
    
    candidates_map = {}  # Store full candidate data for top 100
    total_processed = 0
    
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            total_processed += 1
            
            if total_processed % 10000 == 0:
                print(f"  Processed {total_processed:,}")
            
            candidate = json.loads(line)
            
            try:
                score_result = compute_final_score(candidate)
                score = score_result["final_score"]
                candidate_id = candidate["candidate_id"]
                
                # If we haven't filled the heap yet, add
                if len(top_heap) < keep_top:
                    heapq.heappush(top_heap, (score, candidate_id))
                    candidates_map[candidate_id] = {
                        "candidate": candidate,
                        "score_result": score_result,
                    }
                # If this score is better than the worst in heap, replace it
                elif score > top_heap[0][0]:
                    old_score, old_id = heapq.heapreplace(top_heap, (score, candidate_id))
                    del candidates_map[old_id]
                    candidates_map[candidate_id] = {
                        "candidate": candidate,
                        "score_result": score_result,
                    }
            
            except Exception as e:
                print(f"  ERROR scoring {candidate_id}: {str(e)[:50]}")
                continue
    
    print(f"  Total processed: {total_processed:,}")
    print(f"  Top candidates identified: {len(top_heap)}")
    
    # Convert heap to sorted list (descending order)
    sorted_candidates = []
    while top_heap:
        score, candidate_id = heapq.heappop(top_heap)
        sorted_candidates.insert(0, (candidate_id, score, candidates_map[candidate_id]))
    
    return sorted_candidates

def create_optimized_submission(output_file="team_redrob_submission.csv"):
    """
    Generate submission using streaming approach
    """
    print("="*80)
    print("GENERATING SUBMISSION (Optimized for 100k candidates)")
    print("="*80 + "\n")
    
    # Stream and identify top 100
    print("Step 1: Identifying top 100 candidates...")
    top_100 = stream_score_candidates()
    
    print(f"\nStep 2: Writing submission to {output_file}...")
    
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["candidate_id", "rank", "score", "reasoning"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for rank, (candidate_id, score, data) in enumerate(top_100, 1):
            candidate = data["candidate"]
            score_result = data["score_result"]
            
            # Generate reasoning
            reasoning = generate_reasoning(candidate, score_result)
            
            writer.writerow({
                "candidate_id": candidate_id,
                "rank": rank,
                "score": f"{score:.6f}",
                "reasoning": reasoning,
            })
    
    print(f"\n✓ Submission created: {output_file}")
    print(f"  - Rows: {len(top_100)}")
    print(f"  - Top score: {top_100[0][1]:.4f}")
    print(f"  - 100th score: {top_100[-1][1]:.4f}")
    
    return output_path

def create_detailed_analysis(output_file="team_redrob_detailed.csv", top_candidates=None):
    """
    Create detailed analysis CSV with all scores
    """
    print(f"\nStep 3: Creating detailed analysis...")
    
    if top_candidates is None:
        top_candidates = stream_score_candidates()
    
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "rank", "candidate_id", "final_score",
            "retrieval_fit", "production_ai", "yoe_fit", "must_have_skills",
            "vector_db_exp", "product_company", "ai_skill_count",
            "behavior_score", "honeypot_penalty"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for rank, (candidate_id, score, data) in enumerate(top_candidates, 1):
            score_result = data["score_result"]
            
            writer.writerow({
                "rank": rank,
                "candidate_id": candidate_id,
                "final_score": f"{score:.6f}",
                "retrieval_fit": f"{score_result['tech_features']['retrieval_fit']:.4f}",
                "production_ai": f"{score_result['tech_features']['production_ai']:.4f}",
                "yoe_fit": f"{score_result['tech_features']['yoe_fit']:.4f}",
                "must_have_skills": f"{score_result['tech_features']['must_have_skills']:.4f}",
                "vector_db_exp": f"{score_result['tech_features']['vector_db_exp']:.4f}",
                "product_company": f"{score_result['tech_features']['product_company']:.4f}",
                "ai_skill_count": f"{score_result['tech_features']['ai_skill_count']:.4f}",
                "behavior_score": f"{score_result['behavior_score']:.4f}",
                "honeypot_penalty": f"{score_result['honeypot_penalty']:.4f}",
            })
    
    print(f"✓ Detailed analysis created: {output_file}")
    
    return output_path

if __name__ == "__main__":
    # Create submission
    submission_path = create_optimized_submission()
    
    # Also create detailed analysis - reuse the same top 100
    detailed_path = create_detailed_analysis()
    
    print("="*80)
    print("Files generated successfully!")
    print("="*80)
