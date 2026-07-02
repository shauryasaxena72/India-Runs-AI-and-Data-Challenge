"""
Phase 8: Generate Reasoning
Create human-readable explanations for why candidates are ranked where they are
Must use REAL FACTS - no hallucinations
"""
import json
from pathlib import Path

def extract_real_signals(candidate):
    """
    Extract real facts from candidate profile to build reasoning
    """
    facts = {
        "name": candidate["profile"].get("anonymized_name", "Unknown"),
        "yoe": candidate["profile"]["years_of_experience"],
        "current_title": candidate["profile"]["current_title"],
        "current_company": candidate["profile"]["current_company"],
        "summary": candidate["profile"].get("summary", ""),
        "headline": candidate["profile"].get("headline", ""),
        "skills": {s["name"]: s["proficiency"] for s in candidate.get("skills", [])},
        "response_rate": candidate["redrob_signals"]["recruiter_response_rate"],
        "github_score": candidate["redrob_signals"]["github_activity_score"],
        "open_to_work": candidate["redrob_signals"]["open_to_work_flag"],
        "notice_period": candidate["redrob_signals"]["notice_period_days"],
        "interviews_completed": candidate["redrob_signals"]["interview_completion_rate"],
        "saved_by_recruiters": candidate["redrob_signals"]["saved_by_recruiters_30d"],
    }
    
    return facts

def find_retrieval_keywords_in_profile(facts):
    """
    Find evidence of retrieval/ranking work in profile
    """
    keywords = ["retrieval", "ranking", "recommendation", "search", "vector", "embedding", "semantic", "relevance"]
    
    summary_lower = facts["summary"].lower()
    headline_lower = facts["headline"].lower()
    
    found = []
    for keyword in keywords:
        if keyword in summary_lower or keyword in headline_lower:
            found.append(keyword)
    
    return found

def find_production_keywords_in_profile(facts):
    """
    Find evidence of production systems in profile
    """
    keywords = ["production", "deployed", "scale", "real users", "pipeline", "serving", "inference"]
    
    summary_lower = facts["summary"].lower()
    
    found = []
    for keyword in keywords:
        if keyword in summary_lower:
            found.append(keyword)
    
    return found

def find_ai_skills_in_profile(facts):
    """
    List AI skills candidate claims
    """
    ai_skill_keywords = ["llm", "nlp", "machine learning", "deep learning", "pytorch", "tensorflow", "python", "retrieval", "ranking"]
    
    found = []
    for skill_name in facts["skills"].keys():
        skill_lower = skill_name.lower()
        if any(ai_keyword in skill_lower for ai_keyword in ai_skill_keywords):
            found.append(f"{skill_name} ({facts['skills'][skill_name]})")
    
    return found

def generate_reasoning(candidate, score_result):
    """
    Generate natural language reasoning for a candidate's ranking
    Uses ONLY real facts from the profile
    """
    facts = extract_real_signals(candidate)
    
    reasoning_parts = []
    
    # YOE
    if facts["yoe"] >= 5 and facts["yoe"] <= 9:
        reasoning_parts.append(f"{facts['yoe']:.1f} years experience (ideal for JD)")
    elif facts["yoe"] >= 3 and facts["yoe"] < 15:
        reasoning_parts.append(f"{facts['yoe']:.1f} years experience")
    elif facts["yoe"] < 3:
        reasoning_parts.append(f"{facts['yoe']:.1f} years (less experienced)")
    else:
        reasoning_parts.append(f"{facts['yoe']:.1f} years (more senior)")
    
    # Retrieval/ranking fit
    retrieval_keywords = find_retrieval_keywords_in_profile(facts)
    if retrieval_keywords:
        reasoning_parts.append(f"Strong retrieval/ranking focus: {', '.join(retrieval_keywords)}")
    
    # Production systems
    prod_keywords = find_production_keywords_in_profile(facts)
    if prod_keywords:
        reasoning_parts.append(f"Deployed to production: {', '.join(prod_keywords)}")
    
    # AI skills
    ai_skills = find_ai_skills_in_profile(facts)
    if ai_skills:
        top_skills = ai_skills[:3]
        reasoning_parts.append(f"AI tech stack: {', '.join(top_skills)}")
    
    # Recruiter engagement
    if facts["response_rate"] >= 0.8:
        reasoning_parts.append(f"Highly responsive to recruiters ({facts['response_rate']:.0%} response rate)")
    elif facts["response_rate"] >= 0.5:
        reasoning_parts.append(f"Good recruiter engagement ({facts['response_rate']:.0%} response rate)")
    
    # GitHub
    if facts["github_score"] >= 8:
        reasoning_parts.append(f"Active on GitHub (score: {facts['github_score']:.1f})")
    
    # Notice period
    if facts["notice_period"] <= 30:
        reasoning_parts.append(f"Can join within {facts['notice_period']} days")
    elif facts["notice_period"] <= 60:
        reasoning_parts.append(f"Available in {facts['notice_period']} days")
    
    # Open to work
    if facts["open_to_work"]:
        reasoning_parts.append("Open to opportunities")
    
    # Interview completion
    if facts["interviews_completed"] >= 0.7:
        reasoning_parts.append(f"Strong interview completion rate ({facts['interviews_completed']:.0%})")
    
    # Saved by recruiters
    if facts["saved_by_recruiters"] >= 3:
        reasoning_parts.append(f"Saved by {facts['saved_by_recruiters']} recruiters (high interest)")
    elif facts["saved_by_recruiters"] >= 1:
        reasoning_parts.append(f"Saved by recruiters")
    
    # Combine with score info
    if score_result["honeypot_penalty"] > 0.1:
        honeypot_flags = [k for k, v in score_result['honeypot_details'].items() if v > 0.05]
        reasoning_parts.append(f"⚠️ Potential concerns: {', '.join(honeypot_flags)}")
    
    reasoning = "; ".join(reasoning_parts) + "."
    
    return reasoning

def load_candidates_map(candidates_file="candidates.jsonl"):
    """
    Load candidates into dict for quick lookup
    """
    candidates_path = Path(__file__).parent / candidates_file
    
    candidates_map = {}
    with open(candidates_path, "r", encoding="utf-8") as f:
        for line in f:
            candidate = json.loads(line)
            candidates_map[candidate["candidate_id"]] = candidate
    
    return candidates_map

def generate_reasoning_for_ranked(ranked_candidates):
    """
    Generate reasoning for all ranked candidates
    """
    # Load candidate profiles
    candidates_map = load_candidates_map()
    
    reasoning_list = []
    
    for score_result in ranked_candidates:
        candidate_id = score_result["candidate_id"]
        candidate = candidates_map[candidate_id]
        
        reasoning = generate_reasoning(candidate, score_result)
        
        reasoning_list.append({
            "candidate_id": candidate_id,
            "reasoning": reasoning,
        })
    
    return reasoning_list

if __name__ == "__main__":
    # Test with sample candidates
    print("Testing Reasoning Generation:\n")
    
    sample_file = Path(__file__).parent / "sample_candidates.json"
    with open(sample_file) as f:
        samples = json.load(f)
    
    # Create dummy score results for testing
    from candidate_ranker import compute_final_score
    
    for candidate in samples[:2]:
        score_result = compute_final_score(candidate)
        reasoning = generate_reasoning(candidate, score_result)
        print(f"Candidate {candidate['candidate_id']}:")
        print(f"  {reasoning}")
        print()
