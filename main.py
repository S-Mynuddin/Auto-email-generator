import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(page_title="Smart Outreach Assistant", page_icon="💼", layout="wide")

    st.markdown(
        """
        # 💼 Smart Outreach Assistant  
        _Generate AI-crafted cold emails tailored to job descriptions._
        
        Paste a job URL, and this assistant will:
        - Analyze the job posting
        - Match your portfolio
        - Generate a professional cold email automatically
        """
    )

    with st.sidebar:
        st.header("🔗 Job Post Link")
        url_input = st.text_input(
            "Paste the job URL below:",
            value="https://careers.nike.com/retail-associate-ft-ontario-mills/job/R-63877",
            help="Enter a valid job post URL to extract information."
        )
        submit_button = st.button("Generate Email")

    if submit_button:
        with st.spinner("🔍 Analyzing job post and generating email..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No job details found at the provided URL.")
                    return

                for job in jobs:
                    st.subheader(f"🎯 Target Role: {job.get('title', 'N/A')}")
                    st.markdown(f"**Location**: {job.get('location', 'Not specified')}")
                    st.markdown(f"**Required Skills**: {', '.join(job.get('skills', []))}")

                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    st.markdown("### ✉️ Suggested Cold Email")
                    st.code(email, language='markdown')

            except Exception as e:
                st.error(f"❌ An error occurred: Change API KEY")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
