import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Sample dataset (expand with real data)
data = {
    'engine_cranks': [0,1,1,0,1],
    'lights_dim': [1,0,0,1,0],
    'warning_light': [0,1,0,1,0],
    'oil_leak': [0,0,1,0,0],
    'smoke_exhaust': [0,0,0,0,1],
    'fault': ['Dead Battery', 'Alternator', 'Oil Leak', 'Electrical', 'Exhaust']
}

df = pd.DataFrame(data)
X = df.drop('fault', axis=1)
y = df['fault']

model = DecisionTreeClassifier()
model.fit(X, y)

joblib.dump(model, "trained_model.pkl")