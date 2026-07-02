import streamlit as st
import subprocess
from pathlib import Path

st.title("Redrob Ranker - Sandbox")
st.write("Run the ranker on a small sample and download the submission CSV.")

sample_file = "sample_candidates.jsonl"
output_file = "team_redrob_submission.csv"

if not Path(sample_file).exists():
    st.warning(f"Sample file {sample_file} not found in the repo.")

if st.button("Run ranker"):
    with st.spinner("Running submission_generator_optimized.py..."):
        try:
            # Run the ranker script
            result = subprocess.run(["python", "submission_generator_optimized.py"], capture_output=True, text=True, check=True)
            st.success("Ranker finished successfully.")
            st.code(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error("Ranker failed — see logs below.")
            st.code(e.stdout + "\n" + e.stderr)

# Provide link to download output if present
if Path(output_file).exists():
    st.download_button("Download submission CSV", data=Path(output_file).read_bytes(), file_name=output_file)
else:
    st.info("Run the ranker to generate the submission CSV (team_redrob_submission.csv).")
