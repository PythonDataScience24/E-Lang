from transformers import pipeline, set_seed
import random
import re  # To help with filtering complex sentences

# Initialize the generators
set_seed(42)  # For reproducibility
text_generator = pipeline('text-generation', model='gpt2')
translator = pipeline('translation_en_to_de', model='Helsinki-NLP/opus-mt-en-de')


def create_gap_sentence(translation):
    words = translation.split()
    gap_index = random.randint(0, len(words) - 1)
    correct_word = words[gap_index]
    words[gap_index] = '_____'
    return ' '.join(words), correct_word


def generate_english_sentence():
    while True:
        generated_text = text_generator("This is", max_length=20, num_return_sequences=1)[0]['generated_text'].strip()
        # Post-processing to ensure the sentence is simple and short
        sentences = re.split(r'[.?!]', generated_text)  # Split by sentence terminators
        for sentence in sentences:
            words = sentence.strip().split()
            if 2 <= len(words) <= 10:  # Ensures the sentence is not too long or too short
                return ' '.join(words)
        # If no suitable sentence is found, it will continue generating


def main():
    while True:
        english_sentence = generate_english_sentence()
        print(f"Generated English sentence: {english_sentence}")

        translation = translator(english_sentence)[0]['translation_text']
        gap_sentence, correct_word = create_gap_sentence(translation)

        print("Complete the sentence by filling in the gap:")
        print(gap_sentence)
        user_input = input("Your word: ")

        if user_input.lower() == correct_word.lower():
            print("Correct!")
        else:
            print(f"Incorrect! The correct word was: {correct_word}")

        if input("Try another one? (yes/no): ").lower() != 'yes':
            break


if __name__ == "__main__":
    main()
