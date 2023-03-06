from transformers import pipeline
from newspaper import Article
import pandas as pd
import re
import yake
from tqdm import tqdm


pretrained_sentiment = "w11wo/indonesian-roberta-base-sentiment-classifier"
pretrained_ner = "cahya/bert-base-indonesian-NER"
pretrained_summary = "panggi/t5-base-indonesian-summarization-cased"

sentiment_pipeline = pipeline(
    task="sentiment-analysis",
    model=pretrained_sentiment,
    tokenizer=pretrained_sentiment,
    top_k=None
)

ner_pipeline = pipeline(
    task="ner",
    model=pretrained_ner,
    tokenizer=pretrained_ner,
    aggregation_strategy="simple"
)

summary_pipeline = pipeline(
    task="summarization",
    model=pretrained_summary,
    tokenizer=pretrained_summary
)

def sentiment_analysis(text):
    output = sentiment_pipeline(text)
    return {elm["label"]: elm["score"] for elm in output[0]}

def ner(text):
    output = ner_pipeline(text)
    for elm in output:
        elm['entity'] = elm['entity_group']
    return output

def summary(text):
    output = summary_pipeline(text, min_length=32, max_length=64)
    return output[0]['summary_text']

def inference(text):
    return sentiment_analysis(text), ner(text)

def sentiment_df(df):
    text_list = list(df["summary"].astype(str).values)
    result = [sentiment_analysis(text) for text in tqdm(text_list)]
    labels = []
    # scores = []
    for pred in result:
        idx = list(pred.values()).index(max(list(pred.values())))
        labels.append(list(pred.keys())[idx])
        # scores.append(round(list(pred.values())[idx], 3))
    df['sentiment'] = labels
    # df['Score'] = scores
    return df

def ner_df(df):
    text_list = list(df["summary"].astype(str).values)
    label_list = list(df["sentiment"].astype(str).values)
    result = [ner(text) for text in tqdm(text_list)]
    terms = []
    sentiments = []
    urls = []
    article_ids = []
    publish_dates = []
    sources = []
    ent = ['PER', 'NOR', 'ORG']
    for i, preds in enumerate(result):
        for pred in preds:
            if pred['entity_group'] in ent:
                terms.append(pred['word'])
                sentiments.append(label_list[i])
                urls.append(df['URL'][i])
                article_ids.append(df['Article_ID'][i])
                publish_dates.append(df['PublishDate'][i])
                sources.append(df['source'][i])

    df_ner = pd.DataFrame(columns=['URL', 'PublishDate', 'Article_ID', 'source', 'entity', 'sentiment'])
    df_ner['URL'] = urls
    df_ner['PublishDate'] = publish_dates
    df_ner['Article_ID'] = article_ids
    df_ner['source'] = sources
    df_ner['entity'] = terms
    df_ner['sentiment'] = sentiments
    return df_ner

def get_article_content(url, source, category):
    article = Article(url, language="id")
    article.download()
    article.parse()

    return {
        "url": str(url),
        "source": str(source),
        "category": str(category),
        "title": str(article.title),
        "text": str(re.sub(r'\n\s*\n', '\n\n', article.text)),
        "published_at": article.publish_date.strftime("%Y-%m-%d")
    }

def keyword_extraction(text):
    language = "id"
    max_ngram_size = 3
    windowSize = 1
    numOfKeywords = 5

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords

def keyword_df(df):
    text_list = list(df["summary"].astype(str).values)
    label_list = list(df["sentiment"].astype(str).values)
    result = [keyword_extraction(text) for text in tqdm(text_list)]
    terms = []
    sentiments = []
    urls = []
    article_ids = []
    publish_dates = []
    sources = []
    for i, preds in enumerate(result):
        for pred in preds:
            terms.append(pred[0])
            sentiments.append(label_list[i])
            urls.append(df['URL'][i])
            article_ids.append(df['Article_ID'][i])
            publish_dates.append(df['PublishDate'][i])
            sources.append(df['source'][i])

    df_ner = pd.DataFrame(columns=['URL', 'PublishDate', 'Article_ID', 'source', 'entity', 'sentiment'])
    df_ner['URL'] = urls
    df_ner['PublishDate'] = publish_dates
    df_ner['Article_ID'] = article_ids
    df_ner['source'] = sources
    df_ner['keyword'] = terms
    df_ner['sentiment'] = sentiments
    return df_ner

data_kompas = 'data/kompas.csv'
data_tribun = 'data/tribunnews.csv'


tqdm.pandas()

# pd_kompas = pd.read_csv(data_kompas)
# pd_tribun = pd.read_csv(data_tribun)

# pd_kompas['source'] = 'kompas'
# pd_tribun['source'] = 'tribun'

# pd_data = pd.concat([pd_kompas, pd_tribun])

# pd_data['summary'] = pd_data['Body_Text'].progress_apply(summary)

# pd_data.to_csv('data/competitors_summary.csv', index=False)


# pd_data['sentiment'] = pd_data['summary'].progress_apply(sentiment_analysis)

# pd_data = sentiment_df(pd_data)

# pd_data.to_csv('data/competitors_sentiment.csv', index=False)

pd_data = pd.read_csv('data/competitors_sentiment.csv')

pd_ner = ner_df(pd_data)

pd_ner.to_csv('data/ner_sentiment.csv', index=False)

pd_keyword = keyword_df(pd_data)

pd_keyword.to_csv('data/keyword_sentiment.csv', index=False)

# pd_data['ner'] = pd_data['summary'].progress_apply(ner)

# pd_data.to_csv('data/competitors_ner.csv', index=False)

# pd_data['keywords'] = pd_data['summary'].progress_apply(keyword_extraction)

# pd_data.to_csv('data/competitors_inferenced.csv', index=False)