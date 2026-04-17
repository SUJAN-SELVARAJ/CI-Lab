import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
table = pd.DataFrame(data.data, columns=data.feature_names)
table['target'] = data.target

X = table.iloc[:, 0:-1].values
y = table.iloc[:, -1].values

n_trees = int(input("Enter no. of trees: "))
splits = {'70-30': 0.3, '60-40': 0.4, '75-25': 0.25}
result = []
conf_mat = {}

for split_name, test_size in splits.items():
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    model = RandomForestClassifier(n_estimators=n_trees, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acr = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    result.append([split_name, acr, prec, rec, f1])

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    conf_mat[split_name] = (tn, fp, fn, tp)

print("\nResults for splits:")
print(f"{'Split':<10} {'Accuracy':<10} {'Precision':<10} {'Recall':<10} {'F1_Score':<10}")
for row in result:
    print(f"{row[0]:<10} {row[1]:.4f}    {row[2]:.4f}    {row[3]:.4f}    {row[4]:.4f}")

print("\nConfusion Matrix:")

for split_name, (tn, fp, fn, tp) in conf_mat.items():
    print(f"{split_name} Split:\n")
    print("\t Predicted")
    print(f"Actual | {tn}   {fp} ")
    print(f"         {fn}   {tp} ")

