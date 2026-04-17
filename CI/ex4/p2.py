import math

def safe_log2(x: float) -> float:
    """Calculates log2, returning 0.0 for non-positive inputs to avoid errors."""
    return math.log2(x) if x > 0 else 0.0

def entropy(rows, target):
    """Calculates the entropy of a given set of rows based on the target column."""
    label_counts = {}
    for row in rows:
        y = row[target]
        label_counts[y] = label_counts.get(y, 0) + 1
    
    total = len(rows)
    H = 0.0
    for c in label_counts.values():
        p = c / total
        H -= p * safe_log2(p)
    return H, label_counts

def split_by_value(rows, attr):
    """Groups rows by the values of a specific attribute."""
    groups = {}
    for row in rows:
        v = row[attr]
        groups.setdefault(v, []).append(row)
    return groups

def print_table(attr, groups, target, labels):
    """Prints a formatted table showing the distribution of target classes."""
    header = f"{attr:<15} | " + " | ".join(f"{str(L):^7}" for L in labels) + " | Total"
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)
    for val, subset in groups.items():
        counts = {}
        for row in subset:
            y = row[target]
            counts[y] = counts.get(y, 0) + 1
        
        row_str = f"{str(val):<15} | "
        for L in labels:
            row_str += f"{counts.get(L, 0):^7} | "
        row_str += f"{len(subset):^5}"
        print(row_str)
    print(separator)

def step_by_step_report(rows, attributes, target):
    """Generates a detailed report with tables and Information Gain math."""
    n = len(rows)
    H_S, label_counts = entropy(rows, target)
    labels_sorted = sorted(label_counts.keys())

    print(f"\nTotal examples: {n}")
    print(f"Base Entropy H(S): {H_S:.4f}")
    print("-" * 35)

    ig_results = []
    for attr in attributes:
        print(f"\nANALYSIS FOR ATTRIBUTE: {attr}")
        groups = split_by_value(rows, attr)
        
        # Display the requested table
        print_table(attr, groups, target, labels_sorted)

        H_after = 0.0
        weighted_terms = []
        for val, subset in groups.items():
            n_v = len(subset)
            H_v, _ = entropy(subset, target)
            H_after += (n_v / n) * H_v
            weighted_terms.append(f"({n_v}/{n})*{H_v:.4f}")

        IG = H_S - H_after
        print(f"Weighted Entropy H(S|{attr}): {' + '.join(weighted_terms)} = {H_after:.4f}")
        print(f"Information Gain IG({attr}): {IG:.4f}")
        ig_results.append((attr, IG))

    print("\n" + "="*45)
    print("FINAL SUMMARY (OVERALL INFORMATION GAIN)")
    print("="*45)
    for attr, IG in ig_results:
        print(f"{attr:15s} -> IG: {IG:.4f}")

    best_attr, best_IG = max(ig_results, key=lambda x: x[1])
    print(f"\nBest Attribute (Root Node) = {best_attr} (IG = {best_IG:.4f})")
    print("="*45)

def load_dataset(filename):
    """Reads a CSV-style dataset from a file."""
    data = []
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    
    headers = [h.strip() for h in lines[0].split(",")]
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        data.append({headers[i]: values[i] for i in range(len(headers))})
    
    return data, headers[:-1], headers[-1]

if __name__ == "__main__":
    # To run, ensure you have your 'a.txt' file in the same directory
    filename = "a.txt" 
    try:
        data, attributes, target = load_dataset(filename)
        step_by_step_report(data, attributes, target)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Create the file with your dataset first.")

