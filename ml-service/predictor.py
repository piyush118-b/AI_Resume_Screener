import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle, os

MODEL_PATH = "xgboost_model.pkl"

def generate_training_data():
    """
    Creates a realistic fake dataset.
    In a real product, this would be your REAL historical hiring data!
    Each row = one candidate. Columns = features. Label = did they get hired? (1=Yes, 0=No)
    """
    np.random.seed(42)
    n = 800   # 800 fake candidates

    similarity_scores  = np.random.uniform(20, 99, n)
    years_experience   = np.random.randint(0, 15, n)
    # Education: 0=None, 1=Diploma, 2=Bachelor, 3=Master, 4=PhD
    education_levels   = np.random.randint(0, 5, n)
    skill_counts       = np.random.randint(1, 12, n)

    # 🌟 The Label: candidates with high similarity + experience tend to get hired!
    # We add some random noise to make it feel realistic (hiring is never 100% logic!)
    scores = (
        similarity_scores * 0.45 +
        years_experience  * 2.0  +
        education_levels  * 4.0  +
        skill_counts      * 1.5  +
        np.random.normal(0, 8, n)
    )
    hired = (scores > 70).astype(int)  # threshold deciding hired/not hired

    return pd.DataFrame({
        "similarity_score": similarity_scores,
        "years_experience": years_experience,
        "education_level":  education_levels,
        "skill_count":      skill_counts,
        "hired":            hired
    })

def train_and_save_model():
    """Trains the XGBoost model and saves it to disk as a .pkl file."""
    print("Generating training data...")
    df = generate_training_data()

    X = df[["similarity_score", "years_experience", "education_level", "skill_count"]]
    y = df["hired"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc   = accuracy_score(y_test, preds)
    print(f"Model Accuracy on test set: {acc*100:.1f}%")

    # Save model to disk so FastAPI can load it without re-training every time
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")
    return model

def load_model():
    """Load from disk if exists, otherwise train a fresh one."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return train_and_save_model()

def predict_placement(similarity_score: float, years_experience: int,
                      education_level: int, skill_count: int) -> float:
    """
    Returns the probability (0-100%) that a candidate will pass the HR screening.
    """
    model = load_model()
    features = pd.DataFrame([{
        "similarity_score": similarity_score,
        "years_experience": years_experience,
        "education_level":  education_level,
        "skill_count":      skill_count
    }])
    # predict_proba returns [[prob_no, prob_yes]] — we want prob_yes
    prob = model.predict_proba(features)[0][1]
    return float(round(prob * 100, 2))

# 🌟 If you run this file directly (python predictor.py) it will train + save the model!
if __name__ == "__main__":
    train_and_save_model()
