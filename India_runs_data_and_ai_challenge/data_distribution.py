import json

path = r"D:\Portfolio\Data Science Projects\INDIA Run Hackathon\[PUB] India_runs_data_and_ai_challenge\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\sample_candidates.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Candidates:", len(data))

cand = data[0]

print("\nTop-level keys:")
print(cand.keys())

print("\nSkills count:")
print(len(cand["skills"]))

print("\nCareer entries:")
print(len(cand["career_history"]))