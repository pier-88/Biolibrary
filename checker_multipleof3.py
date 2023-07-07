import os
from Bio import SeqIO

# Function to check if sequence length is a multiple of 3
def is_multiple_of_3(sequence):
    return len(sequence.seq) % 3 == 0

# Function to process files in a directory (including subdirectories)
def process_files(directory):
    total_files = 0
    passed_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fa') or file.endswith('.fasta'):
                total_files += 1
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as handle:
                    sequences = list(SeqIO.parse(handle, 'fasta'))

                # Check if all sequences in the file have length multiple of 3
                if all(is_multiple_of_3(seq) for seq in sequences):
                    passed_files += 1
                    print(f"All sequences in {file} have a length multiple of 3.")
                else:
                    print(f"Not all sequences in {file} have a length multiple of 3.")

    # Calculate the percentage of files that passed
    percentage_passed = (passed_files / total_files) * 100
    print(f"Percentage of files passed: {percentage_passed:.2f}%")

# Get the current working directory
directory = os.getcwd()

# Process files in the current directory and subdirectories
process_files(directory)
