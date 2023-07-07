import openpyxl

input_file = 'input.xlsx'
output_file = 'output.txt'

# Load the workbook
workbook = openpyxl.load_workbook(input_file)

# Select the active sheet
sheet = workbook.active

# Open the output file in write mode
with open(output_file, 'w') as file:
    # Iterate over the rows in the selected column
    for row in sheet.iter_rows(values_only=True):
        if row[0]:
            # Split the cell value by comma and space
            words = row[0].split(', ')

            # Write each word on a separate line in the output file
            file.writelines(word + '\n' for word in words)
