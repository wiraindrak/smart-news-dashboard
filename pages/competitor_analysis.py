import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns

competitors_data = pd.read_csv("data/competitors_sentiment.csv")
keyword_sentiment = pd.read_csv("data/keyword_sentiment.csv")
ner_sentiment = pd.read_csv("data/ner_sentiment.csv")

def set_data(start_date, end_date):

    data_all = competitors_data
    data_key = keyword_sentiment
    data_ner = ner_sentiment

    data_ner = data_ner[data_ner['entity'].str.contains(r'[A-Za-z]') == True]
    data_ner = data_ner[data_ner['entity'].str.contains('#') == False]
    data_ner = data_ner[data_ner['entity'].str.len() > 2]

    data_all['date'] = data_all['PublishDate'].apply(lambda x: x.split()[0])
    data_key['date'] = data_key['PublishDate'].apply(lambda x: x.split()[0])
    data_ner['date'] = data_ner['PublishDate'].apply(lambda x: x.split()[0])

    data_all['date'] = data_all['date'].apply(lambda x: x.split('T')[0])
    data_key['date'] = data_key['date'].apply(lambda x: x.split('T')[0])
    data_ner['date'] = data_ner['date'].apply(lambda x: x.split('T')[0])

    data_all = data_all[ (data_all['date'] >= start_date) & (data_all['date'] <= end_date) ]
    data_key = data_key[ (data_key['date'] >= start_date) & (data_key['date'] <= end_date) ]
    data_ner = data_ner[ (data_ner['date'] >= start_date) & (data_ner['date'] <= end_date) ]

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
    fig, ax = plt.subplots(figsize = (20, 20))
    ax.imshow(wordcloud)
    plt.axis("off")
    return fig

def set_entity_bar(data):
    df = data['entity'].value_counts().iloc[0:20]
    fig = plt.figure(figsize=(10, 10))
    sns.barplot(x=df.values, y=df.index, orient='h')
    plt.title('Top Entities')
    plt.ylabel('Entity', fontsize=12)
    plt.xlabel('Frequency', fontsize=12)
    return fig

def set_entity_positive_bar(data):
    df = data[data['sentiment'] == 'positive']['entity'].value_counts().iloc[0:20]
    fig = plt.figure(figsize=(10, 10))
    sns.barplot(x=df.values, y=df.index, orient='h')
    plt.title('Top Positive Entities')
    plt.ylabel('Entity', fontsize=12)
    plt.xlabel('Frequency', fontsize=12)
    return fig

def set_entity_negative_bar(data):
    df = data[data['sentiment'] == 'negative']['entity'].value_counts().iloc[0:20]
    fig = plt.figure(figsize=(10, 10))
    sns.barplot(x=df.values, y=df.index, orient='h')
    plt.title('Top Negative Entities')
    plt.ylabel('Entity', fontsize=12)
    plt.xlabel('Frequency', fontsize=12)
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


    col1.markdown('#### Top Entity Distribution')
    col2.markdown('#### Top Entity Distribution')
    fig_wc_kompas = set_entity_bar(data_ner[data_ner['source'] == 'kompas'])
    fig_wc_tribun = set_entity_bar(data_ner[data_ner['source'] == 'tribun'])
    col1.pyplot(fig_wc_kompas)
    col2.pyplot(fig_wc_tribun)

    col1.markdown('#### Top Positive Entity Distribution ✅')
    col2.markdown('#### Top Positive Entity Distribution ✅')
    fig_wc_kompas = set_entity_positive_bar(data_ner[data_ner['source'] == 'kompas'])
    fig_wc_tribun = set_entity_positive_bar(data_ner[data_ner['source'] == 'tribun'])
    col1.pyplot(fig_wc_kompas)
    col2.pyplot(fig_wc_tribun)

    col1.markdown('#### Top Negative Entity Distribution ❌')
    col2.markdown('#### Top Negative Entity Distribution ❌')
    fig_wc_kompas = set_entity_negative_bar(data_ner[data_ner['source'] == 'kompas'])
    fig_wc_tribun = set_entity_negative_bar(data_ner[data_ner['source'] == 'tribun'])
    col1.pyplot(fig_wc_kompas)
    col2.pyplot(fig_wc_tribun)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.markdown("# Competitor Analysis")

    start_date = st.sidebar.date_input("Start date", value=date(2023, 2, 26)).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End date", value=date(2023, 2, 27)).strftime("%Y-%m-%d")

    # filterby = st.sidebar.selectbox(
    #     "Filter Content By Sentiment",
    #     ("All", "Positive", "Negative", "Neutral")
    # )

    data_all, data_key, data_ner = set_data(start_date, end_date)

    set_feed(data_all, data_key, data_ner)