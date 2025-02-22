import pandas as pd
import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
# by Billy Adamson

# training data
csv_files = ["training_data/@DOGE.csv", "training_data/SDOGE.csv", "training_data/SOL.csv", "training_data/TRUMP.csv", "training_data/USDT.csv"]

all_data = pd.DataFrame()

# load and preprocess each CSV file
for file in csv_files:
    df = pd.read_csv(file, header=None, parse_dates=[0])
    df.columns = ['Date', 'SearchQueries', 'Ignore', 'Price']
    df = df.drop(columns=['Ignore'])  # Drop the 'Ignore' column
    df = df.sort_values(by='Date').reset_index(drop=True)
    df['SearchQueries'] = df['SearchQueries'].replace(0, 1)

    # create features: percentage change, rolling averages, and volatility
    df['PriceChange'] = df['Price'].pct_change().fillna(1e-6)
    df['SearchQueryChange'] = df['SearchQueries'].pct_change().fillna(1e-6)
    df['RollingMinPrice'] = df['Price'].rolling(window=3).min().shift(-3)
    df['Volatility'] = df['Price'].rolling(window=5).std().fillna(0)

    # create labels: 1 if price drops more than 10% in the next 3 days, otherwise 0
    df['CrashLabel'] = (df['RollingMinPrice'] < df['Price'] * 0.9).astype(int)
    
    df.replace([np.inf, -np.inf], 1e-6, inplace=True)
    all_data = pd.concat([all_data, df], ignore_index=True)

# prepare features and labels
X = all_data[['PriceChange', 'SearchQueryChange', 'Volatility']].values
y = all_data['CrashLabel'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train
clf = RandomForestClassifier(random_state=42)
scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
print(f"Cross-Validation Accuracy: {scores.mean():.2f}")

clf.fit(X_train, y_train)

# predict and evaluate
y_pred = clf.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

def predict_crash(new_file):
    new_df = pd.read_csv(new_file, header=None, parse_dates=[0])
    new_df.columns = ['Date', 'SearchQueries', 'Ignore', 'Price']
    new_df = new_df.drop(columns=['Ignore'])

    # replace 0 in SearchQueries with 1 and calculate percentage change
    new_df['SearchQueries'] = new_df['SearchQueries'].replace(0, 1)
    new_df['PriceChange'] = new_df['Price'].pct_change().fillna(1e-6)
    new_df['SearchQueryChange'] = new_df['SearchQueries'].pct_change().fillna(1e-6)
    new_df['Volatility'] = new_df['Price'].rolling(window=5).std().fillna(0)

    # prob for each row
    X_new = new_df[['PriceChange', 'SearchQueryChange', 'Volatility']].values
    probabilities = clf.predict_proba(X_new)[:, 1]

    # Return the probability for the latest row (present time)
    crash_probability = int(math.ceil(probabilities[-1] * 100))
    
    return crash_probability

# # Example usage:
# result = predict_crash('training_data/USDT.csv')
# print(f"Crash Probability: {result:.2f}")
