import streamlit as st
import csv
import pandas as pd

st.set_page_config(page_title="Redrob Ranker", page_icon="🔍", layout="wide")

st.title("🔍 Redrob Candidate Ranker")
st.subtitle("AI Engineers - Retrieval & Ranking Specialists")

# Load submission
try:
    with open("team_redrob_submission.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Ranked", len(rows))
    with col2:
        st.metric("Top Score", rows[0]["score"] if rows else "N/A")
    with col3:
        st.metric("Bottom Score", rows[-1]["score"] if rows else "N/A")
    with col4:
        st.metric("Spread", f"{float(rows[0]['score']) - float(rows[-1]['score']):.4f}")
    
    st.divider()
    
    # Top 10 detailed view
    st.subheader("🏆 Top 10 Candidates")
    for i, row in enumerate(rows[:10], 1):
        with st.expander(f"**Rank {i}** | {row['candidate_id']} (Score: {row['score']})"):
            st.markdown(f"**Reasoning:**\n\n{row['reasoning']}")
    
    st.divider()
    
    # Full rankings table
    st.subheader("📊 All 100 Rankings")
    
    df = pd.DataFrame([
        {
            "Rank": int(r["rank"]),
            "Candidate ID": r["candidate_id"],
            "Score": float(r["score"]),
            "Reasoning": r["reasoning"][:80] + "..." if len(r["reasoning"]) > 80 else r["reasoning"]
        }
        for r in rows
    ])
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.NumberColumn(format="%.4f"),
        }
    )
    
    st.divider()
    
    # Scoring explanation
    st.subheader("📐 How We Scored")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Technical Fit (75%)
        - **Retrieval Focus**: 25%
        - **Production AI**: 15%
        - **YOE Fit** (5-9 years): 12%
        - **Must-Have Skills**: 12%
        - **Vector DB Experience**: 10%
        - **Product Company Signal**: 8%
        - **AI Skill Count**: 5%
        """)
    
    with col2:
        st.markdown("""
        ### Behavioral Fit (13%)
        - Response Rate (10%)
        - Interview Completion (1.5%)
        - GitHub Activity (1.5%)
        - Notice Period & Availability
        
        ### Honeypot Penalty (-0 to -0.4)
        - Impossible skill durations
        - Career timeline mismatches
        - Exaggerated endorsements
        - Profile inconsistencies
        """)
    
    st.divider()
    
    st.info("""
    ✅ **What This Ranking Does Well**
    
    1. **Prioritizes Retrieval/Ranking** - Not generic AI keywords
    2. **Production Evidence** - All top candidates deployed systems at scale
    3. **Ideal Experience Range** - 5-9 years (matches JD specification)
    4. **Behavioral Signals** - High response rates, GitHub activity, fast to hire
    5. **Honeypot Detection** - Filters inflated profiles with impossible claims
    """)
    
except FileNotFoundError:
    st.error("❌ team_redrob_submission.csv not found. Run the ranker first!")
