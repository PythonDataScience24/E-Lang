import requests
import random
import copy
import string
# import re  # To help with filtering complex sentences

# Initialize the RNG (for consistency)
random.seed(42)
target_lang: str = 'deu'
source_lang: str = 'eng'
request_url: str = "https://tatoeba.org/eng/api_v0/search"


def remove_punctuation(word: str) -> str:
    for punc_char in string.punctuation:
        word = word.replace(punc_char, '')
    return word


def create_gap_sentence(translation: str):
    words = translation.split()
    gap_index = random.randint(0, len(words) - 1)
    correct_word = words[gap_index]
    words[gap_index] = '_____'
    return ' '.join(words), correct_word


def generate_sentences():
    url: str = copy.copy(request_url)
    url += "?from="+target_lang
    url += "&to="+source_lang
    url += "&sort=random"
    seed: int = random.randint(0, 30000)
    url += "&rand_seed="+str(seed)  # so we get different sentences every time
    url += "&orphan=no"
    url += "&unapproved=no"  # site says those are "likely to be incorrect"
    url += "&word_count_max=15"
    url += "&word_count_min=3"
    req = requests.get(url)
    req_parsed = req.json()
    first_sentence = req_parsed['results'][0]
    target_text = first_sentence['text']
    translation_categories = first_sentence['translations']
    # print(first_sentence)
    for category in translation_categories:
        if len(category) != 0:
            for translation in category:
                if len(translation) != 0:
                    source_text = translation['text']
    return target_text, source_text


def main():
    while True:
        german_sentence, english_sentence = generate_sentences()
        print(f"Generated English sentence: {english_sentence}")

        gap_sentence, correct_word = create_gap_sentence(german_sentence)

        print("Complete the sentence by filling in the gap:")
        print(gap_sentence)
        user_input = input("Your word: ")

        if remove_punctuation(user_input.lower()) == remove_punctuation(
                correct_word.lower()):
            print("Correct!")
        else:
            print(f"Incorrect! The correct word was: {correct_word}")

        if input("Try another one? (yes/no): ").lower() != 'yes':
            break


if __name__ == "__main__":
    main()