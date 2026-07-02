"""
Phase 5: Honeypot Detection
Identify suspicious candidates with impossible/exaggerated claims
Very important - helps eliminate noise from dataset
"""

def check_impossible_skill_duration(candidate):
    """
    Check: Skill duration vs Years of Experience
    Example: YOE = 3 years but skill marked as 70 months = impossible
    """
    yoe = candidate["profile"]["years_of_experience"]
    yoe_months = yoe * 12
    
    penalty = 0.0
    
    for skill in candidate.get("skills", []):
        duration_months = skill.get("duration_months", 0)
        
        # If skill duration > YOE + 6 months buffer, it's suspicious
        if duration_months > yoe_months + 6:
            penalty += 0.05
    
    # Cap penalty at 0.3
    return min(0.3, penalty)

def check_too_many_expert_skills(candidate):
    """
    Check: Candidates claiming too many expert-level skills (>10)
    Suspicious - likely inflated claims
    """
    expert_skills = sum(
        1 for skill in candidate.get("skills", [])
        if skill.get("proficiency") == "expert"
    )
    
    if expert_skills > 10:
        # Penalty increases with count
        return min(0.3, 0.05 * (expert_skills - 10))
    
    return 0.0

def check_career_timeline_issues(candidate):
    """
    Check: Sum of job durations vs claimed Years of Experience
    """
    yoe_claimed = candidate["profile"]["years_of_experience"]
    
    # Calculate total duration of all jobs
    total_months = 0
    for job in candidate.get("career_history", []):
        total_months += job.get("duration_months", 0)
    
    total_years_worked = total_months / 12.0
    
    # Allow 1 year discrepancy for gaps/education/unemployed periods
    discrepancy = abs(total_years_worked - yoe_claimed)
    
    if discrepancy > 2.0:  # More than 2 years off
        penalty = min(0.2, discrepancy / 10.0)
        return penalty
    
    return 0.0

def check_exaggerated_endorsements(candidate):
    """
    Check: Endorsements way above network size
    If endorsements > connections * 2, suspicious
    """
    endorsements = candidate["redrob_signals"]["endorsements_received"]
    connections = candidate["redrob_signals"]["connection_count"]
    
    if connections > 0 and endorsements > connections * 2:
        ratio = endorsements / connections
        penalty = min(0.1, 0.01 * (ratio - 2))
        return penalty
    
    return 0.0

def check_skill_endorsement_mismatch(candidate):
    """
    Check: High endorsements on skills not claimed
    or claimed skills with zero endorsements but marked expert
    """
    penalty = 0.0
    
    for skill in candidate.get("skills", []):
        endorsements = skill.get("endorsements", 0)
        proficiency = skill.get("proficiency", "beginner")
        
        # Expert skill with 0 endorsements is suspicious
        if proficiency == "expert" and endorsements == 0:
            penalty += 0.02
    
    return min(0.15, penalty)

def check_profile_inconsistencies(candidate):
    """
    Check: Profile claim inconsistencies
    - Current role vs skills
    - Headline vs summary mismatch
    """
    penalty = 0.0
    
    # Check if someone claims AI expertise but is HR/Operations manager
    current_title = candidate["profile"]["current_title"].lower()
    summary = candidate["profile"]["summary"].lower()
    
    # HR-type roles shouldn't claim technical depth
    hr_keywords = ["hr manager", "operations", "recruiter", "administrative", "pm", "product manager"]
    
    if any(keyword in current_title for keyword in hr_keywords):
        technical_keywords = ["deep learning", "machine learning", "python", "engineering"]
        if summary.count("ai") > 3 or any(keyword in summary for keyword in technical_keywords):
            # Person claims to be non-technical but uses tons of AI terminology
            penalty += 0.15
    
    return penalty

def check_recent_spike_in_claims(candidate):
    """
    Check: Recent additions of skills that don't match job history
    Example: Added 5 AI skills last month but been in HR for 3 years
    """
    penalty = 0.0
    
    # Check if candidate's career is purely non-technical but has many technical skills
    is_technical_career = False
    for job in candidate.get("career_history", []):
        title = job.get("title", "").lower()
        tech_keywords = ["engineer", "developer", "scientist", "analyst"]
        if any(keyword in title for keyword in tech_keywords):
            is_technical_career = True
            break
    
    if not is_technical_career:
        # Non-technical career but has many expert AI skills
        expert_ai_skills = 0
        ai_skills = ["llm", "nlp", "deep learning", "machine learning", "python", "pytorch"]
        
        for skill in candidate.get("skills", []):
            if any(ai in skill["name"].lower() for ai in ai_skills):
                if skill.get("proficiency") in ["advanced", "expert"]:
                    expert_ai_skills += 1
        
        if expert_ai_skills > 3:
            penalty += 0.1
    
    return penalty

def compute_honeypot_penalty(candidate):
    """
    Compute total honeypot penalty (0-1)
    Penalties are subtracted from final score
    """
    
    penalties = {
        "impossible_skill_duration": check_impossible_skill_duration(candidate),
        "too_many_expert_skills": check_too_many_expert_skills(candidate),
        "career_timeline_issues": check_career_timeline_issues(candidate),
        "exaggerated_endorsements": check_exaggerated_endorsements(candidate),
        "skill_endorsement_mismatch": check_skill_endorsement_mismatch(candidate),
        "profile_inconsistencies": check_profile_inconsistencies(candidate),
        "recent_skill_spike": check_recent_spike_in_claims(candidate),
    }
    
    total_penalty = sum(penalties.values())
    
    # Cap total penalty at 0.4 (don't eliminate candidates entirely)
    total_penalty = min(0.4, total_penalty)
    
    return {
        "honeypot_penalty": total_penalty,
        "components": penalties,
    }

if __name__ == "__main__":
    # Test with sample data
    import json
    from pathlib import Path
    
    sample_file = Path(__file__).parent / "sample_candidates.json"
    with open(sample_file) as f:
        samples = json.load(f)
    
    print("Sample Honeypot Detection:\n")
    for candidate in samples[:2]:
        result = compute_honeypot_penalty(candidate)
        print(f"Candidate: {candidate['candidate_id']}")
        print(f"  Honeypot Penalty: {result['honeypot_penalty']:.3f}")
        print(f"  Breakdown:")
        for key, value in result['components'].items():
            if value > 0:
                print(f"    - {key}: {value:.3f}")
