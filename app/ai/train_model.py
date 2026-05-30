import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = {
    "text": [
        "help me",
        "someone is following me",
        "fire in building",
        "i met with an accident",
        "save me",
        "i am in danger",
        "need immediate help",
        "everything is fine",
        "i am safe",
        "just checking in",
        "having a good day",
        "all okay"
    ],
    "label": [
        1,1,1,1,1,1,1,
        0,0,0,0,0
    ]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["text"])
y = df["label"]

model = LogisticRegression()

model.fit(X, y)

joblib.dump(model, "emergency_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")