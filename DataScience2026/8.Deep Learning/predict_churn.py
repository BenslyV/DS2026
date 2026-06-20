from pathlib import Path
import pickle

import pandas as pd

try:
    from tensorflow.keras.models import load_model
except ModuleNotFoundError as exc:
    raise SystemExit(
        "TensorFlow is required to load model.h5. Run this script with the same "
        "Python environment/kernel where TensorFlow is installed."
    ) from exc


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.h5"
SCALER_PATH = BASE_DIR / "scaler.pkl"
GENDER_ENCODER_PATH = BASE_DIR / "label_encoder_gender.pkl"
GEO_ENCODER_PATH = BASE_DIR / "onehot_encoder_geo.pkl"


def load_artifacts():
    model = load_model(MODEL_PATH)

    with SCALER_PATH.open("rb") as file:
        scaler = pickle.load(file)

    with GENDER_ENCODER_PATH.open("rb") as file:
        label_encoder_gender = pickle.load(file)

    with GEO_ENCODER_PATH.open("rb") as file:
        onehot_encoder_geo = pickle.load(file)

    return model, scaler, label_encoder_gender, onehot_encoder_geo


def prepare_customer_data(customer_data, scaler, label_encoder_gender, onehot_encoder_geo):
    customer_df = pd.DataFrame([customer_data])

    customer_df["Gender"] = label_encoder_gender.transform(customer_df["Gender"])

    geo_encoded = onehot_encoder_geo.transform(customer_df[["Geography"]]).toarray()
    geo_encoded_df = pd.DataFrame(
        geo_encoded,
        columns=onehot_encoder_geo.get_feature_names_out(["Geography"]),
        index=customer_df.index,
    )

    customer_df = pd.concat(
        [customer_df.drop("Geography", axis=1), geo_encoded_df],
        axis=1,
    )

    return scaler.transform(customer_df)


def main():
    sample_customer = {
        "CreditScore": 600,
        "Geography": "France",
        "Gender": "Male",
        "Age": 40,
        "Tenure": 3,
        "Balance": 60000,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000,
    }

    model, scaler, label_encoder_gender, onehot_encoder_geo = load_artifacts()
    customer_scaled = prepare_customer_data(
        sample_customer,
        scaler,
        label_encoder_gender,
        onehot_encoder_geo,
    )

    churn_probability = model.predict(customer_scaled)[0][0]
    prediction = "Customer is likely to churn" if churn_probability >= 0.5 else "Customer is not likely to churn"

    print(f"Churn probability: {churn_probability:.4f}")
    print(prediction)


if __name__ == "__main__":
    main()
