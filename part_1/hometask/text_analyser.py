import re
import string

from collections import Counter
from itertools import islice
from typing import Iterable


class TextAnalyser:
    def __init__(self, text: str):
        self._text = text

    def number_of_characters(self) -> int:
        """returns number of characters"""
        return len(self._text)

    def number_of_words(self) -> int:
        """returns number of words"""
        return len(self._text.split())

    def _split_to_sentences(self) -> list[str]:
        return re.split(r'[.!?]+', self._text.replace('...', '.'))

    def number_of_sentences(self) -> int:
        """returns number of sentences"""
        return len(self._split_to_sentences())

    def frequency_of_characters(self) -> list[tuple[str, int]]:
        """returns frequency of characters"""
        return Counter(self._text).most_common()

    def frequency_of_characters_percent(self) -> list[tuple[str, float]]:
        """returns distribution of characters as a percentage of total"""
        counter = Counter(self._text)
        return [(i, counter[i] / self.number_of_characters() * 100.0) for i in counter]

    def _get_clear_words(self, only_unique: bool = False) -> list[str]:
        words = self._text.translate(str.maketrans('', '', string.punctuation)).lower().split()
        return words if not only_unique else list(set(words))

    def avg_word_length(self) -> int:
        """returns average length of word in text (rounded to an integer)"""
        words = self._get_clear_words()
        return round(sum(len(w) for w in words) / len(words))

    def avg_sentence_length(self) -> int:
        """returns average count of words in sentences (rounded to an integer)"""
        sentences = self._split_to_sentences()
        return round(sum(len(s.split()) for s in sentences) / len(sentences))

    def most_used_words(self, n: int = 10) -> list[str]:
        """returns list of n most used words"""
        counter = Counter(self._get_clear_words())
        return [word for word, _ in counter.most_common(n)]

    def _sorted_words_by_length(self, reverse: bool = False):
        """return list of sorted words (by default the shortest is first)"""
        return sorted((self._get_clear_words(only_unique=True)), key=lambda x: len(x), reverse=reverse)

    def longest_words(self, n: int = 10) -> list[str]:
        """return list of n the longest words"""
        return self._sorted_words_by_length(reverse=True)[:n]

    def shortest_words(self, n: int = 10) -> list[str]:
        """return list of n the shortest words"""
        return self._sorted_words_by_length()[:n]

    def _sorted_sentences_by_length(self, reverse: bool = False) -> list[str]:
        """return list of sorted sentences by words count (by default the shortest is first)"""
        return sorted(
            (s.strip() for s in self._split_to_sentences() if s),
            key=lambda x: len(x.strip().split()),
            reverse=reverse
        )

    def longest_sentences(self, n: int = 10) -> list[str]:
        """return list of n the longest sentences (by words)"""
        return self._sorted_sentences_by_length(reverse=True)[:n]

    def shortest_sentences(self, n: int = 10) -> list[str]:
        """return list of n the shortest sentences (by words)"""
        return self._sorted_sentences_by_length()[:n]

    def _get_palindromes(self):
        """returns list of palindromes"""
        return [word for word in self._get_clear_words(only_unique=True) if word == word[::-1]]

    def number_of_palindromes(self) -> int:
        """return number of palindromes in text"""
        return len(self._get_palindromes())
