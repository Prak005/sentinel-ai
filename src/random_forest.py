
from pathlib import Path
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support
)


def train_random_forest(
    X_train,
    y_train,
    X_test,
    y_test,
    model_path="models/random_forest.pkl"
):
    """
    Train and evaluate the Random Forest classifier.
    """

    # Initialize the model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced_subsample",
        n_jobs=-1
    )

    # Train the model
    print("Training Random Forest...")
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate evaluation metrics
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    accuracy = accuracy_score(y_test, predictions)

    # Display results
    labels = sorted(set(y_train) | set(y_test))

    print("\nRandom Forest Evaluation")
    print("-------------------------------")

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            labels=labels,
            target_names=labels,
            zero_division=0
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions, labels=labels))

    # Save trained model
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(f"\nModel saved successfully: {model_path}")

    return model, predictions


