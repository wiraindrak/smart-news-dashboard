import streamlit as st
import pandas as pd
from datetime import date


competitors_data = pd.read_csv("data/competitors_sentiment.csv")


def set_data(competitor, start_date, end_date, filterby):
    data = competitors_data

    data['date'] = data['PublishDate'].apply(lambda x: x.split()[0])

    if competitor == 'Kompas':
        data = data[data['source'] == 'kompas']
    elif competitor == 'Tribun':
        data = data[data['source'] == 'tribun']

    data = data[ (data['date'] >= start_date) & (data['date'] <= end_date) ]

    if filterby == "All":
        data = data
    elif filterby == "Positive":
        data = data[data["sentiment"] == 'positive']
    elif filterby == "Negative":
        data = data[data["sentiment"] == 'negative']
    elif filterby == "Neutral":
        data = data[data["sentiment"] == 'neutral']


    data = data.sort_values(by='PublishDate', ascending=False)
    data = data.dropna()
    data = data.reset_index()
    return data

def set_feed(data):

    for index, row in data.iterrows():
        cont = st.container()
        cont.markdown('### %s' % row['Title'])

        c1, c2 = cont.columns(2)
        c1.markdown('%s ([link](%s))' % (row['source'], row['URL']))
        c2.markdown(row['PublishDate'])

        cont.markdown('> %s' % row['summary'])

        if row['sentiment'] == 'positive':
            cont.metric("Sentiment", "Positive ✅")
        elif row['sentiment'] == 'negative':
            cont.metric("Sentiment", "Negative ❌")
        elif row['sentiment'] == 'neutral':
            cont.metric("Sentiment", "Neutral ⏸️")
        cont.markdown("""---""")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("# Competitor Feed")
    competitor = st.sidebar.selectbox(
        "Competitors",
        ("All", "Kompas", "Tribun")
    )
    start_date = st.sidebar.date_input("Start date", value=date(2023, 2, 26)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 2, 27)).strftime("%Y-%m-%d")

    filterby = st.sidebar.selectbox(
        "Filter Content By Sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    data = set_data(competitor, start_date, end_date, filterby)

    set_feed(data)