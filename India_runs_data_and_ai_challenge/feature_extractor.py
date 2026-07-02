"""
Phase 3: Candidate Feature Extraction
For each candidate, compute technical fit features based on JD requirements
"""
from jd_features import (
    must_have, good_to_have, negative, vector_databases, 
    production_keywords, core_retrieval_keywords, JD_SIGNALS
)
import re

def normalize_text(text):
    """Normalize text for keyword matching"""
    if not text:
        return ""
    return text.lower().strip()

def count_keyword_matches(text, keywords, case_sensitive=False):
    """Count how many keywords appear in text"""
    if not text:
        return 0
    
    text = normalize_text(text)
    count = 0
    for keyword in keywords:
        keyword = normalize_text(keyword)
        if keyword in text:
            count += 1
    return count

def find_keyword_matches(text, keywords):
    """Return which keywords are found in text"""
    if not text:
        return []
    
    text = normalize_text(text)
    found = []
    for keyword in keywords:
        keyword = normalize_text(keyword)
        if keyword in text:
            found.append(keyword)
    return found

def feature_1_years_experience_fit(candidate):
    """
    Feature 1: Years Experience Fit
    JD: 5-9 years ideal
    """
    yoe = candidate["profile"]["years_of_experience"]
    
    ideal_min = JD_SIGNALS["yoe_ideal_min"]
    ideal_max = JD_SIGNALS["yoe_ideal_max"]
    acceptable_min = JD_SIGNALS["yoe_acceptable_min"]
    acceptable_max = JD_SIGNALS["yoe_acceptable_max"]
    
    if ideal_min <= yoe <= ideal_max:
        score = 1.0
    elif acceptable_min <= yoe <= acceptable_max:
        # Linear interpolation for acceptable range
        dist_ideal = min(
            abs(yoe - ideal_min),
            abs(yoe - ideal_max)
        )
        dist_boundary = min(
            abs(yoe - acceptable_min),
            abs(yoe - acceptable_max)
        )
        # Score between 0.5 and 1.0
        score = 0.5 + (0.5 * (1 - dist_ideal / (ideal_max - ideal_min)))
    else:
        # Penalize heavily for too junior or too senior
        if yoe < acceptable_min:
            score = max(0, yoe / acceptable_min * 0.5)
        else:
            score = max(0, 1 - (yoe - acceptable_max) / (acceptable_max * 0.5))
    
    return max(0, min(1, score))

def feature_2_ai_skill_count(candidate):
    """
    Feature 2: AI Skill Count
    Count presence of key AI skills
    """
    ai_skills = [
        "llm",
        "nlp",
        "retrieval",
        "ranking",
        "python",
        "machine learning",
        "deep learning",
        "vector",
        "embeddings",
        "rag",
        "recommendation",
        "bert",
        "transformer",
        "pytorch",
        "tensorflow",
    ]
    
    candidate_skills = {s["name"].lower() for s in candidate.get("skills", [])}
    
    # Count matches
    count = sum(1 for skill in ai_skills if any(skill in cs for cs in candidate_skills))
    
    # Normalize to 0-1 (cap at 10 skills = 1.0)
    score = min(1.0, count / 10)
    
    return score

def feature_3_retrieval_fit(candidate):
    """
    Feature 3: Retrieval & Ranking Focus
    Search career descriptions, summary, headline for retrieval/ranking keywords
    Huge importance per JD
    """
    texts_to_search = [
        candidate["profile"].get("headline", ""),
        candidate["profile"].get("summary", ""),
        candidate["profile"].get("current_title", ""),
    ]
    
    # Also search career history descriptions
    for job in candidate.get("career_history", []):
        texts_to_search.append(job.get("description", ""))
    
    combined_text = " ".join(texts_to_search)
    
    # Count core retrieval keyword matches
    match_count = count_keyword_matches(combined_text, core_retrieval_keywords)
    
    # Normalize: expect 2+ matches for good fit, 4+ for excellent
    if match_count >= 4:
        score = 1.0
    elif match_count >= 2:
        score = 0.7
    elif match_count >= 1:
        score = 0.4
    else:
        score = 0.0
    
    return score

def feature_4_vector_db_experience(candidate):
    """
    Feature 4: Vector Database Experience
    Look for specific vector database technologies
    """
    candidate_skills = {s["name"].lower() for s in candidate.get("skills", [])}
    
    vdb_found = [vdb for vdb in vector_databases 
                 if any(vdb.lower() in cs for cs in candidate_skills)]
    
    # Normalize: 1+ = 0.5, 2+ = 0.8, 3+ = 1.0
    if len(vdb_found) >= 3:
        score = 1.0
    elif len(vdb_found) >= 2:
        score = 0.8
    elif len(vdb_found) >= 1:
        score = 0.5
    else:
        score = 0.0
    
    return score

def feature_5_production_ai(candidate):
    """
    Feature 5: Production AI Systems Experience
    Look for keywords indicating production/deployed systems at scale
    """
    texts_to_search = [
        candidate["profile"].get("headline", ""),
        candidate["profile"].get("summary", ""),
    ]
    
    for job in candidate.get("career_history", []):
        texts_to_search.append(job.get("description", ""))
        texts_to_search.append(job.get("title", ""))
    
    combined_text = " ".join(texts_to_search)
    
    match_count = count_keyword_matches(combined_text, production_keywords)
    
    # Scoring: 0 = theoretical only, 1+ = production experience, 3+ = strong
    if match_count >= 3:
        score = 1.0
    elif match_count >= 1:
        score = 0.6
    else:
        score = 0.0
    
    return score

def feature_6_product_company_signal(candidate):
    """
    Feature 6: Product Company Signal
    Positive: startup, saas, product companies
    Negative: only TCS, Infosys, Wipro, etc. (entire career)
    """
    positive_keywords = ["startup", "saas", "product", "fintech", "tech", "platform"]
    negative_keywords = ["tcs", "infosys", "wipro", "cognizant", "accenture", "capgemini"]
    
    career = candidate.get("career_history", [])
    
    # Check industries and company names
    positive_count = 0
    negative_count = 0
    
    for job in career:
        company_name = normalize_text(job.get("company", ""))
        industry = normalize_text(job.get("industry", ""))
        
        # Check for positive signals
        if any(pos in company_name or pos in industry for pos in positive_keywords):
            positive_count += 1
        
        # Check for negative signals (entire career only)
        if any(neg in company_name for neg in negative_keywords):
            negative_count += 1
    
    # If entire career is just big consultancy, penalize heavily
    if negative_count == len(career) and len(career) > 0:
        score = 0.0
    elif positive_count > 0:
        score = 0.8
    elif len(career) > 0:
        score = 0.3
    else:
        score = 0.0
    
    return score

def feature_7_must_have_skills(candidate):
    """
    Bonus: Must Have Skills
    Check for Python and core retrieval/ranking skills
    """
    candidate_skills = {s["name"].lower() for s in candidate.get("skills", [])}
    
    must_have_found = sum(
        1 for skill in must_have 
        if any(skill.lower() in cs for cs in candidate_skills)
    )
    
    # At least 3 must-haves = 0.5 baseline, 5+ = 1.0
    if must_have_found >= 5:
        score = 1.0
    elif must_have_found >= 3:
        score = 0.7
    elif must_have_found >= 1:
        score = 0.3
    else:
        score = 0.0
    
    return score

def extract_features(candidate):
    """
    Extract all features for a candidate
    Returns dict with all feature scores
    """
    features = {
        "candidate_id": candidate["candidate_id"],
        "yoe_fit": feature_1_years_experience_fit(candidate),
        "ai_skill_count": feature_2_ai_skill_count(candidate),
        "retrieval_fit": feature_3_retrieval_fit(candidate),
        "vector_db_exp": feature_4_vector_db_experience(candidate),
        "production_ai": feature_5_production_ai(candidate),
        "product_company": feature_6_product_company_signal(candidate),
        "must_have_skills": feature_7_must_have_skills(candidate),
    }
    
    return features

if __name__ == "__main__":
    # Quick test with sample candidate
    import json
    from pathlib import Path
    
    sample_file = Path(__file__).parent / "sample_candidates.json"
    with open(sample_file) as f:
        samples = json.load(f)
    
    print("Sample Feature Extraction:\n")
    for candidate in samples[:2]:
        features = extract_features(candidate)
        print(f"\nCandidate: {candidate['candidate_id']}")
        print(f"  YOE Fit: {features['yoe_fit']:.2f}")
        print(f"  AI Skill Count: {features['ai_skill_count']:.2f}")
        print(f"  Retrieval Fit: {features['retrieval_fit']:.2f}")
        print(f"  Vector DB Exp: {features['vector_db_exp']:.2f}")
        print(f"  Production AI: {features['production_ai']:.2f}")
        print(f"  Product Company: {features['product_company']:.2f}")
        print(f"  Must Have Skills: {features['must_have_skills']:.2f}")
