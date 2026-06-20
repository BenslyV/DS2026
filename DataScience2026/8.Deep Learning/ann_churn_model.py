from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight

try:
    import tensorflow as tf
    from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
    from tensorflow.keras.layers import Dense, Dropout
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.optimizers import Adam
except ModuleNotFoundError as exc:
    raise SystemExit(
        "TensorFlow is required to train this ANN model. Install it in your "
        "deep-learning environment, then run this script again."
    ) from exc


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Churn_Modelling.csv"
MODEL_PATH = BASE_DIR / "ann_churn_model.keras"
SCALER_PATH = BASE_DIR / "scaler.pkl"
GENDER_ENCODER_PATH = BASE_DIR / "label_encoder_gender.pkl"
GEO_ENCODER_PATH = BASE_DIR / "onehot_encoder_geo.pkl"
LOG_DIR = BASE_DIR / "logs" / "fit"


def make_onehot_encoder() -> OneHotEncoder:
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def load_and_preprocess_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    data = pd.read_csv(DATA_PATH)

    data = data.drop(["RowNumber", "CustomerId", "Surname"], axis=1)

    label_encoder_gender = LabelEncoder()
    data["Gender"] = label_encoder_gender.fit_transform(data["Gender"])

    onehot_encoder_geo = make_onehot_encoder()
    geo_encoded = onehot_encoder_geo.fit_transform(data[["Geography"]])
    geo_encoded_df = pd.DataFrame(
        geo_encoded,
        columns=onehot_encoder_geo.get_feature_names_out(["Geography"]),
        index=data.index,
    )

    data = pd.concat([data.drop("Geography", axis=1), geo_encoded_df], axis=1)

    X = data.drop("Exited", axis=1)
    y = data["Exited"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train,
        y_train,
        test_size=0.2,
        random_state=42,
        stratify=y_train,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    with GENDER_ENCODER_PATH.open("wb") as file:
        pickle.dump(label_encoder_gender, file)

    with GEO_ENCODER_PATH.open("wb") as file:
        pickle.dump(onehot_encoder_geo, file)

    with SCALER_PATH.open("wb") as file:
        pickle.dump(scaler, file)

    return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test


def build_ann_model(input_dim: int) -> Sequential:
    model = Sequential(
        [
            Dense(64, activation="relu", input_shape=(input_dim,)),
            Dropout(0.2),
            Dense(32, activation="relu"),
            Dropout(0.2),
            Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    return model


def main() -> None:
    tf.random.set_seed(42)
    np.random.seed(42)

    X_train, X_val, X_test, y_train, y_val, y_test = load_and_preprocess_data()
    model = build_ann_model(X_train.shape[1])

    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.array([0, 1]),
        y=y_train,
    )
    class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        TensorBoard(log_dir=str(LOG_DIR), histogram_freq=1),
    ]

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=callbacks,
        class_weight=class_weight_dict,
        verbose=1,
    )

    y_probability = model.predict(X_test).ravel()
    y_pred = (y_probability >= 0.5).astype(int)

    print("\nTest accuracy:", round(accuracy_score(y_test, y_pred), 4))
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    model.save(MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Training epochs completed: {len(history.history['loss'])}")


if __name__ == "__main__":
    main()
