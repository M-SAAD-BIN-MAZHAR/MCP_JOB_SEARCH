import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="AI Job Recommender", layout="wide", page_icon="📄")

# Custom CSS for modern dashboard look
st.markdown("""
<style>
/* Page background */
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Card style */
.card {
    background: #1c1c1c;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
}

/* Job card style */
.job-card {
    background: #2a2a2a;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
    transition: transform 0.2s;
}
.job-card:hover {
    transform: scale(1.02);
}

/* Badges */
.badge {
    display:inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    background-color: #ff4b5c;
    color: white;
    font-size: 12px;
    margin-right: 5px;
}

/* Section headers */
h2 {
    background: linear-gradient(to right, #ff4b5c, #ffb347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Expanders */
.st-expander {
    background: #1e1e1e;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Job Recommender")
st.markdown("Upload your resume and get AI-powered **job recommendations**, **skill analysis**, and a **future roadmap**.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    # Tabs for better UX
    tabs = st.tabs(["📑 Summary", "🛠️ Skill Gaps", "🚀 Roadmap", "💼 Job Recommendations"])

    # ---------- Resume Summary ----------
    with tabs[0]:
        with st.spinner("Summarizing your resume..."):
            summary = ask_openai(f"Summarize this resume highlighting skills, education, and experience:\n\n{resume_text}")
        st.markdown(f"<div class='card'>{summary}</div>", unsafe_allow_html=True)

    # ---------- Skill Gaps ----------
    with tabs[1]:
        with st.spinner("Finding skill gaps..."):
            gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences for better job opportunities:\n\n{resume_text}")
        st.markdown(f"<div class='card'>{gaps}</div>", unsafe_allow_html=True)

    # ---------- Future Roadmap ----------
    with tabs[2]:
        with st.spinner("Creating future roadmap..."):
            roadmap = ask_openai(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skills to learn, certifications needed, industry exposure):\n\n{resume_text}")
        st.markdown(f"<div class='card'>{roadmap}</div>", unsafe_allow_html=True)

    # ---------- Job Recommendations ----------
    with tabs[3]:
        if st.button("🔎 Get Job Recommendations"):
            with st.spinner("Extracting job search keywords..."):
                keywords = ask_openai(
                    f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}"
                )
                search_keywords_clean = keywords.replace("\n", "").strip()
                st.success(f"**Job Search Keywords:** {search_keywords_clean}")

            with st.spinner("Fetching jobs from LinkedIn and Naukri..."):
                linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=50)
                naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=50)

            col1, col2 = st.columns(2)

            # LinkedIn Jobs
            with col1:
                st.subheader("💼 LinkedIn Jobs")
                if linkedin_jobs:
                    for job in linkedin_jobs:
                        with st.expander(f"{job.get('title')} at {job.get('companyName')}"):
                            st.markdown(f"""
                                <div class='job-card'>
                                    <strong>Location:</strong> <span class='badge'>{job.get('location')}</span><br>
                                    <strong>Apply Link:</strong> <a href='{job.get('link')}' target='_blank'>Click Here</a>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No LinkedIn jobs found.")

            # Naukri Jobs
            with col2:
                st.subheader("💼 Naukri Jobs (Pakistan)")
                if naukri_jobs:
                    for job in naukri_jobs:
                        with st.expander(f"{job.get('title')} at {job.get('companyName')}"):
                            st.markdown(f"""
                                <div class='job-card'>
                                    <strong>Location:</strong> <span class='badge'>{job.get('location')}</span><br>
                                    <strong>Apply Link:</strong> <a href='{job.get('url')}' target='_blank'>Click Here</a>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No Naukri jobs found.")
