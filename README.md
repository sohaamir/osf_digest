# OSF Preprint Digest
OSF Preprint Digest is a command-line tool that retrieves preprints from the Open Science Framework (OSF) based on specified disciplines and generates concise summaries of the preprints using the BART-large-CNN model. The tool allows users to stay updated with the latest research in their fields of interest by providing a digestible overview of recently published preprints.

## Features
- Retrieve preprints from OSF based on user-specified disciplines
- Filter preprints published within a specified number of days
- Generate concise summaries of the preprints using the BART-large-CNN model
- Save the retrieved preprints as JSON files for further analysis
- Create CSV files containing the preprint summaries organized by discipline

## How It Works
The OSF Preprint Digest tool retrieves preprints from the Open Science Framework (OSF) based on user-specified disciplines and date range using the OSF API. It filters the preprints to include only those with English abstracts, processes the abstracts, and splits them into smaller chunks for better summarization. The tool also retrieves citation information for each preprint using the OSF API. The retrieved preprints are saved as JSON files for further analysis, and the BART-large-CNN model is used to generate concise summaries of the preprints. Finally, the preprint summaries are organized by discipline and saved as CSV files for easy access and review.

## Installation
Clone the repository:
```bash
git clone https://github.com/sohaamir/osf_digest.git
```

Change to the project directory:
```bash
cd osf-preprint-digest
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Install the CLI tool:
```bash
pip install -e .
```

## Configuration
Before running the OSF Preprint Digest tool, you need to set up the necessary API tokens.

Create a file named .env in the project root directory.
Open the .env file and add the following lines:

```bash
OSF_TOKEN=your_osf_token
HF_TOKEN=your_hf_token
```

Replace your_osf_token with your OSF API token and your_hf_token with your Hugging Face API token.

## Usage
To run the OSF Preprint Digest tool, use the following command:

```bash
osf_digest --disciplines <discipline1> <discipline2> ... --days <days> --pagesize <pagesize> --max_length <max_length> --min_length <min_length>
```

Arguments
```bash
--disciplines: List of disciplines to retrieve preprints from (default: ['Psychiatry'])
--days: Number of days to summarize since today (default: 7, range: 0-365)
--pagesize: Number of preprints to retrieve per request (default: 100)
--max_length: Maximum length of the generated summary (default: 170)
--min_length: Minimum length of the generated summary (default: 30)
```

Example
```bash
osf_digest --disciplines "Psychiatry" "Neuroscience" --days 14 --pagesize 50 --max_length 200 --min_length 50
```
This command will retrieve preprints from the "Psychiatry" and "Neuroscience" disciplines published in the last 14 days, with a page size of 50 preprints per request. The generated summaries will have a maximum length of 200 and a minimum length of 50.

### Output
The OSF Preprint Digest tool generates the following output files:

- JSON files containing the retrieved preprints, saved in the data/json directory
- A CSV file containing the preprint summaries, saved in the data/csv directory
- A CSV file containing the discipline-wise summaries, saved in the output/digests directory

## Dependencies
The OSF Preprint Digest tool relies on the following dependencies:

```bash
Python 3.6+
requests
tqdm
unidecode
langdetect
transformers
torch
python-dotenv
```

These dependencies are listed in the requirements.txt file and can be installed using pip install -r requirements.txt.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## Acknowledgements
This tool utilizes the Open Science Framework (OSF) API for retrieving preprints.
The preprint summaries are generated using the BART-large-CNN model from Hugging Face.

## Contact
If you have any questions or need further assistance, please contact me at axs2210@bham.ac.uk or open a thread!