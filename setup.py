from setuptools import setup, find_packages

setup(
    name="osf_digest",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "osf_digest = cli.cli:main"
        ]
    },
    install_requires=[
        "requests",
        "tqdm",
        "unidecode",
        "langdetect",
        "transformers",
        "torch",
        "python-dotenv"
    ],
    author="Aamir Sohail",
    author_email="axs2210@student.bham.ac.uk",
    description="A command-line tool to retrieve and summarize preprints from OSF",
    license="MIT",
    keywords="osf preprints summarization",
    url="https://github.com/sohaamir/osf_digest"
)