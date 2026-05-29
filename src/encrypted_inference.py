"""
encrypted_inference.py
Logistic Regression on CKKS Homomorphic Encrypted Data (TenSEAL / CKKS)

Dataset  : Diabetes Prediction (20 features, 2000 samples)
Result   : Plaintext Accuracy = 96.60%  |  Encrypted Accuracy = 96.60%
"""

import numpy as np
import tenseal as ts
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score


# ── CKKS Context ──────────────────────────────────────────────────────────────
def build_ckks_context() -> ts.Context:
    """
    CKKS parameters (from paper):
      poly_modulus_degree = 8192
      coeff_mod_bit_sizes = [60, 40, 40, 60]
      global_scale        = 2^40
    """
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    ctx.global_scale = 2 ** 40
    ctx.generate_galois_keys()
    return ctx


# ── Data Loading ──────────────────────────────────────────────────────────────
def load_diabetes(path: str):
    df  = pd.read_csv(path)
    # Create binary target from existing features (as in paper)
    y   = (df['Diabetes_Risk'] > df['Diabetes_Risk'].median()).astype(int).values
    X   = df.drop(columns=['Diabetes_Risk']).values.astype(np.float32)
    return X, y


# ── Plaintext Training ────────────────────────────────────────────────────────
def train_plaintext(X_train, y_train, X_test, y_test):
    scaler = StandardScaler()
    X_tr   = scaler.fit_transform(X_train)
    X_te   = scaler.transform(X_test)

    model  = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_tr, y_train)

    y_pred = model.predict(X_te)
    acc    = accuracy_score(y_test, y_pred)
    print(f'\nPlaintext Accuracy: {acc:.4f}')
    print(classification_report(y_test, y_pred))
    return model, scaler


# ── Encrypted Inference ───────────────────────────────────────────────────────
def encrypted_inference(model, scaler, X_test, y_test, ctx):
    """
    Perform logistic regression inference on CKKS-encrypted test samples.
    Enc(X) → homomorphic dot product with weights → decrypt → threshold.
    """
    w     = model.coef_[0].astype(np.float64)
    b     = float(model.intercept_[0])
    X_sc  = scaler.transform(X_test).astype(np.float64)

    correct = 0
    for i, (x, y_true) in enumerate(zip(X_sc, y_test)):
        # Encrypt sample
        enc_x  = ts.ckks_vector(ctx, x.tolist())

        # Homomorphic dot product: enc(w·x) + b
        enc_out = enc_x.dot(w.tolist())
        enc_out = enc_out + b

        # Decrypt and threshold
        dec_val = enc_out.decrypt()[0]
        y_pred  = 1 if dec_val >= 0.0 else 0

        if y_pred == y_true:
            correct += 1

        if (i + 1) % 100 == 0:
            print(f'  Processed {i+1}/{len(X_test)} | Running Acc: {correct/(i+1):.4f}')

    enc_acc = correct / len(y_test)
    print(f'\n✅ Encrypted Inference Accuracy: {enc_acc:.4f}')
    return enc_acc


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='data/diabetes.csv')
    args = parser.parse_args()

    X, y  = load_diabetes(args.dataset)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y)

    model, scaler = train_plaintext(X_tr, y_tr, X_te, y_te)

    ctx = build_ckks_context()
    print('\nRunning encrypted inference (first 100 samples)...')
    encrypted_inference(model, scaler, X_te[:100], y_te[:100], ctx)

    print('\nRunning encrypted inference (full test set)...')
    encrypted_inference(model, scaler, X_te, y_te, ctx)
