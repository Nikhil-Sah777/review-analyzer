import re
from collections import Counter

import pandas as pd
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Review Analyzer", page_icon="📊", layout="wide")

FILE_NAME = "big_reviews.csv"
FEATURES = ["battery", "camera", "sound", "display", "screen", "delivery",
            "packaging", "price", "quality", "performance", "design",
            "service", "value"]

vader = SentimentIntensityAnalyzer()


def label_from_score(score):
    if score >= 0.05:
        return "Positive"
    if score <= -0.05:
        return "Negative"
    return "Neutral"


@st.cache_data
def load_and_analyze(max_rows):
    df = pd.read_csv(FILE_NAME, nrows=max_rows, encoding_errors="ignore")
    df.columns = [c.strip().lower() for c in df.columns]
    df["review"] = df["review"].fillna("").astype(str)
    df["summary"] = df["summary"].fillna("").astype(str)
    df["text"] = df["summary"] + ". " + df["review"]
    df["predicted"] = df["text"].apply(
        lambda t: label_from_score(vader.polarity_scores(t)["compound"])
    )
    df["actual"] = df["sentiment"].astype(str).str.strip().str.capitalize()
    return df


def count_features(df, only_negative=False):
    subset = df[df["predicted"] == "Negative"] if only_negative else df
    counter = Counter()
    for text in subset["text"]:
        words = set(re.findall(r"[a-z']+", text.lower()))
        for feature in FEATURES:
            if feature in words:
                counter[feature] += 1
    return pd.Series(counter, dtype="int64").sort_values(ascending=False)


st.title("📊 Review Analyzer")
st.write("Turns customer reviews into sentiment, top features and common complaints.")

max_rows = st.sidebar.slider("Number of reviews to analyze", 1000, 50000, 20000, step=1000)
df = load_and_analyze(max_rows)

accuracy = (df["predicted"] == df["actual"]).mean() * 100
positive_share = (df["predicted"] == "Positive").mean() * 100

c1, c2, c3 = st.columns(3)
c1.metric("Reviews analyzed", f"{len(df):,}")
c2.metric("Match with dataset labels", f"{accuracy:.1f}%")
c3.metric("Positive reviews", f"{positive_share:.1f}%")

left, right = st.columns(2)
with left:
    st.subheader("Sentiment")
    st.bar_chart(df["predicted"].value_counts())
with right:
    st.subheader("Most mentioned features")
    st.bar_chart(count_features(df).head(8))

st.subheader("Top complaints (features in negative reviews)")
st.bar_chart(count_features(df, only_negative=True).head(8))

st.subheader("Try it yourself")
user_text = st.text_area("Type a review:", "The sound quality is amazing but the battery is poor.")
if user_text:
    score = vader.polarity_scores(user_text)["compound"]
    st.write(f"**{label_from_score(score)}** (score: {score:.2f})")

st.subheader("Browse reviews")
choice = st.selectbox("Show reviews that are:", ["Positive", "Negative", "Neutral"])
st.dataframe(df[df["predicted"] == choice][["summary", "review", "actual"]].head(50))