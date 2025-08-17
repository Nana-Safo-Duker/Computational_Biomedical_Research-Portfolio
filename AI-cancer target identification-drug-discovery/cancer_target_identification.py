"""Detailed analysis workflow for: AI-cancer target identification-drug-discovery"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 111
N_SAMPLES = 420
N_FEATURES = 18
CLASS_SHIFT = 0.85
ASSETS = Path("assets")
FEATURE_NAMES = ['expression_z', 'mutation_burden', 'druggability', 'network_centrality', 'pathway_enrichment', 'essentiality', 'tissue_specificity', 'literature_score']


def synthesize_dataset(seed: int = SEED) -> pd.DataFrame:
    """Create a topic-specific synthetic biomedical table."""
    rng = np.random.default_rng(seed)
    n = N_SAMPLES
    half = n // 2
    # Class A near baseline; class B shifted for separable signal
    x_a = rng.normal(loc=0.0, scale=1.0, size=(half, N_FEATURES))
    x_b = rng.normal(loc=CLASS_SHIFT, scale=1.05, size=(n - half, N_FEATURES))
    X = np.vstack([x_a, x_b])
    y = np.array([0] * half + [1] * (n - half))
    cols = [f"f{i}" for i in range(N_FEATURES)]
    for i, name in enumerate(FEATURE_NAMES):
        if i < N_FEATURES:
            cols[i] = name
    df = pd.DataFrame(X, columns=cols)
    df["label"] = y
    return df


def load_data(path: str | None = None) -> pd.DataFrame:
    """Load CSV if present; otherwise synthesize demonstration data."""
    if path and Path(path).exists():
        return pd.read_csv(path)
    return synthesize_dataset()


def preprocess(df: pd.DataFrame, target: str = "label"):
    """Prepare features and target with simple imputation."""
    df = df.copy()
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())
    X = df.drop(columns=[target])
    y = df[target]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series):
    """Train baseline models and return metrics + artifacts."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=SEED, stratify=y
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    logit = LogisticRegression(max_iter=2000, random_state=SEED)
    logit.fit(X_train_s, y_train)
    rf = RandomForestClassifier(n_estimators=120, random_state=SEED)
    rf.fit(X_train_s, y_train)

    proba = logit.predict_proba(X_test_s)[:, 1]
    pred = (proba >= 0.5).astype(int)
    rf_pred = rf.predict(X_test_s)

    return {
        "logit": logit,
        "rf": rf,
        "scaler": scaler,
        "X_test": X_test_s,
        "y_test": y_test,
        "proba": proba,
        "pred": pred,
        "auc": float(roc_auc_score(y_test, proba)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
        "rf_accuracy": float(accuracy_score(y_test, rf_pred)),
        "importances": rf.feature_importances_,
        "feature_names": list(X.columns),
        "report": classification_report(y_test, pred),
    }


def create_visualization(artifacts: dict) -> Path:
    """Render a topic-specific two-panel overview for the project README."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    y_test = artifacts["y_test"]
    proba = artifacts["proba"]

    kind = "target_score_distribution"
    if kind == "target_score_distribution":
        axes[0].hist(proba[y_test == 0], bins=18, alpha=0.7, label="Non-priority", color="#90A4AE")
        axes[0].hist(proba[y_test == 1], bins=18, alpha=0.7, label="Priority target", color="#C62828")
        axes[0].set_title("AI Cancer Target Identification\nPredicted Target Priority Scores")
        axes[0].set_xlabel("Model score"); axes[0].set_ylabel("Count"); axes[0].legend(fontsize=8)
    elif kind == "phenotype_umap_like":
        # 2D projection proxy from first two scaled features of test set
        xy = artifacts["X_test"][:, :2]
        axes[0].scatter(xy[y_test == 0, 0], xy[y_test == 0, 1], s=18, alpha=0.7, label="Phenotype A", c="#1565C0")
        axes[0].scatter(xy[y_test == 1, 0], xy[y_test == 1, 1], s=18, alpha=0.7, label="Phenotype B", c="#2E7D32")
        axes[0].set_title("AI Cancer Target Identification\nLatent Phenotype Embedding (proxy)")
        axes[0].set_xlabel("Dim 1"); axes[0].set_ylabel("Dim 2"); axes[0].legend(fontsize=8)
    else:
        names = np.array(artifacts["feature_names"][:8])
        imp = artifacts["importances"][: len(names)]
        order = np.argsort(imp)
        axes[0].barh(names[order], imp[order], color="#6A1B9A")
        axes[0].set_title("AI Cancer Target Identification\nFeature Importance (RF)")
        axes[0].set_xlabel("Importance")

    fpr, tpr, _ = roc_curve(y_test, proba)
    axes[1].plot(fpr, tpr, color="#EF6C00", lw=2, label=f"AUC = {artifacts['auc']:.3f}")
    axes[1].plot([0, 1], [0, 1], ls="--", color="gray")
    axes[1].set_title("Classifier ROC (simulated demo)")
    axes[1].set_xlabel("False Positive Rate"); axes[1].set_ylabel("True Positive Rate")
    axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)

    fig.tight_layout()
    out = ASSETS / "overview.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def run() -> None:
    df = load_data()
    X, y = preprocess(df)
    artifacts = train_model(X, y)
    chart = create_visualization(artifacts)
    print("Topic: AI-cancer target identification-drug-discovery")
    print(
        f"Metrics: AUC={artifacts['auc']:.4f}, Acc={artifacts['accuracy']:.4f}, "
        f"F1={artifacts['f1']:.4f}, RF Acc={artifacts['rf_accuracy']:.4f}"
    )
    print(f"n={len(df)}, features={X.shape[1]}, seed={SEED}")
    print(f"Visualization saved to: {chart}")


if __name__ == "__main__":
    run()
