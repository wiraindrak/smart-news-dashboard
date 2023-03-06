import streamlit as st
from st_pages import Page, show_pages
import nltk

nltk.download('stopwords')

show_pages(
    [
        Page("app.py", "Home Page", "🏠"),
        Page("pages/trending_content_feed.py", "Trending Content Feed", "🔭"),
        Page("pages/competitor_feed.py", "Competitor Feed", "👁️"),
        Page("pages/competitor_analysis.py", "Competitor Analysis", "⚖️")
    ]
)


# Main Description
st.markdown("## 👋 Welcome to Smart Media Dashboard, your best tool to Analyze Your News Competitors!")
st.markdown("Developed by Product Data Team")
st.markdown("The app is still under development. Please reach us if you have any comments or suggestions.")

# Description of the features.
st.markdown(
    """
    ### Select on the left panel what you want to explore:
    - With 🔭 Trending Content Feed, you will see a timeline aggregator that displays trending content based on our scraper.
    - With 👁️ Competitor Analysis,you will see a timeline aggregator that displays competitor content based on our scraper.
    - With ⚖️ Competitor Analysis, you will see the competitor analysis results and you can see each its sentity and sentiment.
    """
)