from Bio import Entrez
from Bio import SeqIO

def fetch_transcript_sequences(gene_name, output_file):
    Entrez.email = 'your_email@example.com'  # Enter your email address here

    # Search for the gene by name and retrieve the first matching transcript
    term = f'{gene_name}[Gene] AND Homo sapiens[Organism] AND mRNA[Filter]'
    handle = Entrez.esearch(db='nuccore', term=term)
    record = Entrez.read(handle)
    handle.close()

    # Get the transcript ID for the first result
    transcript_id = record['IdList'][0]

    # Fetch the transcript record in FASTA format
    handle = Entrez.efetch(db='nuccore', id=transcript_id, rettype='fasta', retmode='text')
    transcript_record = handle.read()
    handle.close()

    # Save the transcript sequence to a FASTA file
    with open(output_file, 'w') as file:
        file.write(transcript_record)

    return transcript_record

# Fetch and save the transcript sequence for BRCA2
gene_name = 'BRCA2'
output_file = 'BRCA2_transcript.fasta'
transcript_sequence = fetch_transcript_sequences(gene_name, output_file)

print(f"Transcript sequence for {gene_name} saved in {output_file}")
