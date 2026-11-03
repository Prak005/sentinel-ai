
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def clean_dataframe(df, label_column="Label"):
    """
    Clean the raw network traffic dataset.
    """

    df = df.copy()

    # Remove unnecessary spaces from column names
    df.columns = df.columns.astype(str).str.strip()

    # Handle infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Clean text columns
    for column in df.select_dtypes(include=["object", "string"]).columns:
        df[column] = df[column].astype(object).map(
            lambda value: value.strip()
            if isinstance(value, str) else value
        )
        df[column] = df[column].replace(r"^\s*$", np.nan, regex=True)

    # Remove rows without a target label
    if label_column in df.columns:
        df = df.dropna(subset=[label_column])

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove columns containing only missing values
    df = df.dropna(axis=1, how="all")

    return df


def prepare_data(
    df,
    label_column="Label",
    test_size=0.2,
    random_state=42
):
    """
    Prepare cleaned data for machine learning.
    """

    # Step 1: Clean the dataset
    df = clean_dataframe(df, label_column)

    if label_column not in df.columns:
        raise ValueError(f"Target column '{label_column}' not found.")

    # Step 2: Separate features and target
    X = df.drop(columns=[label_column])
    y = df[label_column].astype(str)

    if X.shape[1] == 0:
        raise ValueError("No input features found.")

    # Step 3: Identify numerical and categorical columns
    numerical_features = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    transformers = []

    # Numerical preprocessing
    if numerical_features:
        numerical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        transformers.append(
            ("numerical", numerical_pipeline, numerical_features)
        )

    # Categorical preprocessing
    if categorical_features:
        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ])

        transformers.append(
            ("categorical", categorical_pipeline, categorical_features)
        )

    preprocessor = ColumnTransformer(transformers)

    # Step 4: Split training and testing data
    class_counts = y.value_counts()

    stratify_target = (
        y if len(class_counts) > 1 and class_counts.min() >= 2
        else None
    )

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_target
    )

    # Step 5: Fit only on training data to prevent data leakage
    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)

    print("Preprocessing completed successfully!")
    print("Training samples:", X_train.shape[0])
    print("Testing samples:", X_test.shape[0])
    print("Number of features after preprocessing:", X_train.shape[1])

    return X_train, X_test, y_train, y_test, preprocessor
