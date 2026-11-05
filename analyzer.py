import csv
import re
from collections import Counter
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

FILE_NAME = "big_reviews.csv"
MAX_ROWS = 20000

feature_words = ["battery", "camera", "sound", "display", "screen", "delivery",
                 "packaging", "price", "quality", "performance", "design",
                 "service", "value"]

vader = SentimentIntensityAnalyzer()


def get_words(text):
    return set(re.findall(r"[a-z']+", text.lower()))


def analyze(text):
    score = vader.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def read_reviews(filename, max_rows):
    data = []
    with open(filename, newline="", encoding="utf-8", errors="ignore") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {key.strip().lower(): value for key, value in row.items()}
            review = row.get("review") or ""
            summary = row.get("summary") or ""
            label = (row.get("sentiment") or "").strip().capitalize()
            data.append((summary + ". " + review, label))
            if len(data) >= max_rows:
                break
    return data


data = read_reviews(FILE_NAME, MAX_ROWS)

counts = Counter()
real_counts = Counter()
feature_mentions = Counter()
complaints = Counter()
correct = 0

for text, real_label in data:
    result = analyze(text)
    counts[result] += 1
    real_counts[real_label] += 1
    if result == real_label:
        correct += 1
    words = get_words(text)
    for feature in feature_words:
        if feature in words:
            feature_mentions[feature] += 1
            if result == "Negative":
                complaints[feature] += 1

print("Reviews analyzed:", len(data))
print("Our sentiment summary:", dict(counts))
print("Dataset's real labels:", dict(real_counts))
print("Most mentioned features:", feature_mentions.most_common(5))
print("Most common complaints:", complaints.most_common(5))
print(f"Matches the dataset's labels: {correct / len(data) * 100:.1f}%")

# ---- Dashboard ----
labels = ["Positive", "Negative", "Neutral"]
values = [counts[label] for label in labels]

top = feature_mentions.most_common(5)
names = [item[0] for item in top]
numbers = [item[1] for item in top]

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(labels, values, color=["green", "red", "gray"])
axes[0].set_title("Review Sentiment")
axes[0].set_ylabel("Number of reviews")

axes[1].bar(names, numbers, color="steelblue")
axes[1].set_title("Most Mentioned Features")
axes[1].set_ylabel("Mentions")

plt.tight_layout()
plt.savefig("dashboard.png")
plt.show()