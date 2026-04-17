import itertools

def get_target(inputs, gate_choice, is_bipolar):
    # Convert bipolar -1 to 0 for standard logic processing
    logic_in = [0 if x == -1 else x for x in inputs]

    if gate_choice == 1: # AND
        res = all(logic_in)
    elif gate_choice == 2: # OR
        res = any(logic_in)
    elif gate_choice == 3: # AND-NOT (x1 AND NOT x2)
        res = (logic_in[0] == 1) and (logic_in[1] == 0) if len(logic_in) >= 2 else 0
    else:
        res = 0

    return 1 if res else (-1 if is_bipolar else 0)

def activation(yin, theta, is_bipolar):
    if yin >= theta:
        return 1
    return -1 if is_bipolar else 0

def main():
    mode_choice = int(input("Input mode (1: Binary, 2: Bipolar): "))
    is_bipolar = (mode_choice == 2)

    num_inputs = int(input("Number of inputs: "))
    gate_choice = int(input("Logic gate (1: AND, 2: OR, 3: AND-NOT): "))

    # --- NEW SECTION: CUSTOM USER INPUTS ---
    num_samples = int(input("How many input samples (rows) will you provide? "))
    dataset = []
    for i in range(num_samples):
        print(f"Entry {i+1}:")
        row = []
        for j in range(num_inputs):
            # Prompting for x1, x2... xn for each row
            val = float(input(f"  Enter value for x{j+1}: "))
            row.append(val)
        dataset.append(tuple(row))
    # ----------------------------------------

    theta = float(input("Threshold (theta): "))
    learning_rate = float(input("Learning rate: "))

    w = []
    for i in range(num_inputs):
        w.append(float(input(f"Initial weight w{i+1}: ")))
    b = float(input("Initial bias: "))

    print("\n--- Training Starts ---\n")

    epoch = 1
    max_epochs = 100
    converged = False
    col_w = 8 

    while not converged and epoch <= max_epochs:
        print(f"--- Epoch {epoch} ---")

        headers = [f"x{i+1}" for i in range(num_inputs)] + ["t"] + \
                  [f"w{i+1}" for i in range(num_inputs)] + ["b", "yin", "y"]

        header_str = "".join([f"{h:<{col_w}}" for h in headers])
        print(header_str)
        print("-" * len(header_str))

        error_count = 0

        for inputs in dataset:
            t = get_target(inputs, gate_choice, is_bipolar)
            yin = b + sum(w[i] * inputs[i] for i in range(num_inputs))
            y = activation(yin, theta, is_bipolar)

            row_vals = list(inputs) + [t] + w + [b, yin, y]
            row_str = "".join([f"{v:<{col_w}g}" for v in row_vals])
            print(row_str)

            if y != t:
                for i in range(num_inputs):
                    w[i] += learning_rate * t * inputs[i]
                b += learning_rate * t
                error_count += 1

        print("-" * len(header_str) + "\n")

        if error_count == 0:
            converged = True
        else:
            epoch += 1

    print("Training Complete!")
    final_weights = "  ".join([f"w{i+1}={w[i]:g}" for i in range(num_inputs)])
    print(f"Final:  {final_weights}  b={b:g}")

if __name__ == "__main__":
    main()

