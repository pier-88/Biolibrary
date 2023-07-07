# Load required libraries
library(seqinr)
library(tools)

# Get the current directory
current_dir <- getwd()

# List all files in the directory
files <- list.files(current_dir, pattern = "\\.fa$|\\.fasta$", full.names = TRUE)

# Check if there are any files in the directory
if (length(files) == 0) {
  stop("No .fa or .fasta files found in the directory.")
}

# Read the first file to extract its name
first_file <- files[1]
output_filename <- file_path_sans_ext(basename(first_file))

# Merge sequences from each file
merged_seqs <- NULL
for (file in files) {
  seqs <- read.fasta(file)
  seqs <- lapply(seqs, toupper)
  merged_seqs <- c(merged_seqs, seqs)
}

# Define output file path
output_file <- file.path(current_dir, paste0("merged_", output_filename, ".fasta"))

# Write merged sequences to a new FASTA file
write.fasta(sequences = merged_seqs, names = names(merged_seqs), file.out = output_file)
