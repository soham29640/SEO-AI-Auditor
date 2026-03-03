from sklearn.feature_extraction.text import TfidfVectorizer

def build_tfidf(text_series):

    tfidf = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1,3)
    )

    transformed_output = tfidf.fit_transform(text_series)

    return transformed_output