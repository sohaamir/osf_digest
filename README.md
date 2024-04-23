# OSF Preprint Digest
OSF Preprint Digest is a command-line tool that retrieves preprints from the Open Science Framework (OSF) based on specified disciplines and generates concise summaries of the preprints using the [BART-large-CNN model](https://huggingface.co/facebook/bart-large-cnn). I was surprised to see that there was (to my knowledge at least) no readily available tool which summarises published articles in this way, so I decided to make it myself 🙂

## Functionality
- The tool filters the preprints to include only those with English abstracts, processes the abstracts, and splits them into smaller chunks for better summarization.
- It also separately retrieves citation information for each preprint including the author list, which is combined with the abstract.
- The retrieved preprints are saved as JSON files for further analysis, and the BART-large-CNN model is used to generate concise summaries of the preprints.
- Finally, the preprint summaries are organized by discipline and saved as CSV files for easy access and review.

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

which will install the following:

```bash
requests
tqdm
unidecode
langdetect
transformers
torch
python-dotenv
```

Install the CLI tool from the project root:
```bash
pip install -e .
```

## Configuration
Before running the OSF Preprint Digest tool, you need to set up the necessary API tokens, which we can then load into the script using `dotenv`.

Create a file named `.env` in the project root directory.
Open the `.env` file and add the following lines:

```bash
OSF_TOKEN=your_osf_token
HF_TOKEN=your_hf_token
```

Replace your_osf_token with your OSF API token and your_hf_token with your Hugging Face API token. Both are freely available on the respective websites, you just need to make an account.

Your folder structure should look something like this:

├── README.md
├── cli
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   └── cli.cpython-311.pyc
│   ├── cli.py
│   └── instructions.md
├── data
│   ├── csv
│   │   ├── 2024-04-14_osf_digest.csv
│   │   └── 2024-04-21_osf_digest.csv
│   └── json
│       ├── behavioural_neuroscience_preprints.json
│       ├── cognitive_neuroscience_preprints.json
│       ├── education_preprints.json
│       ├── memory_preprints.json
│       ├── mental_health_preprints.json
│       └── psychiatry_preprints.json
├── osf_digest.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── requires.txt
│   └── top_level.txt
├── output
│   └── digests
│       ├── 2024-04-14_discipline_summaries.csv
│       └── 2024-04-21_discipline_summaries.csv
├── request_preprints.py
├── requirements.txt
└── setup.py

## How the script works

We firstly import a number of external modules/packages:

```python
import requests
import json
from datetime import datetime, timedelta
from tqdm import tqdm
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from langdetect import detect
import csv
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
import torch
from dotenv import load_dotenv
```

- `requests` to get the information from OSF
- `datetime` to set the length of time for the request to cover
- `tqdm` for progress bars when pulling the information
- `unidecode` to sort out pesky characters (most commonly in author's names)
- `concurrent.futures` to speed things up
- `langdetect` to remove non-English abstracts
- `transformers` and `torch` to run the BART model
- `dotenv` to load the environmental variables (our OSF and Hugging Face tokens)

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
