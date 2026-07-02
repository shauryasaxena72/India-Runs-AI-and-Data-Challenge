"""
Phase 4: Behavioral Signals Scoring
Score candidate engagement and behavioral signals
Most teams underuse these - huge opportunity!
"""
from datetime import datetime, timedelta

def score_open_to_work(candidate):
    """
    Open to Work Flag: +1.0 if true, +0 if false
    """
    if candidate["redrob_signals"]["open_to_work_flag"]:
        return 1.0
    return 0.0

def score_response_rate(candidate):
    """
    Response Rate to Recruiter Messages:
    0.8+ -> 1.0 (excellent)
    0.5-0.8 -> 0.8 (good)
    0.1-0.5 -> 0.4 (moderate)
    <0.1 -> 0.0 (bad)
    """
    rr = candidate["redrob_signals"]["recruiter_response_rate"]
    
    if rr >= 0.8:
        return 1.0
    elif rr >= 0.5:
        return 0.8
    elif rr >= 0.1:
        return 0.4
    else:
        return 0.0

def score_response_time(candidate):
    """
    Response Time (hours):
    Faster is better - logarithmic scoring
    <24 hours -> 1.0
    24-72 hours -> 0.8
    72-168 hours (1 week) -> 0.5
    >1 week -> 0.2
    """
    hours = candidate["redrob_signals"]["avg_response_time_hours"]
    
    if hours <= 24:
        return 1.0
    elif hours <= 72:
        return 0.8
    elif hours <= 168:
        return 0.5
    else:
        return 0.2

def score_recent_activity(candidate):
    """
    Recent Activity:
    Check last login date relative to signup
    Active in last 7 days -> 1.0
    Active in last 30 days -> 0.8
    Active in last 90 days -> 0.4
    Inactive >90 days -> 0.0
    """
    try:
        last_active = datetime.strptime(candidate["redrob_signals"]["last_active_date"], "%Y-%m-%d")
        today = datetime.now()
        days_since_active = (today - last_active).days
        
        if days_since_active <= 7:
            return 1.0
        elif days_since_active <= 30:
            return 0.8
        elif days_since_active <= 90:
            return 0.4
        else:
            return 0.0
    except:
        return 0.2

def score_saved_by_recruiters(candidate):
    """
    Saved by Recruiters (30d):
    If saved at least once -> 0.8
    If saved multiple times (3+) -> 1.0
    Not saved -> 0.0
    """
    saved_count = candidate["redrob_signals"]["saved_by_recruiters_30d"]
    
    if saved_count >= 3:
        return 1.0
    elif saved_count >= 1:
        return 0.8
    else:
        return 0.0

def score_interview_completion(candidate):
    """
    Interview Completion Rate:
    Normalize to 0-1 scale
    >0.7 = strong candidate, follows through
    """
    rate = candidate["redrob_signals"]["interview_completion_rate"]
    # Already 0-1 scale
    return rate

def score_github_activity(candidate):
    """
    GitHub Activity Score:
    Normalize to 0-1 based on activity distribution
    Expected range: 0-15 or so
    """
    score = candidate["redrob_signals"]["github_activity_score"]
    
    # Normalize (assuming max ~15)
    normalized = min(1.0, score / 12.0)
    return normalized

def score_notice_period(candidate):
    """
    Notice Period:
    JD prefers <30 days
    0-30 days -> 1.0
    31-60 days -> 0.8
    61-90 days -> 0.4
    90+ days -> 0.0
    """
    days = candidate["redrob_signals"]["notice_period_days"]
    
    if days <= 30:
        return 1.0
    elif days <= 60:
        return 0.8
    elif days <= 90:
        return 0.4
    else:
        return 0.0

def score_profile_completeness(candidate):
    """
    Profile Completeness Score:
    Already 0-100 scale
    """
    score = candidate["redrob_signals"]["profile_completeness_score"]
    return score / 100.0

def score_connection_count(candidate):
    """
    Connection Count:
    More connections = more engaged network
    Expected range: 0-500+
    Normalize: 100+ = 0.8, 50-100 = 0.5, <50 = 0.3
    """
    connections = candidate["redrob_signals"]["connection_count"]
    
    if connections >= 200:
        return 1.0
    elif connections >= 100:
        return 0.8
    elif connections >= 50:
        return 0.5
    else:
        return 0.3

def compute_behavior_score(candidate):
    """
    Compute overall behavior score (normalized 0-1)
    Weights reflect engagement and availability signals
    """
    
    components = {
        "open_to_work": score_open_to_work(candidate),
        "response_rate": score_response_rate(candidate),
        "response_time": score_response_time(candidate),
        "recent_activity": score_recent_activity(candidate),
        "saved_by_recruiters": score_saved_by_recruiters(candidate),
        "interview_completion": score_interview_completion(candidate),
        "github_activity": score_github_activity(candidate),
        "notice_period": score_notice_period(candidate),
    }
    
    # Weights (sum to 1.0)
    weights = {
        "open_to_work": 0.10,
        "response_rate": 0.20,
        "response_time": 0.10,
        "recent_activity": 0.10,
        "saved_by_recruiters": 0.10,
        "interview_completion": 0.15,
        "github_activity": 0.10,
        "notice_period": 0.15,
    }
    
    weighted_score = sum(components[key] * weights[key] for key in components)
    
    return {
        "behavior_score": weighted_score,
        "components": components,
    }

if __name__ == "__main__":
    # Test with sample data
    import json
    from pathlib import Path
    
    sample_file = Path(__file__).parent / "sample_candidates.json"
    with open(sample_file) as f:
        samples = json.load(f)
    
    print("Sample Behavior Score Calculation:\n")
    for candidate in samples[:1]:
        result = compute_behavior_score(candidate)
        print(f"Candidate: {candidate['candidate_id']}")
        print(f"  Overall Behavior Score: {result['behavior_score']:.2f}")
        print(f"  Components:")
        for key, value in result['components'].items():
            print(f"    - {key}: {value:.2f}")
