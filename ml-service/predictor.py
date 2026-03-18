import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle, os

MODEL_PATH = "xgboost_model.pkl"

def generate_training_data():
    """
    Creates a more sophisticated fake dataset using non-linear logic.
    Reflects the interaction between experience and job fit.
    """
    np.random.seed(42)
    n = 5000   # Triple the dataset size for better learning

    similarity_scores  = np.random.uniform(10, 100, n)
    years_experience   = np.random.randint(0, 20, n)
    education_levels   = np.random.randint(0, 5, n)
    skill_counts       = np.random.randint(1, 15, n)
    
    # 🌟 NEW: Complexity Logic
    # 1. Experience * Match interaction (Experience is only valuable if it matches the job)
    exp_match_interaction = (years_experience / 20.0) * (similarity_scores / 100.0)
    
    # 2. Minimum Threshold: If similarity is < 25%, likelihood of being hired drops drastically
    base_match = np.where(similarity_scores < 25, -20, similarity_scores * 0.3)
    
    # 3. Diminishing returns on skill counts (having 50 skills isn't 5x better than 10)
    skill_strength = np.log1p(skill_counts) * 10
    
    # Final 'Secret' Score Formula
    scores = (
        base_match + 
        (exp_match_interaction * 40) + 
        (education_levels * 5) + 
        skill_strength +
        np.random.normal(0, 10, n) # Noise
    )
    
    hired = (scores > 55).astype(int)

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
