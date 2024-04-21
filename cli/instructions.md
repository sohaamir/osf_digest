# OSF Preprint Summarizer
A command-line tool to retrieve and summarize preprints from the Open Science Framework (OSF).

## Installation
Clone the repository:
`git clone https://github.com/sohaamir/osf_digest.git`

Change to the project directory:
`cd osf_digest`

Install the required dependencies:
`pip install -r requirements.txt`

Install the CLI tool:
`python setup.py install`

## Usage
To run the OSF Preprint Summarizer, use the following command:
```bash
osf_digest --disciplines <discipline1> <discipline2> ... --days <days> --pagesize <pagesize> --max_length <max_length> --min_length <min_length> --osf_token <osf_token> --hf_token <hf_token>
Arguments
--disciplines: List of disciplines to retrieve preprints from (default: ['Psychiatry'])
--days: Number of days to summarize since today (default: 7, range: 0-365)
--pagesize: Number of preprints to retrieve per request (default: 100)
--max_length: Maximum length of the generated summary (default: 170)
--min_length: Minimum length of the generated summary (default: 30)
```

Example
```bash
osf_digest --disciplines "Psychiatry" "Neuroscience" --days 14 --pagesize 50 --max_length 200 --min_length 50 --osf_token YOUR_OSF_TOKEN --hf_token YOUR_HF_TOKEN
```
This command will retrieve preprints from the "Psychiatry" and "Neuroscience" disciplines published in the last 14 days, with a page size of 50 preprints per request. The generated summaries will have a maximum length of 200 and a minimum length of 50.

## Output
The tool will save the retrieved preprints as JSON files in the data/json directory and as a CSV file in the data/csv directory. The generated discipline summaries will be saved as a CSV file in the output/digests directory.

## License
This project is licensed under the MIT License.

This documentation provides an overview of the OSF Preprint Summarizer, including installation instructions, usage examples, and information about the output files.