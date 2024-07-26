# ProcessIPMS
 Processing Pipeline for IPMS data

## Introduction

This pipeline processes protein interaction data files to filter, annotate, and combine the data, creating the necessary input files for SAINTexpress. It supports multiple replicates and control files, and generates a combined interaction, prey, and bait file for downstream analysis.

## Requirements

- Python 3.x
- pandas
- re
- SAINTexpress-spc

You can install the required Python packages using:
```bash
pip install pandas

## Usage
1. Clone the repository:
git clone https://github.com/your_username/repo_name.git
cd repo_name
2. Place your input files in the ./01_CleanInput/ directory.

3. Modify the main function at the end of the script to include your specific settings for replicates and controls.

4. Run the script:
```bash
python process_IPMS.py

Running the Script

The script can be customized for different experiments by modifying the main function. For example:
```python
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
    main('Preips_ARID3B', preips_arid3b_replicates, control_replicates)
    
    # Preips_BRD4 settings
    preips_brd4_replicates = {
        1: './01_CleanInput/MS241058-S1-1.txt',
        2: './01_CleanInput/MS241058-S1-2.txt'
    }
    control_replicates = {
        1: './01_CleanInput/MS241058-S46-1.txt',
        2: './01_CleanInput/MS241058-S46-2.txt'
    }
    main('Preips_BRD4', preips_brd4_replicates, control_replicates)

## Function Descriptions
- create_output_dir(output_dir): Creates the specified output directory if it does not already exist.
- process_interaction(file, label, replicate, output_dir): Processes interaction data by filtering, annotating, and saving the processed data.
- process_prey(file, label, replicate, output_dir): Processes prey data by filtering, extracting gene IDs, and saving the processed data.
- combine_files(files, output_file, column_replace=False): Combines multiple files into a single file, optionally replacing hyphens with underscores.
- create_bait_file(bait_data, output_file): Creates a bait file with the specified data.
- run_saintexpress(interaction_file, prey_file, bait_file, output_dir): Runs SAINTexpress with the specified interaction, prey, and bait files, and moves the resulting list.txt file to the output directory.

## Contact
For any questions or issues, please contact o.sj@live.com