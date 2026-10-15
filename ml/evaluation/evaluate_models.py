import numpy as np

def evaluate_emotion_model(y_true, y_pred):
    """
    Evaluates emotion classification performance.
    y_true: True labels (0-6)
    y_pred: Predicted labels (0-6)
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted')
    rec = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    cm = confusion_matrix(y_true, y_pred)
    
    print("--- Emotion Model Evaluation ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print("Confusion Matrix:\n", cm)
    return acc, prec, rec, f1, cm

def evaluate_age_model(y_true, y_pred):
    """
    Evaluates age estimation regression performance.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    
    print("\n--- Age Estimation Model Evaluation ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} years")
    # A smaller MAE represents better performance. 
    return mae

if __name__ == "__main__":
    print("Running Mock ML Evaluation Suite...")
    # Mock data for demonstration
    mock_true_emo = [0, 1, 2, 0, 1, 3, 2, 0]
    mock_pred_emo = [0, 1, 2, 1, 1, 3, 2, 0]
    evaluate_emotion_model(mock_true_emo, mock_pred_emo)
    
    mock_true_age = [25, 30, 18, 55, 42]
    mock_pred_age = [23, 31, 19, 50, 44]
    evaluate_age_model(mock_true_age, mock_pred_age)
