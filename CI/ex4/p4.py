import math
def safe_log2(x):
    """Calculates log2, returning 0.0 for non-positive inputs."""
    return math.log2(x) if x > 0 else 0.0
def calculate_entropy_with_math(counts):
    """Calculates entropy and returns both the value and the string formula."""
    total = sum(counts)
    if total == 0: return 0.0, "0"
    formula_parts = []
    entropy_val = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            entropy_val -= p * safe_log2(p)
            formula_parts.append(f"({c}/{total})log2({c}/{total})")
    
    formula_str = " - ".join(formula_parts)
    if formula_str: formula_str = "-" + formula_str
    return entropy_val, formula_str
def generate_full_report(filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    headers = [h.strip() for h in lines[0].split(',')]
    attributes = headers[:-1]
    target = headers[-1]
    data = [dict(zip(headers, [v.strip() for v in line.split(',')])) for line in lines[1:]]
    
    labels = sorted(list(set(row[target] for row in data)))
    total_n = len(data)
    
    print("="*65)
    print(f"STEP 1: TOTAL ENTROPY H(S)")
    print("="*65)
    
    base_counts = [sum(1 for r in data if r[target] == L) for L in labels]
    h_s, h_s_formula = calculate_entropy_with_math(base_counts)
    
    print(f"Class Counts: {dict(zip(labels, base_counts))}")
    print(f"H(S) Formula: {h_s_formula}")
    print(f"H(S) Value:   {h_s:.4f}\n")

    ig_results = []

    print("="*65)
    print(f"STEP 2: ATTRIBUTE ANALYSIS & INFORMATION GAIN")
    print("="*65)

    for attr in attributes:
        print(f"\n[ATTRIBUTE: {attr}]")
        unique_vals = sorted(list(set(row[attr] for row in data)))
        
        # Table Layout
        header = f"{attr:<15} | " + " | ".join(f"{L:^7}" for L in labels) + " | Total | H(Sv)"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        
        weighted_terms = []
        h_after = 0.0
        
        for v in unique_vals:
            subset = [r for r in data if r[attr] == v]
            nv = len(subset)
            v_counts = [sum(1 for r in subset if r[target] == L) for L in labels]
            h_v, _ = calculate_entropy_with_math(v_counts)
            
            counts_str = " | ".join(f"{c:^7}" for c in v_counts)
            print(f"{v:<15} | {counts_str} | {nv:^5} | {h_v:.4f}")
            
            h_after += (nv / total_n) * h_v
            weighted_terms.append(f"({nv}/{total_n})*{h_v:.4f}")
            
        print("-" * len(header))
        print(f"H(S|{attr}) = {' + '.join(weighted_terms)} = {h_after:.4f}")
        
        gain = h_s - h_after
        print(f"Gain({attr}) = {h_s:.4f} - {h_after:.4f} = {gain:.4f}")
        ig_results.append((attr, gain))

    print("\n" + "="*65)
    print(f"STEP 3: FINAL RANKING")
    print("="*65)
    
    # Sort results by Gain value descending
    ig_results.sort(key=lambda x: x[1], reverse=True)
    
    for attr, ig in ig_results:
        print(f"IG({attr:15s}) = {ig:.4f}")
    
    # Extract the top attribute and its value
    best_attr, best_val = ig_results[0]
    print(f"\nBEST ATTRIBUTE FOR ROOT NODE: {best_attr} (Gain = {best_val:.4f})")
    print("="*65)

if __name__ == "__main__":
    generate_full_report('a.txt')

