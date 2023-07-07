library(seqinr)
library(openxlsx)
library(ape)
library(phylotools)
library(phangorn)

# Define the ka function
ka <- function(file_path, output_file) {
  gene_name <- tools::file_path_sans_ext(basename(file_path))
  alignment <- read.alignment(file_path, format = "fasta")
  
  # Perform error handling for kaks calculation
  tryCatch({
    kaks_result <- kaks(alignment)
    kadf <- as.data.frame(as.matrix(kaks_result$ka))
    ksdf <- as.data.frame(as.matrix(kaks_result$ks))
    kratio <- data.frame(asd = colnames(kadf), kadf / ksdf)
    names(kratio)[1] <- paste(gene_name, "_kaks", sep = "")
    xlsx_filename <- paste0(gene_name, "_kaks.xlsx")
    write.xlsx(kratio, file = xlsx_filename, colNames = TRUE)
    
    # Filter results where Ka/Ks is larger than 1
    filtered_results <- kratio[kratio[, 2] > 1, ]
    
    # Write the filtered results to a text file
    if (nrow(filtered_results) > 0) {
      species_combinations <- apply(filtered_results, 1, function(row) paste(row[2], row[1], sep = " - "))
      results <- paste(species_combinations, gene_name)
      writeLines(results, output_file, sep = "\n")
    }
    
    # tree
    tree <- nj(dist.alignment(alignment))
    png(paste0(gene_name, "_tree_plot.png"), width = 800, height = 600)
    plot(tree)
    dev.off()
    nwk_filename <- paste0(gene_name, ".nwk")
    write.tree(tree, file = nwk_filename)
  }, error = function(e) {
    print(paste("Error processing:", gene_name))
    print(e)
  })
}

# Search for .fa and .fasta files in the script's directory
fasta_files <- list.files(pattern = "\\.fa$|\\.fasta$")

# Output file path
output_file <- "ka_output.txt"

# Process each .fa or .fasta file
for (file in fasta_files) {
  file_path <- file
  ka(file_path, output_file)
}
