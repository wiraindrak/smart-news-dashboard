import streamlit as st
import pandas as pd
from datetime import date


trending_news_data = pd.read_csv("data/trending_content_news.csv")
trending_ls_data = pd.read_csv("data/trending_content_lifestyle.csv")


def set_data(category, start_date, end_date, sortby, filterby):
    if category == 'News':
        data = trending_news_data
    elif category == 'Lifestyle':
        data = trending_ls_data

    data = data[ (data['Published Date'] >= start_date) & (data['Published Date'] <= end_date) ]

    if sortby == "Most Trending":
        data['trending_score'] = data['Likes'] + data['Comment'] + data['Total Shares']
        data = data.sort_values(by='trending_score', ascending=False)
    elif sortby == "Most Likes":
        data = data.sort_values(by='Likes', ascending=False)
    elif sortby == "Most Comments":
        data = data.sort_values(by='Comment', ascending=False)
    elif sortby == "Most Shares":
        data = data.sort_values(by='Total Shares', ascending=False)


    if filterby == "All":
        data = data
    elif filterby == "Positive":
        data = data[data["Sentiment"] == 'Positif']
    elif filterby == "Negative":
        data = data[data["Sentiment"] == 'Negatif']
    elif filterby == "Neutral":
        data = data[data["Sentiment"] == 'Neutral']

    data = data.dropna()
    data = data.reset_index()
    return data

def set_feed(data):

    for index, row in data.iterrows():
        cont = st.container()
        cont.markdown('### %s' % row['Judul'])
        cont.markdown('> %s' % row['Full Article'])

        col1, col2, col3, col4 = cont.columns(4)

        if row['Sentiment'] == 'Positif':
            col1.metric("Sentiment", "Positive ✅")
        elif row['Sentiment'] == 'Negatif':
            col1.metric("Sentiment", "Negative ❌")
        elif row['Sentiment'] == 'Neutral':
            col1.metric("Sentiment", "Neutral ⏸️")
        col2.metric("Likes", "%s 👍🏻" % int(row['Likes']))
        col3.metric("Comments", "%s 💬" % int(row['Comment']))
        col4.metric("Shares", "%s 🚀" % int(row['Total Shares']))
        cont.markdown("""---""")



if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("# Trending Content Feed")
    category = st.sidebar.selectbox(
        "Content Category",
        ("News", "Lifestyle")
    )
    start_date = st.sidebar.date_input("Start date", value=date(2023, 2, 26)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 2, 27)).strftime("%Y-%m-%d")
    sortby = st.sidebar.selectbox(
        "Sort Content By",
        ("Most Trending", "Most Likes", "Most Comments", "Most Shares")
    )

    filterby = st.sidebar.selectbox(
        "Filter Content By Sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    data = set_data(category, start_date, end_date, sortby, filterby)

    set_feed(data)