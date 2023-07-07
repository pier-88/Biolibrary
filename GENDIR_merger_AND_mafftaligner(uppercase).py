from Bio import SeqIO
from Bio.Align.Applications import MafftCommandline
from io import StringIO
import os
from tqdm import tqdm

# Get the current directory
current_dir = os.getcwd()

# Get the path to the "Alignments" directory
alignments_dir = os.path.join(current_dir, "Alignments")
os.makedirs(alignments_dir, exist_ok=True)

# Get the list of subdirectories
subdirectories = [f for f in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, f))]

# Check if there are any subdirectories
if len(subdirectories) == 0:
    raise ValueError("No subdirectories found.")

# Iterate over each subdirectory
for subdir in tqdm(subdirectories, desc="Processing subdirectories"):
    # Move into the subdirectory
    subdirectory_path = os.path.join(current_dir, subdir)
    os.chdir(subdirectory_path)

    # List all files in the subdirectory
    files = [f for f in os.listdir(subdirectory_path) if f.endswith('.fa') or f.endswith('.fasta')]

    # Check if there are any files in the subdirectory
    if len(files) == 0:
        print(f"No .fa or .fasta files found in the subdirectory '{subdir}'. Skipping.")
        continue

    # Read the first file to extract its name
    first_file = files[0]
    output_filename = os.path.splitext(first_file)[0]

    # Merge sequences from each file
    merged_seqs = []
    for file in files:
        for record in SeqIO.parse(file, 'fasta'):
            merged_seqs.append(record)

    # Define output file paths
    merged_output_file = os.path.join(subdirectory_path, f'merged_{output_filename}.fasta')
    alignment_output_file = os.path.join(subdirectory_path, f'alignment_{output_filename}.fasta')

    # Write merged sequences to a new FASTA file
    SeqIO.write(merged_seqs, merged_output_file, 'fasta')

    # Convert merged sequences to uppercase if not already
    merged_seqs = [seq.upper() for seq in merged_seqs]

    # Perform multiple sequence alignment using 'mafft'
    mafft_cline = MafftCommandline(input=merged_output_file)
    alignment = mafft_cline()

    # Convert alignment to uppercase if not already
    alignment_stdout, _ = alignment
    alignment_stdout = alignment_stdout.upper()

    # Write the merged sequences to an output file, converting to uppercase if not already
    with open(merged_output_file, 'w') as f:
        for seq in merged_seqs:
            f.write(f'>{seq.id}\n{str(seq.seq)}\n')

    # Write the alignment to an output file
    with open(alignment_output_file, 'w') as f:
        f.write(alignment_stdout)

    # Move the alignment and merged files to the "Alignments" directory
    alignment_file_dest = os.path.join(alignments_dir, os.path.basename(alignment_output_file))
    merged_file_dest = os.path.join(alignments_dir, os.path.basename(merged_output_file))
    os.rename(alignment_output_file, alignment_file_dest)
    os.rename(merged_output_file, merged_file_dest)

# Return to the initial directory
os.chdir(current_dir)
