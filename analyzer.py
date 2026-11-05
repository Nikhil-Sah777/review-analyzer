import matplotlib.pyplot as plt

import csv
from collections import Counter

positive_words = ["great", "amazing", "love", "good", "excellent", "happy", "best", "fast"]
negative_words = ["terrible", "broken", "bad", "high", "worst", "slow", "heats", "not worth"]
feature_words = ["battery", "camera", "price", "screen", "delivery", "sound", "quality", "money"]


def analyze(review):
    text = review.lower()
    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"


def read_reviews(filename):
    reviews = []
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviews.append(row["review"])
    return reviews


reviews = read_reviews("reviews.csv")

counts = Counter()
feature_mentions = Counter()
complaints = Counter()

for review in reviews:
    result = analyze(review)
    counts[result] += 1
    text = review.lower()
    for feature in feature_words:
        if feature in text:
            feature_mentions[feature] += 1
            if result == "Negative":
                complaints[feature] += 1
    print(f"{result}: {review}")

print()
print("Sentiment summary:", dict(counts))
print("Most mentioned features:", feature_mentions.most_common(3))
print("Most common complaints:", complaints.most_common(3))


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