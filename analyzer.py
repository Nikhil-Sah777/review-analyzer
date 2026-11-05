# Simple Product Review Analyzer

reviews = [
    "Great battery life and amazing camera. Love it!",
    "Terrible delivery, the phone arrived broken.",
    "Good screen but the price is too high.",
    "Battery is bad and it heats up. Not worth the money.",
    "Excellent sound quality, very happy with this purchase.",
    "It is okay, nothing special.",
]

positive_words = ["great", "amazing", "love", "good", "excellent", "happy", "best", "fast"]
negative_words = ["terrible", "broken", "bad", "high", "worst", "slow", "heats", "not worth"]


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


counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

for review in reviews:
    result = analyze(review)
    counts[result] += 1
    print(f"{result}: {review}")

print()
print("Summary:", counts)