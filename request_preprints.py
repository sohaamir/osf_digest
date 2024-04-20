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

# Set up API endpoint and parameters
osf_url = "https://api.osf.io/v2/preprints/"
disciplines = ['Psychiatry']
data_folder = "data/json"
csv_folder = "data/csv"

# Retrieve the OSF_TOKEN environment variable
osf_token = os.getenv("OSF_TOKEN")
if not osf_token:
    raise ValueError("OSF_TOKEN environment variable not set")

# Set up authentication header with your access token
headers = {
    "Authorization": f"Bearer {osf_token}"
}

# Create the data folder if it doesn't exist
os.makedirs(data_folder, exist_ok=True)
os.makedirs(csv_folder, exist_ok=True)

def normalize_text(text):
    return unidecode(text)

def split_abstract(abstract, max_words_per_line=15):
    words = abstract.split()
    lines = []
    current_line = []
    for word in words:
        if len(current_line) < max_words_per_line:
            current_line.append(word)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def process_citation(preprint, headers):
    citation_url = f"https://api.osf.io/v2/preprints/{preprint['id']}/citation/?style=chicago-author-date"
    response = requests.get(citation_url, headers=headers)
    if response.status_code == 200:
        citation_data = response.json()
        authors = [normalize_text(f"{author['family']}, {author['given']}") for author in citation_data["data"]["attributes"]["author"]]
        preprint["authors"] = authors
    else:
        print(f"Request failed for preprint {preprint['id']} with status code: {response.status_code}")
    return preprint

def is_english(text):
    try:
        language = detect(text)
        return language == 'en'
    except:
        return False

all_preprints = []

for discipline in disciplines:
    print(f"Processing discipline: {discipline}")

    filename = f"{discipline.lower().replace(' ', '_')}_preprints.json"
    filepath = os.path.join(data_folder, filename)

    preprints = []

    osf_params = {
        "filter[date_created][gte]": (datetime.now() - timedelta(days=7)).isoformat(),  # Define number of days to summarise since today
        "filter[subjects]": discipline,
        "page[size]": 100  # Increase the page size to retrieve more preprints per request
    }

    start_time = time.time()

    next_url = osf_url
    with tqdm(desc="Retrieving preprints", unit="preprint") as pbar:
        while next_url:
            response = requests.get(next_url, params=osf_params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for preprint in data["data"]:
                    abstract = normalize_text(preprint["attributes"]["description"])
                    if not is_english(abstract):
                        continue

                    disciplines = [discipline]  # Add the current discipline to the list
                    if "attributes" in preprint and "subjects" in preprint["attributes"]:
                        for subject in preprint["attributes"]["subjects"]:
                            if isinstance(subject, dict) and "text" in subject:
                                disciplines.append(normalize_text(subject["text"]))
                            elif isinstance(subject, str):
                                disciplines.append(normalize_text(subject))

                    tags = []
                    if "attributes" in preprint and "tags" in preprint["attributes"]:
                        tags = [normalize_text(tag) for tag in preprint["attributes"]["tags"]]

                    split_abstract_text = split_abstract(abstract)

                    preprints.append({
                        "id": preprint["id"],
                        "title": normalize_text(preprint["attributes"]["title"]),
                        "authors": [],  # Placeholder for author information
                        "abstract": split_abstract_text,
                        "date_published": preprint["attributes"]["date_published"],
                        "license": preprint["relationships"]["license"]["data"]["id"] if "license" in preprint["relationships"] and preprint["relationships"]["license"]["data"] else None,
                        "disciplines": disciplines,
                        "tags": tags
                    })
                    pbar.update(1)
                next_url = data["links"].get("next")
            else:
                print(f"Request failed with status code: {response.status_code}")
                break

    end_time = time.time()
    retrieval_time = end_time - start_time
    print(f"Time taken to retrieve preprints: {retrieval_time:.2f} seconds")

    print(f"Total preprints retrieved for {discipline}: {len(preprints)}")

    start_time = time.time()

    # Retrieve author information for each preprint using threading
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_citation, preprint, headers) for preprint in preprints]
        with tqdm(desc="Retrieving citation data", unit="citation", total=len(preprints)) as pbar:
            for future in as_completed(futures):
                preprint = future.result()
                pbar.update(1)

    end_time = time.time()
    citation_time = end_time - start_time
    print(f"Time taken to retrieve citation data: {citation_time:.2f} seconds")

    start_time = time.time()

    # Save the updated data to the JSON file
    with open(filepath, "w") as file:
        json.dump(preprints, file, indent=4)

    end_time = time.time()
    saving_time = end_time - start_time
    print(f"Time taken to save data: {saving_time:.2f} seconds")

    print(f"Saved data to: {filepath}")

    all_preprints.extend(preprints)

# Create a single CSV file for all citations
current_date = datetime.now().strftime("%Y-%m-%d")
csv_filename = f"{current_date}_osf_digest.csv"
csv_filepath = os.path.join(csv_folder, csv_filename)

with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["title", "authors", "abstract", "disciplines"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for preprint in all_preprints:
        writer.writerow({
            "title": preprint["title"],
            "authors": "; ".join(preprint["authors"]),
            "abstract": " ".join(preprint["abstract"]),
            "disciplines": "; ".join(preprint["disciplines"])
        })

print(f"Saved CSV file to: {csv_filepath}")

# Create the output directory if it doesn't exist
output_dir = "output/digests"
os.makedirs(output_dir, exist_ok=True)

# Set up Hugging Face authentication
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN environment variable not set")
os.environ["HF_TOKEN"] = hf_token

# Organize data by discipline
discipline_data = {}
for preprint in all_preprints:
    for discipline in preprint["disciplines"]:
        if discipline not in discipline_data:
            discipline_data[discipline] = []
        discipline_data[discipline].append(" ".join(preprint["abstract"]))

# Load the BART-large-CNN model using the pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")

# Generate summaries for each discipline
discipline_summaries = {}
for discipline, abstracts in discipline_data.items():
    # Generate summaries for each abstract
    abstract_summaries = []
    for preprint in all_preprints:
        if discipline in preprint["disciplines"]:
            abstract = " ".join(preprint["abstract"])
            # Truncate the abstract if needed
            abstract = abstract[:1024]

            summary = summarizer(abstract, max_length=170, min_length=30, do_sample=False)
            abstract_summaries.append(f"Title: {preprint['title']}\nAuthors: {'; '.join(preprint['authors'])}\nSummary: {summary[0]['summary_text']}\n")

    # Combine the abstract summaries into a single summary for the discipline
    discipline_summary = "\n".join(abstract_summaries)
    discipline_summaries[discipline] = discipline_summary

# Save the summaries to a CSV file
csv_filename = f"{current_date}_discipline_summaries.csv"
csv_filepath = os.path.join(output_dir, csv_filename)

with open(csv_filepath, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["Discipline", "Summary"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for discipline, summary in discipline_summaries.items():
        writer.writerow({"Discipline": discipline, "Summary": summary})

print(f"Saved discipline summaries to: {csv_filepath}")