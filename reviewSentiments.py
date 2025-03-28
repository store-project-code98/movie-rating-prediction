from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import MaxAbsScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(review):
    sentiment = analyzer.polarity_scores(review)
    return sentiment['compound']

df = pd.read_csv('imdb_reviews.csv')

df['vader_sentiment'] = df['Review'].apply(vader_sentiment)
X = df[['Review', 'vader_sentiment']]
y = df['Rating']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 3))
X_train_tfidf = vectorizer.fit_transform(X_train['Review'])
X_test_tfidf = vectorizer.transform(X_test['Review'])

scaler = MaxAbsScaler()
X_train_tfidf = scaler.fit_transform(X_train_tfidf)
X_test_tfidf = scaler.transform(X_test_tfidf)

model = RandomForestRegressor(random_state=42)

param_dist = {
    'n_estimators': np.arange(100, 1000, 100), 
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2']
}

random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=50, cv=5, n_jobs=-1, verbose=1)
random_search.fit(X_train_tfidf, y_train)

best_model = random_search.best_estimator_

y_pred = best_model.predict(X_test_tfidf)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')

def predict_rating(model, vectorizer, review):
    review_tfidf = vectorizer.transform([review])
    review_tfidf = scaler.transform(review_tfidf)
    prediction = model.predict(review_tfidf)
    return prediction[0]

counter = 1
while True:
    review = input("Enter a review (or type 'Exit' to stop): ")
    
    if review.lower() == 'exit':
        print("Exiting the review input process.")
        break
    
    predicted_rating = predict_rating(best_model, vectorizer, review)
    print(f"Review {counter}: Predicted Rating: {predicted_rating:.2f}")
    counter += 1
