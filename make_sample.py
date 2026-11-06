import pandas as pd

df = pd.read_csv("big_reviews.csv", encoding_errors="ignore")
sample = df.sample(n=30000, random_state=42)
sample.to_csv("sample_reviews.csv", index=False)
print("Done. Rows saved:", len(sample))