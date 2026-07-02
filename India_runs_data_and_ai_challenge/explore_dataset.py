"""
Phase 1: Understand the Dataset
Analyze the candidate pool to inform scoring weights
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

# Load candidates
CANDIDATES_FILE = Path(__file__).parent / "candidates.jsonl"

candidates = []
with open(CANDIDATES_FILE, "r", encoding="utf-8") as f:
    for line in f:
        candidates.append(json.loads(line))

print(f"\n{'='*70}")
print(f"DATASET OVERVIEW")
print(f"{'='*70}")
print(f"Total candidates: {len(candidates)}")

# 1. Years of experience stats
yoe_list = [c["profile"]["years_of_experience"] for c in candidates]
print(f"\nYears of Experience:")
print(f"  - Min: {min(yoe_list):.1f}")
print(f"  - Max: {max(yoe_list):.1f}")
print(f"  - Avg: {sum(yoe_list)/len(yoe_list):.2f}")
print(f"  - Median: {sorted(yoe_list)[len(yoe_list)//2]:.1f}")

# Distribution by buckets
yoe_buckets = defaultdict(int)
for yoe in yoe_list:
    if yoe < 2: bucket = "0-2"
    elif yoe < 5: bucket = "2-5"
    elif yoe < 9: bucket = "5-9"
    elif yoe < 15: bucket = "9-15"
    else: bucket = "15+"
    yoe_buckets[bucket] += 1

print(f"  - Distribution:")
for bucket in ["0-2", "2-5", "5-9", "9-15", "15+"]:
    if bucket in yoe_buckets:
        pct = 100 * yoe_buckets[bucket] / len(candidates)
        print(f"      {bucket}: {yoe_buckets[bucket]:4d} ({pct:5.1f}%)")

# 2. Current titles (top 15)
titles = Counter([c["profile"]["current_title"] for c in candidates])
print(f"\nTop Job Titles:")
for title, count in titles.most_common(15):
    pct = 100 * count / len(candidates)
    print(f"  - {title}: {count:4d} ({pct:5.1f}%)")

# 3. Skills distribution
all_skills = defaultdict(int)
skill_proficiency = defaultdict(lambda: defaultdict(int))

for c in candidates:
    for skill in c.get("skills", []):
        all_skills[skill["name"]] += 1
        skill_proficiency[skill["name"]][skill["proficiency"]] += 1

print(f"\nTop Skills (overall presence):")
for skill, count in sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:20]:
    pct = 100 * count / len(candidates)
    profs = skill_proficiency[skill]
    print(f"  - {skill}: {count:4d} ({pct:5.1f}%) | expert: {profs.get('expert', 0):3d}, advanced: {profs.get('advanced', 0):3d}")

# 4. Behavioral signals
print(f"\nBehavioral Signals Summary:")

# Open to work
open_to_work = sum(1 for c in candidates if c["redrob_signals"]["open_to_work_flag"])
print(f"  - Open to work: {open_to_work}/{len(candidates)} ({100*open_to_work/len(candidates):.1f}%)")

# Response rate distribution
response_rates = [c["redrob_signals"]["recruiter_response_rate"] for c in candidates]
print(f"  - Response Rate (recruiter messages):")
print(f"      - Min: {min(response_rates):.2f}")
print(f"      - Max: {max(response_rates):.2f}")
print(f"      - Mean: {sum(response_rates)/len(response_rates):.2f}")

# Response rate buckets
response_buckets = {">0.8": 0, "0.5-0.8": 0, "0.1-0.5": 0, "<0.1": 0}
for rr in response_rates:
    if rr > 0.8: response_buckets[">0.8"] += 1
    elif rr >= 0.5: response_buckets["0.5-0.8"] += 1
    elif rr >= 0.1: response_buckets["0.1-0.5"] += 1
    else: response_buckets["<0.1"] += 1
print(f"      - Distribution:")
for bucket in [">0.8", "0.5-0.8", "0.1-0.5", "<0.1"]:
    pct = 100 * response_buckets[bucket] / len(candidates)
    print(f"          {bucket}: {response_buckets[bucket]:4d} ({pct:5.1f}%)")

# GitHub activity
github_scores = [c["redrob_signals"]["github_activity_score"] for c in candidates]
print(f"  - GitHub Activity Score:")
print(f"      - Min: {min(github_scores):.1f}")
print(f"      - Max: {max(github_scores):.1f}")
print(f"      - Mean: {sum(github_scores)/len(github_scores):.2f}")

# Interview completion rate
interview_rates = [c["redrob_signals"]["interview_completion_rate"] for c in candidates]
print(f"  - Interview Completion Rate:")
print(f"      - Mean: {sum(interview_rates)/len(interview_rates):.2f}")

# Saved by recruiters
saved_by_recruiters = sum(1 for c in candidates if c["redrob_signals"]["saved_by_recruiters_30d"] > 0)
avg_saved = sum(c["redrob_signals"]["saved_by_recruiters_30d"] for c in candidates) / len(candidates)
print(f"  - Saved by Recruiters (30d):")
print(f"      - Candidates saved at least once: {saved_by_recruiters}/{len(candidates)} ({100*saved_by_recruiters/len(candidates):.1f}%)")
print(f"      - Average saves per candidate: {avg_saved:.2f}")

# Notice period
notice_periods = [c["redrob_signals"]["notice_period_days"] for c in candidates]
print(f"  - Notice Period (days):")
print(f"      - Mean: {sum(notice_periods)/len(notice_periods):.1f}")
notice_buckets = {"0-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
for np in notice_periods:
    if np <= 30: notice_buckets["0-30"] += 1
    elif np <= 60: notice_buckets["31-60"] += 1
    elif np <= 90: notice_buckets["61-90"] += 1
    else: notice_buckets["90+"] += 1
print(f"      - Distribution:")
for bucket in ["0-30", "31-60", "61-90", "90+"]:
    pct = 100 * notice_buckets[bucket] / len(candidates)
    print(f"          {bucket} days: {notice_buckets[bucket]:4d} ({pct:5.1f}%)")

# 5. Company size distribution (current)
company_sizes = Counter([c["profile"]["current_company_size"] for c in candidates])
print(f"\nCurrent Company Size Distribution:")
for size, count in company_sizes.most_common():
    pct = 100 * count / len(candidates)
    print(f"  - {size}: {count:4d} ({pct:5.1f}%)")

# 6. Current industry
industries = Counter([c["profile"]["current_industry"] for c in candidates])
print(f"\nTop Current Industries:")
for industry, count in industries.most_common(10):
    pct = 100 * count / len(candidates)
    print(f"  - {industry}: {count:4d} ({pct:5.1f}%)")

print(f"\n{'='*70}\n")
