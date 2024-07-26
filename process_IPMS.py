# -*- coding: utf-8 -*-
import os
import pandas as pd
import re

def create_output_dir(output_dir):
    """
    Create the output directory if it does not already exist.
    """
    os.makedirs(output_dir, exist_ok=True)

def process_interaction(file, label, replicate, output_dir):
    """
    Process interaction data:
    - Read the input file into a DataFrame.
    - Filter out rows containing 'heavy chain' or 'light chain' in the 'Description' column.
    - Extract relevant columns and insert 'Replicate' and 'Label' columns.
    - Save the processed data to a new file.
    """
    df = pd.read_csv(file, sep='\t', header=0)
    df = df[~df['Description'].astype(str).str.contains('heavy chain|light chain', na=False)]
    interaction_data = df[['Accession', '# PSMs']].copy()
    interaction_data.insert(0, 'Replicate', f'{label}_R{replicate}')
    interaction_data.insert(1, 'Label', label)
    interaction_data.to_csv(f'{output_dir}/interaction_{label}{replicate}.data', sep='\t', index=False, header=False)

def process_prey(file, label, replicate, output_dir):
    """
    Process prey data:
    - Read the input file into a DataFrame.
    - Filter out rows containing 'heavy chain' or 'light chain' in the 'Description' column.
    - Extract relevant columns and add a 'GeneID' column.
    - Save the processed data to a new file.
    """
    df = pd.read_csv(file, sep='\t', header=0)
    df = df[~df['Description'].astype(str).str.contains('heavy chain|light chain', na=False)]
    print(f"Filtered data from {file}:")
    print(df.head())
    prey_data = df[['Accession', '# AAs']].copy()
    prey_data['GeneID'] = df['Description'].astype(str).apply(lambda x: re.search(r'GN=(.*?)\s', x).group(1) if re.search(r'GN=(.*?)\s', x) else x)
    print(f"Processed prey data:")
    print(prey_data.head())
    prey_data.to_csv(f'{output_dir}/prey_{label}{replicate}.data', sep='\t', index=False, header=False)

def combine_files(files, output_file, column_replace=False):
    """
    Combine multiple files into a single file:
    - Read each file into a DataFrame and concatenate them.
    - Optionally replace hyphens with underscores in the first column.
    - Drop duplicate rows.
    - Save the combined data to a new file.
    """
    combined_df = pd.concat([pd.read_csv(file, sep='\t', header=None) for file in files])
    if column_replace:
        combined_df[combined_df.columns[0]] = combined_df[combined_df.columns[0]].astype(str).str.replace('-', '_', regex=True)
    combined_df = combined_df.drop_duplicates()
    combined_df.to_csv(output_file, sep='\t', index=False, header=False)

def create_bait_file(bait_data, output_file):
    """
    Create a bait file with the specified data.
    """
    with open(output_file, 'w') as bait_file:
        for line in bait_data:
            bait_file.write(line)

def run_saintexpress(interaction_file, prey_file, bait_file, output_dir):
    """
    Run SAINTexpress with the specified interaction, prey, and bait files.
    Move the resulting list.txt file to the output directory.
    """
    os.system(f'SAINTexpress-spc {interaction_file} {prey_file} {bait_file}')
    os.system(f'mv list.txt {output_dir}/')

def main(label, replicates, controls):
    """
    Main function to process interaction and prey files for the specified label and controls.
    """
    output_dir = f"./02_Output/{label}"
    create_output_dir(output_dir)
    
    # Process interaction files
    for replicate, file in replicates.items():
        process_interaction(file, label, replicate, output_dir)
    for replicate, file in controls.items():
        process_interaction(file, "Control", replicate, output_dir)

    interaction_files = [f'{output_dir}/interaction_{label}{replicate}.data' for replicate in replicates] + \
                        [f'{output_dir}/interaction_Control{replicate}.data' for replicate in controls]
    combine_files(interaction_files, f'{output_dir}/interaction.data')

    # Process prey files
    for replicate, file in replicates.items():
        process_prey(file, label, replicate, output_dir)
    for replicate, file in controls.items():
        process_prey(file, "Control", replicate, output_dir)

    prey_files = [f'{output_dir}/prey_{label}{replicate}.data' for replicate in replicates] + \
                 [f'{output_dir}/prey_Control{replicate}.data' for replicate in controls]
    combine_files(prey_files, f'{output_dir}/prey.data', column_replace=True)

    # Create bait file
    bait_data = [f"{label}_R{replicate}\t{label}\tT\n" for replicate in replicates] + \
                [f"Control_R{replicate}\tControl\tC\n" for replicate in controls]
    create_bait_file(bait_data, f'{output_dir}/bait.data')

    # Run SAINTexpress
    run_saintexpress(f'{output_dir}/interaction.data', f'{output_dir}/prey.data', f'{output_dir}/bait.data', output_dir)

if __name__ == "__main__":
    # Preips_ARID3B settings
    preips_arid3b_replicates = {
        1: './01_CleanInput/MS241058-R1-1.txt',
        2: './01_CleanInput/MS241058-R1-2.txt'
    }
    control_replicates = {
        1: './01_CleanInput/MS241058-R46-1.txt',
        2: './01_CleanInput/MS241058-R46-2.txt'
    }
    main('R1_SOX2', preips_arid3b_replicates, control_replicates)
    
    # Preips_BRD4 settings
    preips_brd4_replicates = {
        1: './01_CleanInput/MS241058-S1-1.txt',
        2: './01_CleanInput/MS241058-S1-2.txt'
    }
    control_replicates = {
        1: './01_CleanInput/MS241058-S46-1.txt',
        2: './01_CleanInput/MS241058-S46-2.txt'
    }
    main('NSC_SOX2', preips_brd4_replicates, control_replicates)
