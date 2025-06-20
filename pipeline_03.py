# -*- coding: utf-8 -*-
"""pipeline_03.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1exFK4bUCdkufW_xRLZfmVq35IhmlhBqR
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score

# 1. Função de pré-processamento dos dados
def preprocess_data(df):
    X = df.drop(columns=['Carga_Traçao'])
    y = df['Carga_Traçao']

    numerical_features = [
        'Deph(m)', 'Nspt', 'qc(Mpa)', 'fs(Mpa)',
        'Depth_fs_product', 'Nspt_qc_ratio', 'log_Nspt',
        'Nspt_carga_product', 'log_Nspt_carga_product'
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), numerical_features)
        ],
        remainder='passthrough'
    )

    return X, y, preprocessor


# 2. Função de treinamento do modelo
def train_model(X, y, preprocessor):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline_rf = Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(random_state=42))
    ])

    pipeline_rf.fit(X_train, y_train)

    y_pred = pipeline_rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"MSE do Random Forest: {mse:.4f}")
    print(f"R² do Random Forest: {r2:.4f}")

    return pipeline_rf


# 3. Função para previsão de novo caso
def predict_new_case(pipeline_rf):
    new_data = pd.DataFrame({
        'Deph(m)': [15],
        'Nspt': [25],
        'qc(Mpa)': [12.5],
        'fs(Mpa)': [0.15],
        'Nspt_qc_ratio': [25 / (12.5 + 1e-8)],
        'Depth_fs_product': [15 * 0.15],
        'Nspt_carga_product': [0],
        'log_Nspt': [np.log1p(25)],
        'log_Nspt_carga_product': [0]
    })

    predicted_carga = pipeline_rf.predict(new_data)
    print(f"Capacidade de carga prevista (kN) pelo Random Forest: {predicted_carga[0]:.2f}")


# Execução principal
if __name__ == "__main__":
    df = pd.read_csv('df_preprocessed.csv')
    X, y, preprocessor = preprocess_data(df)
    model = train_model(X, y, preprocessor)
    predict_new_case(model)