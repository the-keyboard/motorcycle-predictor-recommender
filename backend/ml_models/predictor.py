import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

def preprocess_data(df):
    numerical_features = [
        'displacement_cc',
        'power_bhp',
        'weight_kg',
        'mileage',
        'top_speed',
        'star_rating'
    ]
    num_pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_features)
    ])
    return preprocessor, numerical_features

def build_model(df, preprocessor):
    features = df.drop(columns=['price'])
    target   = df['price']

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42
    )

    rf_regressor = RandomForestRegressor(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        random_state=42
    )

    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor',    rf_regressor)
    ])

    pipeline.fit(X_train, y_train)

    y_train_pred = pipeline.predict(X_train)
    y_test_pred  = pipeline.predict(X_test)

    train_r2 = r2_score(y_train, y_train_pred)
    test_r2  = r2_score(y_test,  y_test_pred)
    train_mse = mean_squared_error(y_train, y_train_pred)
    test_mse  = mean_squared_error(y_test,  y_test_pred)

    print(f"Train R²: {train_r2:.4f}  |  Test R²: {test_r2:.4f}")
    print(f"Train MSE: {train_mse:.2f}  |  Test MSE: {test_mse:.2f}")

    importances = pipeline.named_steps['regressor'].feature_importances_
    feature_names = preprocessor.transformers_[0][2]
    for name, imp in zip(feature_names, importances):
        print(f"{name}: {imp:.4f}")

    return pipeline