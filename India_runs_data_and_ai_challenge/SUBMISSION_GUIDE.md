# 🚀 Submission Guide

## Phase 1: Update Metadata (2 minutes)

Edit `submission_metadata.yaml` and replace:
```yaml
team_name: "Your Team Name"
primary_contact:
  name: "Your Full Name"
  email: "your.email@example.com"
  phone: "+91-XXXXXXXXXX"
github_repo: "https://github.com/YOUR_USERNAME/redrob-ranker"
sandbox_link: "https://huggingface.co/spaces/YOUR_USERNAME/redrob-ranker"
```

---

## Phase 2: Create GitHub Repository (5 minutes)

### Step 1: Go to GitHub
1. Log in to [github.com](https://github.com)
2. Click **New** → Create repository
3. Name: `redrob-ranker`
4. Description: "Intelligent candidate ranker for Redrob Hackathon"
5. Make it **Public**
6. Click **Create repository**

### Step 2: Push Your Code

Open PowerShell in your project folder and run:

```powershell
Set-Location -LiteralPath "D:\Portfolio\Data Science Projects\INDIA Run Hackathon\[PUB] India_runs_data_and_ai_challenge\[PUB] India_runs_data_and_ai_challenge\India_runs_data_and_ai_challenge"

git init
git config user.email "your.email@example.com"
git config user.name "Your Name"
git add .
git commit -m "Redrob candidate ranking solution - 100 ranked candidates"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/redrob-ranker.git
git push -u origin main
```

**GitHub will then show you:**
```
 * [new branch]      main -> main
Branch 'main' is set up to track 'origin/main'.
```

Copy your repo URL: `https://github.com/YOUR_USERNAME/redrob-ranker`

---

## Phase 3: Create HuggingFace Spaces (5 minutes)

### Step 1: Go to HuggingFace
1. Log in to [huggingface.co](https://huggingface.co)
2. Click **New** → New Space
3. Name: `redrob-ranker`
4. License: Choose one
5. Space SDK: **Streamlit**
6. Visibility: **Public**
7. Click **Create Space**

### Step 2: Upload Files
1. Click **Files** tab
2. Click **Add file** → Upload files
3. Upload these files:
   - `app.py`
   - `team_redrob_submission.csv`
   - `README.md`
   - `requirements.txt` (create below)

### Step 3: Create requirements.txt
Create a file called `requirements.txt` in your project:

```
streamlit>=1.28
pandas>=2.0
```

Then upload it to HuggingFace.

**Your Space will auto-deploy** in ~1 minute and show:
```
https://huggingface.co/spaces/YOUR_USERNAME/redrob-ranker
```

---

## Phase 4: Portal Submission

### Go to Hackathon Portal
1. Navigate to [hackathon submission portal](https://redrob-challenge.com/submit) ← *Update with actual URL*
2. Log in / Sign up
3. Fill out form:
   - Team name: (from metadata.yaml)
   - Primary contact: (from metadata.yaml)
   - Email: (from metadata.yaml)

### Upload Submission (Stage 1)
- **CSV File:** `team_redrob_submission.csv`
- **GitHub Repo:** `https://github.com/YOUR_USERNAME/redrob-ranker`
- **Sandbox Link:** `https://huggingface.co/spaces/YOUR_USERNAME/redrob-ranker`
- **Reproduce Command:** `python submission_generator_optimized.py`
- Accept terms & submit

---

## Phase 5: What Happens Next

### If Selected for Stage 2:
- Organizers verify your GitHub repo is public
- Test your sandbox link works

### If Selected for Stage 3:
- Organizers verify:
  - `submission_metadata.yaml` matches portal info
  - `reproduce_command` runs end-to-end in 5 min
  - CSV format is correct

### If Selected for Top 50+:
- Code review
- Technical interview
- Final presentations

---

## Checklist Before Submitting

- ✅ `submission_metadata.yaml` - Updated with your info
- ✅ `team_redrob_submission.csv` - Generated and validated
- ✅ `app.py` - Created (Streamlit demo)
- ✅ `.gitignore` - Created
- ✅ `README.md` - Already exists
- ⏳ GitHub repo - Public
- ⏳ HuggingFace Space - Live
- ⏳ Portal submission - Complete

---

## Quick Reference

**Your GitHub Username:** _______________

**Your Email:** _______________

**GitHub Repo URL:** https://github.com/YOUR_USERNAME/redrob-ranker

**HuggingFace Space URL:** https://huggingface.co/spaces/YOUR_USERNAME/redrob-ranker

---

## Troubleshooting

### Git push fails
```
# Check remote
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/redrob-ranker.git
```

### HuggingFace Space not loading
- Check `app.py` is uploaded
- Check `team_redrob_submission.csv` is uploaded
- Wait 2-3 minutes for deployment
- Check Logs tab for errors

### CSV validation fails
```powershell
python validate_submission.py team_redrob_submission.csv
```

Should output: `Submission is valid.`

---

## Questions?

Check these files for help:
- `README.md` - Architecture & approach
- `COMPLETION_SUMMARY.md` - What was built
- `INDEX.md` - File organization

Good luck! 🚀
