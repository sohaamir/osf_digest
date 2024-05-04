# OSF Preprint Digest
OSF Preprint Digest is a command-line tool that retrieves preprints from the Open Science Framework (OSF) generating concise summaries using the [BART-large-CNN model](https://huggingface.co/facebook/bart-large-cnn). I was surprised to see that there was (to my knowledge at least) no readily available tool that summarises published articles in this way, so I decided to make it myself 🙂

## Functionality
- The tool allows the user to specify the date interval for abstracts (i.e., the period from the request), as well as the discipline.
- API calls are separately made for both the abstract and the author list, which are then combined.
- It filters the preprints to include only those with English abstracts.

## Installation
Clone the repository:
```bash
git clone https://github.com/sohaamir/osf_digest.git
```

Change to the project directory:
```bash
cd osf_digest
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
To run the script, you need to set up the necessary API tokens, which we can then load into the script using `dotenv`.

To do this: 
- Create a file named `.env` in the project root directory.
- Open the `.env` file and add the following lines:

```bash
OSF_TOKEN=your_osf_token
HF_TOKEN=your_hf_token
```

Replace your_osf_token with your OSF API token and your_hf_token with your Hugging Face API token. Both are freely available on the respective websites, you just need to make an account.

Your folder structure should look (something) like this:

```
├── LICENSE
├── README.md
├── cli
│   ├── __init__.py
│   ├── cli.py
│   └── instructions.md
├── data
│   ├── csv
│   │   ├── 2024-04-14_osf_digest.csv
│   │   └── 2024-04-21_osf_digest.csv
│   └── json
│       ├── behavioural_neuroscience_preprints.json
│       ├── cognitive_neuroscience_preprints.json
│       ├── education_preprints.json
│       ├── memory_preprints.json
│       ├── mental_health_preprints.json
│       └── psychiatry_preprints.json
├── osf_digest.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── entry_points.txt
│   ├── requires.txt
│   └── top_level.txt
├── output
│   └── digests
│       ├── 2024-04-14_discipline_summaries.csv
│       └── 2024-04-21_discipline_summaries.csv
├── request_preprints.py
├── requirements.txt
└── setup.py
```

(I have decided to include some example outputs with the folder, but feel free to delete them. The actual CLI code is contained within /cli/cli.py but the 'barebones' Python code is also provided in the request_preprints.py script in the repository's root.)

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

All disciplines on OSF are supported, please visit the OSF website for a complete list. You can see the discipline list for a preprint on it's webpage.

### Output
The OSF Preprint Digest tool generates the following output files:

- JSON files containing the retrieved preprints, saved in the data/json directory (a single example):

```json
{
        "id": "j726r",
        "title": "How visual experience shapes body representation",
        "authors": [
            "Shahzad, Iqra",
            "Occelli, Valeria",
            "Giraudet, Eleonore",
            "Azanon, Elena",
            "Longo, Matthew",
            "Moruaux, Andre",
            "Collignon, Olivier"
        ],
        "abstract": [
            "We do not have a veridical representation of our body in our mind. For instance,",
            "tactile distances of equal measure along the medial-lateral axis of our limbs are generally perceived",
            "as larger than those running along the proximal-distal axis. This anisotropy in tactile distances reflects",
            "distortions in body-shape representation, such that the body parts are perceived as wider than they",
            "are. While the origin of such anisotropy remains unknown, it has been suggested that visual",
            "experience could partially play a role in its manifestation. To causally test the role of",
            "visual experience on body shape representation, we investigated tactile distance perception in sighted and early",
            "blind individuals comparing medial-lateral and proximal-distal tactile distances of stimuli presented on the ventral and",
            "dorsal part of the forearm, wrist, and hand. Overestimation of distances in the medial-lateral over",
            "proximal-distal body axes were found in both sighted and blind people, but the magnitude of",
            "the anisotropy was significantly reduced in the forearms of blind people. We conclude that tactile",
            "distance perception is mediated by similar mechanisms in both sighted and blind people, but that",
            "visual experience can modulate the tactile distance anisotropy."
        ],
        "date_published": "2024-04-20T16:07:35.153014",
        "license": "563c1cf88c5e4a3877f9e96c",
        "disciplines": [
            "Psychiatry"
        ],
        "tags": [
            "blindness",
            "tactile distance anisotropy",
            "touch",
            "vision"
        ]
    },
```

- A CSV file containing the preprint summaries, saved in the data/csv directory:

| title                                                        | authors                                                      | abstract                                                     | disciplines |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------- |
| The architecture of spontaneous thoughts  and experiences: a graph theory approach. | Coppola, Peter; Sikka, Pilleriin; Valli, Katja; Tuominen, Jarno;  Revonsuo, Antti; Loukola, Ville; Bernstein, Ryan; , nanna.strif; Kirberg,  Manuela; Ezquerro-Nassar, Alejandro; Windt, Jennifer; Noreika, Valdas; mota,  natalia; Bekinschtein, Tristan | The language people use in everyday life provides a window into the mind.  Mind-wandering and dreams have been thought to reflect unique individual  differences and mental health. Here we use a large dataset of mind-wandering  (n=1619) and dream (n=1434) reports from 176 individuals in conjunction with  graph theory applied to natural language. We find that dream reports have a  more complex structure, while mind-wandering reports have fewer word  repetitions and more verbose structure, with essential nodal points in the  narrative flux. Dream reports tend to have more thematic repetitions, local  cliques, and global integration. Capitalising on a repeated measures design,  we found that the structure of dream and mind-wandering reports contains  individual-specific information. Finally, we find that word centrality in  dreams is predictive of depression symptoms. Thus, this approach is sensitive  to individual differences, quantitatively differentiates two distinct  contents of consciousness, and seems promising for cost-effective analyses of  large naturalistically occurring qualitative datasets. | Psychiatry  |
| How visual experience shapes body  representation            | Shahzad, Iqra; Occelli, Valeria; Giraudet, Eleonore; Azanon, Elena;  Longo, Matthew; Moruaux, Andre; Collignon, Olivier | We do not have a veridical representation of our body in our mind. For  instance, tactile distances of equal measure along the medial-lateral axis of  our limbs are generally perceived as larger than those running along the  proximal-distal axis. This anisotropy in tactile distances reflects  distortions in body-shape representation, such that the body parts are  perceived as wider than they are. While the origin of such anisotropy remains  unknown, it has been suggested that visual experience could partially play a  role in its manifestation. To causally test the role of visual experience on  body shape representation, we investigated tactile distance perception in  sighted and early blind individuals comparing medial-lateral and  proximal-distal tactile distances of stimuli presented on the ventral and  dorsal part of the forearm, wrist, and hand. Overestimation of distances in  the medial-lateral over proximal-distal body axes were found in both sighted  and blind people, but the magnitude of the anisotropy was significantly  reduced in the forearms of blind people. We conclude that tactile distance  perception is mediated by similar mechanisms in both sighted and blind  people, but that visual experience can modulate the tactile distance  anisotropy. | Psychiatry  |
| Towards understanding and halting  legacies of trauma        | Taylor, William; Korobkova, Laura; Bhinderwala, Nabeel; Dias, Brian G | Echoes of natural and anthropogenic traumas not only reverberate within  the physiology, biology, and neurobiology of the generation directly exposed  to them but also within the biology of future generations. With the intent of  understanding this phenomenon, significant efforts have sought to establish  multi-generational legacies of experiences like stress, chemical exposures,  nutritional impoverishment, and chemosensory experiences. From these studies,  we are gaining new appreciation for how legacies of trauma come to be  bequeathed to future generations. This review first outlines principles that  merit attention in the study of multi-generational legacies of trauma. Next,  it discusses causes and consequences that allow for such legacies to  perpetuate across generations. Finally, we discuss silver linings of such  legacies and how legacies of flourishing can be engineered. In summary, this  review synthesizes our current understanding of the concept, causes and  consequences of legacies of trauma and looks to opportunities to halt them. | Psychiatry  |
|                                                              |                                                              |                                                              |             |

- A CSV file containing the discipline-wise summaries, saved in the output/digests directory (the summaries generated by the BART model):

| Title                                                        | Authors                                                      | Summary                                                      | Discipline |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------- |
| The architecture of spontaneous thoughts and  experiences: a graph theory approach. | Coppola, Peter; Sikka, Pilleriin; Valli, Katja; Tuominen, Jarno;  Revonsuo, Antti; Loukola, Ville; Bernstein, Ryan; , nanna.strif; Kirberg,  Manuela; Ezquerro-Nassar, Alejandro; Windt, Jennifer; Noreika, Valdas; mota,  natalia; Bekinschtein, Tristan | The language people use in everyday life provides a window into the mind.  Mind-wandering and dreams have been thought to reflect unique individual  differences and mental health. We find that dream reports have a more complex  structure. We also find that word centrality in dreams is predictive of  depression symptoms. | Psychiatry |
| How visual experience shapes body  representation            | Shahzad, Iqra; Occelli, Valeria; Giraudet, Eleonore; Azanon, Elena;  Longo, Matthew; Moruaux, Andre; Collignon, Olivier | We do not have a veridical representation of our body in our mind. For  instance, tactile distances of equal measure along the medial-lateral axis of  our limbs are generally perceived as larger than those running along the  proximal-distal axis. This anisotropy in tactile distances reflects  distortions in body-shape representation. | Psychiatry |
| Towards understanding and halting  legacies of trauma        | Taylor, William; Korobkova, Laura; Bhinderwala, Nabeel; Dias, Brian G | Echoes of natural and anthropogenic traumas reverberate within the  physiology, biology, and neurobiology of the generation directly exposed to  them. With the intent of understanding this phenomenon, significant efforts  have sought to establish multi-generational legacies of experiences like  stress, chemical exposures, nutritional impoverishment, and chemosensory  experiences. | Psychiatry |

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements
This tool utilizes the Open Science Framework (OSF) API for retrieving preprints.
The preprint summaries are generated using the BART-large-CNN model from Hugging Face.

## Contact
If you have any questions or need further assistance, please contact me at axs2210@bham.ac.uk or open a thread!
