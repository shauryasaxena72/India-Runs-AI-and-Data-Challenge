"""
Show top candidates from submission
"""
import csv

with open('team_redrob_submission.csv') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i >= 10:
            break
        print(f"{row['rank']}: {row['candidate_id']} - Score: {row['score']}")
        print(f"   Reasoning: {row['reasoning'][:100]}...")
        print()
