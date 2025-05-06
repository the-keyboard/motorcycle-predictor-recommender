import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class ContentBasedRecommender:
    def __init__(self, data):
        self.data = data.copy()
        self.feature_columns = [
            'displacement_cc',
            'power_bhp',
            'weight_kg',
            'mileage',
            'top_speed',
            'star_rating'
        ]
        self.scaler = MinMaxScaler()
        self.scaled_data = self._scale_features()

    def _scale_features(self):
        feature_matrix = self.data[self.feature_columns].astype(float)
        scaled_features = self.scaler.fit_transform(feature_matrix)
        scaled_df = pd.DataFrame(scaled_features, columns=self.feature_columns)
        return scaled_df

    def predict(self, user_preferences):
        input_values = [user_preferences[feature] for feature in self.feature_columns]
        user_array = np.array(input_values, dtype=float).reshape(1, -1)
        scaled_user_vector = self.scaler.transform(user_array)
        distance_matrix = np.linalg.norm(self.scaled_data.values - scaled_user_vector, axis=1)
        normalized_scores = 100 - (distance_matrix / np.max(distance_matrix)) * 100
        scored_df = self.data.copy()
        scored_df['score'] = normalized_scores
        ranked_df = scored_df.sort_values(by='score', ascending=False)
        return ranked_df.head(10)

