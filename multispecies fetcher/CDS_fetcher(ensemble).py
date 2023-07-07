import ensembl_rest
import os
from tqdm import tqdm

# Read species and gene symbols from a text file
with open('list.txt', 'r') as f:
    lines = f.read().splitlines()
    spc = lines[0].split(', ')
    listSymb = lines[1:]

# Create a directory to store the fetched CDS sequences
output_dir = 'Fetched CDS sequences'
os.makedirs(output_dir, exist_ok=True)

# Count the total number of iterations
total_iterations = len(spc) * len(listSymb)

# Initialize the progress bar
progress_bar = tqdm(total=total_iterations, desc='Fetching CDS sequences')

for species in spc:
    for symbol in listSymb:
        try:
            data = ensembl_rest.symbol_post(species=species, params={'symbols': [symbol]})

            if symbol in data:
                canid = data[symbol]['canonical_transcript']

                cut_string = canid.split('.')
                new_canid = cut_string[0]

                canid_fasta = ensembl_rest.sequence_id(new_canid,
                                                       headers={'content-type': 'text/x-fasta'},
                                                       params={'type': 'cds'})

                header, sequence = canid_fasta.split('\n', 1)
                symbol_dir = os.path.join(output_dir, symbol)
                os.makedirs(symbol_dir, exist_ok=True)

                # Create a new header
                new_header = f'>{symbol}_{species}_{new_canid}'

                # Write the output directly to a file in the symbol directory
                output_file = os.path.join(symbol_dir, f'{symbol}_{species}.fasta')
                with open(output_file, 'w') as f:
                    f.write(new_header + '\n' + sequence)
                    progress_bar.set_description(f"CDS sequence fetched for {symbol} in {species}")

            else:
                progress_bar.set_description(f"No CDS data found for {symbol} in {species}")

        except Exception as e:
            progress_bar.set_description(f"Error processing {symbol}: {e}")

        progress_bar.update(1)

progress_bar.close()
print("Finished!")
