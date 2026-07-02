import json

path = r"D:\Portfolio\Data Science Projects\INDIA Run Hackathon\[PUB] India_runs_data_and_ai_challenge\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge\sample_candidates.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Candidates:", len(data))

skills_counts = []
yoe = []

for c in data:
    skills_counts.append(len(c["skills"]))
    yoe.append(c["profile"]["years_of_experience"])

print("Min skills:", min(skills_counts))
print("Max skills:", max(skills_counts))
print("Avg skills:", sum(skills_counts)/len(skills_counts))

print("Min YOE:", min(yoe))
print("Max YOE:", max(yoe))
print("Avg YOE:", sum(yoe)/len(yoe))