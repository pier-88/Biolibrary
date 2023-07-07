import requests
import os

def retrieve_gene_sequence(ensembl_gene_id):
    base_url = "https://rest.ensembl.org"
    endpoint = f"/sequence/id/{ensembl_gene_id}?"

    # Set the desired content type to fasta
    headers = {"Content-Type": "text/x-fasta"}

    # Send GET request to Ensembl REST API
    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve gene sequence for {ensembl_gene_id}")
        return None

def save_sequence_to_file(gene_id, sequence):
    filename = f"{gene_id}.fasta"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w") as file:
        file.write(sequence)

    print(f"Sequence saved to {filename}")

# Example usage
gene_id = "ENSG00000139618"  # Replace with your desired Ensembl gene ID
sequence = retrieve_gene_sequence(gene_id)

if sequence:
    save_sequence_to_file(gene_id, sequence)
