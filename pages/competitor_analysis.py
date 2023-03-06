import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

competitors_data = pd.read_csv("data/competitors_sentiment.csv")
keyword_sentiment = pd.read_csv("data/keyword_sentiment.csv")
ner_sentiment = pd.read_csv("data/ner_sentiment.csv")

def set_data(start_date, end_date, filterby):

    data_all = competitors_data
    data_key = keyword_sentiment
    data_ner = ner_sentiment

    data_all['date'] = data_all['PublishDate'].apply(lambda x: x.split()[0])
    data_key['date'] = data_key['PublishDate'].apply(lambda x: x.split()[0])
    data_ner['date'] = data_ner['PublishDate'].apply(lambda x: x.split()[0])

    # if competitor == 'Kompas':
    #     data_key = data_key[data_key['source'] == 'kompas']
    #     data_ner = data_ner[data_ner['source'] == 'kompas']
    # elif competitor == 'Tribun':
    #     data_key = data_key[data_key['source'] == 'tribun']
    #     data_ner = data_ner[data_ner['source'] == 'kompas']

    # data_all = data_all[ (data_all['date'] >= start_date) & (data_all['date'] <= end_date) ]
    data_key = data_key[ (data_key['date'] >= start_date) & (data_key['date'] <= end_date) ]
    data_ner = data_ner[ (data_ner['date'] >= start_date) & (data_ner['date'] <= end_date) ]

    if filterby == "All":
        data_all = data_all
        data_key = data_key
        data_ner = data_ner
    elif filterby == "Positive":
        data_all = data_all[data_all["sentiment"] == 'positive']
        data_key = data_key[data_key["sentiment"] == 'positive']
        data_ner = data_ner[data_ner["sentiment"] == 'positive']
    elif filterby == "Negative":
        data_all = data_all[data_all["sentiment"] == 'negative']
        data_key = data_key[data_key["sentiment"] == 'negative']
        data_ner = data_ner[data_ner["sentiment"] == 'negative']
    elif filterby == "Neutral":
        data_all = data_all[data_all["sentiment"] == 'neutral']
        data_key = data_key[data_key["sentiment"] == 'neutral']
        data_ner = data_ner[data_ner["sentiment"] == 'neutral']

    data_all = data_all.dropna()
    data_all = data_all.reset_index()

    data_key = data_key.dropna()
    data_key = data_key.reset_index()

    data_ner = data_ner.dropna()
    data_ner = data_ner.reset_index()
    return data_all, data_key, data_ner


def set_sentiment_pie(data):
    df = data.groupby('sentiment').sentiment.count().reset_index(name='count').sort_values(['count'], ascending=False)
    fig = px.pie(df, values='count', names='sentiment')
    return fig

def set_wordcloud(data):
    list_stopwords = set(stopwords.words('indonesian'))
    text = " ".join(keyword for keyword in data.entity)
    wordcloud = WordCloud(stopwords=list_stopwords).generate(text)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordcloud)
    plt.axis("off")
    return fig

def set_entity_bar(data):
    df = data.groupby('entity').entity.count().reset_index(name='count').sort_values(['count'], ascending=False)
    fig = px.bar(df, x='count', y='entity', orientation='h')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    # fig = plt.figure(figsize=(10, 5))
    # plt.barh(df.entity, df.count)
    # plt.show()
    return fig

def set_entity_sentiment_bar(data):
    df = data.groupby(['entity', 'sentiment']).entity.count().reset_index(name='count').sort_values(['count'], ascending=False)
    fig = px.bar(df, x='count', y='entity', orientation='h')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def set_feed(data_all, data_key, data_ner):
    col1, col2 = st.columns(2)

    col1.markdown('## Kompas')
    col2.markdown('## Tribun')

    col1.markdown('#### Sentiment Proportion')
    col2.markdown('#### Sentiment Proportion')
    fig_wc_kompas = set_sentiment_pie(data_all[data_all['source'] == 'kompas'])
    fig_wc_tribun = set_sentiment_pie(data_all[data_all['source'] == 'tribun'])
    col1.write(fig_wc_kompas)
    col2.write(fig_wc_tribun)


    col1.markdown('#### Word Cloud')
    col2.markdown('#### Word Cloud')
    fig_wc_kompas = set_wordcloud(data_ner[data_ner['source'] == 'kompas'])
    fig_wc_tribun = set_wordcloud(data_ner[data_ner['source'] == 'tribun'])
    col1.pyplot(fig_wc_kompas)
    col2.pyplot(fig_wc_tribun)


    col1.markdown('#### Entity Distribution')
    col2.markdown('#### Entity Distribution')
    fig_wc_kompas = set_entity_bar(data_ner[data_ner['source'] == 'kompas'])
    fig_wc_tribun = set_entity_bar(data_ner[data_ner['source'] == 'tribun'])
    col1.write(fig_wc_kompas)
    col2.write(fig_wc_tribun)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("# Competitor Analysis")

    start_date = st.sidebar.date_input("Start date", value=date(2023, 2, 26)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 2, 27)).strftime("%Y-%m-%d")

    filterby = st.sidebar.selectbox(
        "Filter Content By Sentiment",
        ("All", "Positive", "Negative", "Neutral")
    )

    data_all, data_key, data_ner = set_data(start_date, end_date, filterby)

    set_feed(data_all, data_key, data_ner)