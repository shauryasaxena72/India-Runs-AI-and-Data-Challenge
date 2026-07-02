"""
Phase 9: Generate Submission
Create CSV submission with candidate_id, rank, score, and reasoning
Must have exactly 100 rows
"""
import csv
from pathlib import Path
from candidate_ranker import rank_candidates
from reasoning_generator import generate_reasoning_for_ranked

def create_submission(output_file="team_redrob_submission.csv"):
    """
    Generate final submission CSV
    Format: candidate_id, rank, score, reasoning
    Exactly 100 rows
    """
    
    print(f"Creating submission...\n")
    
    # Rank all candidates
    print("Step 1: Ranking candidates...")
    ranked = rank_candidates()
    
    # Generate reasoning
    print("Step 2: Generating reasoning...")
    reasoning_list = generate_reasoning_for_ranked(ranked)
    
    # Create map of reasoning by candidate_id
    reasoning_map = {r["candidate_id"]: r["reasoning"] for r in reasoning_list}
    
    # Take top 100
    top_100 = ranked[:100]
    
    print(f"Step 3: Writing submission file...")
    
    output_path = Path(__file__).parent / output_file
    
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["candidate_id", "rank", "score", "reasoning"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write rows
        for rank, candidate_score in enumerate(top_100, 1):
            candidate_id = candidate_score["candidate_id"]
            reasoning = reasoning_map.get(candidate_id, "")
            
            writer.writerow({
                "candidate_id": candidate_id,
                "rank": rank,
                "score": f"{candidate_score['final_score']:.6f}",
                "reasoning": reasoning,
            })
    
    print(f"✓ Submission created: {output_file}")
    print(f"  - Rows: {len(top_100)}")
    print(f"  - Score range: {top_100[0]['final_score']:.4f} to {top_100[-1]['final_score']:.4f}")
    
    return output_path

def create_detailed_analysis(output_file="team_redrob_detailed.csv"):
    """
    Create detailed analysis CSV with all scores
    """
    print(f"\nCreating detailed analysis...\n")
    
    ranked = rank_candidates()
    top_100 = ranked[:100]
    
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
        
        for rank, candidate_score in enumerate(top_100, 1):
            writer.writerow({
                "rank": rank,
                "candidate_id": candidate_score["candidate_id"],
                "final_score": f"{candidate_score['final_score']:.6f}",
                "retrieval_fit": f"{candidate_score['technical_fit']['retrieval_fit']:.4f}",
                "production_ai": f"{candidate_score['technical_fit']['production_ai']:.4f}",
                "yoe_fit": f"{candidate_score['technical_fit']['yoe_fit']:.4f}",
                "must_have_skills": f"{candidate_score['technical_fit']['must_have_skills']:.4f}",
                "vector_db_exp": f"{candidate_score['technical_fit']['vector_db_exp']:.4f}",
                "product_company": f"{candidate_score['technical_fit']['product_company']:.4f}",
                "ai_skill_count": f"{candidate_score['technical_fit']['ai_skill_count']:.4f}",
                "behavior_score": f"{candidate_score['behavior_score']:.4f}",
                "honeypot_penalty": f"{candidate_score['honeypot_penalty']:.4f}",
            })
    
    print(f"✓ Detailed analysis created: {output_file}")
    
    return output_path

if __name__ == "__main__":
    print("="*80)
    print("GENERATING SUBMISSION")
    print("="*80 + "\n")
    
    # Create main submission
    submission_file = create_submission()
    
    # Create detailed analysis
    detailed_file = create_detailed_analysis()
    
    print(f"\n{'='*80}")
    print("Files generated:")
    print(f"  - {submission_file.name}")
    print(f"  - {detailed_file.name}")
    print(f"{'='*80}")
