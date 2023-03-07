import streamlit as st
import pandas as pd
from datetime import date
from streamlit_tags import st_tags_sidebar


competitors_data = pd.read_csv("data/competitors_sentiment.csv")
ner_sentiment = pd.read_csv("data/ner_sentiment.csv")

datner_sentimenta_ner = ner_sentiment[ner_sentiment['entity'].str.contains(r'[A-Za-z]') == True]
ner_sentiment = ner_sentiment[ner_sentiment['entity'].str.contains('#') == False]
ner_sentiment = ner_sentiment[ner_sentiment['entity'].str.len() > 2]

list_entities = set(list(ner_sentiment['entity']))


def set_data(competitor, start_date, end_date, filterby, list_entities):
    data = competitors_data
    data_ner = ner_sentiment

    data['date'] = data['PublishDate'].apply(lambda x: x.split()[0])
    data['date'] = data['date'].apply(lambda x: x.split('T')[0])

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

    if list_entities:
        list_ids = set(list(data_ner[data_ner['entity'].isin(list_entities)]['Article_ID']))
        data = data[data['Article_ID'].isin(list_ids)]

    data = data.sort_values(by='PublishDate', ascending=False)
    data = data.dropna()
    data = data.reset_index()

    return data, list_entities

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

    entities = st_tags_sidebar(
                label='Filter Content By Entity',
                text='Press enter to add more',
                value=[],
                suggestions=list(list_entities),
                maxtags = 4,
                key='2')

    data, list_entities = set_data(competitor, start_date, end_date, filterby, entities)

    set_feed(data)