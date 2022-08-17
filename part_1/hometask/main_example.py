from text_analyser import TextAnalyser
import os


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "sample_text.txt")) as file:
        analyser = TextAnalyser(file.read())

    results = {
        "Number of characters": analyser.number_of_characters(),
        "Number of words": analyser.number_of_words(),
        "Number of sentences": analyser.number_of_sentences(),
        "Frequency of characters": analyser.frequency_of_characters(),
        "Distribution of characters as a percentage of total": analyser.frequency_of_characters_percent(),
        "Average word length": analyser.avg_word_length(),
        "The average number of words in a sentence": analyser.avg_sentence_length(),
        "Top 10 most used words": analyser.most_used_words(),
        "Top 10 longest words": analyser.longest_words(),
        "Top 10 shortest words": analyser.shortest_words(),
        "Top 10 longest sentences": analyser.longest_sentences(),
        "Top 10 shortest sentences": analyser.shortest_sentences(),
        "Number of palindrome words": analyser.number_of_palindromes()
    }

    for k, v in results.items():
        print(f'{k}: {v}')
