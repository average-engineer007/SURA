import re

def evaluate_and_print_v4_variables(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Check if the line contains a variable with v_4_
        if re.match(r'v_4_', line.strip()):
            # Split the line by the equals sign
            variable, expression = line.split('=')
            variable = variable.strip()
            expression = expression.strip()

            # Evaluate the expression
            try:
                result = eval(expression)
                print(f"{variable} = {result}")
            except Exception as e:
                print(f"Error evaluating {variable}: {e}")

# Example usage
file_path = 'answers.txt'
evaluate_and_print_v4_variables(file_path)
