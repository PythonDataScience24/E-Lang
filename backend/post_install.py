import subprocess
import sys

def download_spacy_model():
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "de_core_news_sm"])

if __name__ == "__main__":
    download_spacy_model()
