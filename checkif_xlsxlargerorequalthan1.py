import os
import pandas as pd

# Get the current directory
current_dir = os.getcwd()

# List all files in the directory
files = [f for f in os.listdir(current_dir) if f.endswith('.xlsx') and not f.startswith('~')]

# Check if there are any .xlsx files in the directory
if len(files) == 0:
    raise ValueError("No .xlsx files found in the directory.")

# Iterate over each .xlsx file
for file in files:
    file_path = os.path.join(current_dir, file)

    try:
        # Load the Excel file into a Pandas DataFrame
        df = pd.read_excel(file_path)

        # Convert the DataFrame to a numpy array so we can iterate over it
        array = df.to_numpy()

        # Iterate over each element in the array
        for row in array:
            for value in row:
                # Try to convert the value to a float
                try:
                    num = float(value)
                    if num >= 1:
                        print(f"Found a number larger than 1 in '{file}'")
                        break
                except ValueError:
                    # If the conversion fails, it's not a number and we can continue to the next cell
                    continue
            else:
                continue
            break

    except Exception as e:
        print(f"Error loading '{file}': {e}")
