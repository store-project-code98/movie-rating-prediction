# movie-rating-prediction
Program that uses machine learning to predict what rating a movie would get based on a selected movie review 
Uses Python with Selenium / Chrome WebDriver in Brave to scrape IMDB reviews to collect data, then uses VaderSentiment and Sklearn to train based upon that data

3/28/2025 - Text data is processed with a TfidfVectorizer with 5000 features using a RandomForestRegressor model. Hyperparameter tuning uses RandomizedSearchCV along with MaxAbsScaler to sample and scale the data respectively. Values of 100 to 900 considered for decision trees with max depth ranging from None-30. Min_samples_split options are 2, 5, 10, min samples leaf are 1 and 2, and max_features consideration is sqrt and log.
