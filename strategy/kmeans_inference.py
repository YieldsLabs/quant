import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class KMeansInference:
    POOR_CLUSTER = 1

    def __init__(self, model_path: str, scaler_path: str):
        self.model = self.load_model(model_path)
        self.scaler = self.load_scaler(scaler_path)

    def load_model(self, model_path: str) -> KMeans:
        kmeans = joblib.load(model_path)

        return kmeans

    def load_scaler(self, scaler_path: str) -> StandardScaler:
        scaler = joblib.load(scaler_path)

        return scaler

    def infer(self, strategy_features: list) -> int:
        strategy_features = np.array([strategy_features])

        normalized_features = self.scaler.transform(strategy_features)

        cluster = self.model.predict(normalized_features)

        return cluster[0]
