@echo off
REM Redrob Hackathon - Quick GitHub Setup Script
REM This script automates the git repo creation and push

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo  REDROB HACKATHON - GITHUB SETUP
echo ====================================================
echo.

REM Ask for user inputs
set /p github_user="Enter your GitHub username: "
set /p your_name="Enter your full name: "
set /p your_email="Enter your email: "

REM Validate inputs
if "!github_user!"=="" (
    echo Error: GitHub username required
    exit /b 1
)

if "!your_email!"=="" (
    echo Error: Email required
    exit /b 1
)

echo.
echo ====================================================
echo  STEP 1: Configure Git
echo ====================================================
echo.

git config user.email "!your_email!"
git config user.name "!your_name!"

echo.
echo ====================================================
echo  STEP 2: Initialize Repository
echo ====================================================
echo.

git init
git add .
git commit -m "Redrob candidate ranking solution - 100 ranked candidates"
git branch -M main

echo.
echo ====================================================
echo  STEP 3: Add Remote (You'll need to create the repo first)
echo ====================================================
echo.

echo BEFORE CONTINUING:
echo 1. Go to https://github.com/new
echo 2. Create repository named "redrob-ranker"
echo 3. Press Enter here to continue...

pause

git remote add origin https://github.com/!github_user!/redrob-ranker.git
git push -u origin main

echo.
echo ====================================================
echo  SUCCESS!
echo ====================================================
echo.
echo Your repo: https://github.com/!github_user!/redrob-ranker
echo.
echo NEXT STEPS:
echo 1. Go to https://huggingface.co/spaces
echo 2. Create new Space "redrob-ranker" (Streamlit)
echo 3. Upload: app.py, team_redrob_submission.csv, README.md, requirements.txt
echo 4. Go to hackathon portal and submit
echo.
echo See SUBMISSION_GUIDE.md for detailed instructions
echo.
echo ====================================================
echo.

pause
