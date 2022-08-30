import os.path
import re
import string
import time
from utils import get_logger
from collections import Counter
from functools import wraps, lru_cache


logger = get_logger(__name__)


def timer(method):
    """time metric for TextAnalyser"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, TextAnalyser):
            raise Exception(f"Timer decorator can't be used with {type(self)}")

        if self._timer_enabled:
            start_time = time.time()
            result = method(self, *args, **kwargs)
            print(f"Time elapsed for {method.__name__}: {round((time.time() - start_time) * 10 ** 6, 2)} microseconds")
        else:
            result = method(self, *args, **kwargs)

        return result

    return wrapper


class TextAnalyser:
    def __init__(self, text: str, enable_timer: bool = False, represent_method: callable = None):
        self._text = text
        self._timer_enabled = enable_timer
        self._represent_method = represent_method
        if self._represent_method is None:
            self._represent_method = print

    @lru_cache(1)
    def _get_chars_count(self) -> int:
        """returns count of characters"""
        return len(self._text)

    @timer
    def number_of_characters(self) -> int:
        """returns number of characters"""
        return self._get_chars_count()

    @timer
    def number_of_words(self) -> int:
        """returns number of words"""
        return len(self._text.split())

    @lru_cache(1)
    def _split_to_sentences(self) -> list[str]:
        """returns list of sentences"""
        return re.split(r'[.!?]+', self._text.replace('...', '.'))

    @timer
    def number_of_sentences(self) -> int:
        """returns number of sentences"""
        return len(self._split_to_sentences())

    @timer
    def frequency_of_characters(self) -> list[tuple[str, int]]:
        """returns frequency of characters"""
        return Counter(self._text).most_common()

    @timer
    def frequency_of_characters_percent(self) -> list[tuple[str, float]]:
        """returns distribution of characters as a percentage of total"""
        counter = Counter(self._text)
        return [(i, counter[i] / self._get_chars_count() * 100.0) for i in counter]

    @lru_cache(1)
    def _get_clear_words(self, only_unique: bool = False) -> list[str]:
        """return list of words in text without punctuation and in lovercas"""
        words = self._text.translate(str.maketrans('', '', string.punctuation)).lower().split()
        return words if not only_unique else list(set(words))

    @timer
    def avg_word_length(self) -> int:
        """returns average length of word in text (rounded to an integer)"""
        words = self._get_clear_words()
        return round(sum(len(w) for w in words) / len(words))

    @timer
    def avg_sentence_length(self) -> int:
        """returns average count of words in sentences (rounded to an integer)"""
        sentences = self._split_to_sentences()
        return round(sum(len(s.split()) for s in sentences) / len(sentences))

    @timer
    def most_used_words(self, n: int = 10) -> list[str]:
        """returns list of n most used words"""
        counter = Counter(self._get_clear_words())
        return [word for word, _ in counter.most_common(n)]

    @lru_cache(1)
    def _sorted_words_by_length(self, reverse: bool = False):
        """return list of sorted words (by default the shortest is first)"""
        return sorted((self._get_clear_words(only_unique=True)), key=lambda x: len(x), reverse=reverse)

    @timer
    def longest_words(self, n: int = 10) -> list[str]:
        """return list of n the longest words"""
        return self._sorted_words_by_length(reverse=True)[:n]

    @timer
    def shortest_words(self, n: int = 10) -> list[str]:
        """return list of n the shortest words"""
        return self._sorted_words_by_length()[:n]

    @lru_cache(1)
    def _sorted_sentences_by_length(self, reverse: bool = False) -> list[str]:
        """return list of sorted sentences by words count (by default the shortest is first)"""
        return sorted(
            (s.strip() for s in self._split_to_sentences() if s),
            key=lambda x: len(x.strip().split()),
            reverse=reverse
        )

    @timer
    def longest_sentences(self, n: int = 10) -> list[str]:
        """return list of n the longest sentences (by words)"""
        return self._sorted_sentences_by_length(reverse=True)[:n]

    @timer
    def shortest_sentences(self, n: int = 10) -> list[str]:
        """return list of n the shortest sentences (by words)"""
        return self._sorted_sentences_by_length()[:n]

    @lru_cache(1)
    def _get_palindromes(self):
        """returns list of palindromes"""
        return [word for word in self._get_clear_words(only_unique=True) if word == word[::-1]]

    @timer
    def number_of_palindromes(self) -> int:
        """return number of palindromes in text"""
        return len(self._get_palindromes())

    @timer
    def longest_palindromes(self, n: int = 10) -> list[str]:
        """return n longest palindromes"""
        return sorted(self._get_palindromes(), key=lambda x: len(x), reverse=True)[:n]

    @timer
    def is_text_palindrome(self) -> bool:
        """Check if whole text is palindrome (Without whitespaces and punctuation marks.)"""
        return (clear_text := self._text.translate(str.maketrans('', '', f"{string.punctuation} "))) == clear_text[::-1]

    @timer
    def reversed_text(self) -> str:
        """returns reversed text"""
        return self._text[::-1]

    @timer
    def text_reversed_words(self) -> str:
        """returns reversed text by words (words not reversed, joust order of words)"""
        return ' '.join(self._text.split()[::-1])

    @timer
    def run_full_analysis(self, represent_results: bool = False):
        """
        return results of full analysis of text
        if represent_results is False, results will be just returned as dict
        if represent_results is True, results will be also represented
        """
        if timer_was_enabled := self._timer_enabled:
            self.disable_timer()

        results = {
            "Number of characters": self.number_of_characters(),
            "Number of words": self.number_of_words(),
            "Number of sentences": self.number_of_sentences(),
            "Frequency of characters": self.frequency_of_characters(),
            "Distribution of characters as a percentage of total": self.frequency_of_characters_percent(),
            "Average word length": self.avg_word_length(),
            "The average number of words in a sentence": self.avg_sentence_length(),
            "Top 10 most used words": self.most_used_words(),
            "Top 10 longest words": self.longest_words(),
            "Top 10 shortest words": self.shortest_words(),
            "Top 10 longest sentences": self.longest_sentences(),
            "Top 10 shortest sentences": self.shortest_sentences(),
            "Number of palindrome words": self.number_of_palindromes(),
            "Top 10 longest palindrome words": self.longest_palindromes(),
            "Is text palindrome": self.is_text_palindrome(),
            "Reversed text": self.reversed_text(),
            "Reversed text by word": self.text_reversed_words(),
        }

        if timer_was_enabled:
            self._timer_enabled = True

        if represent_results is True:
            self._represent_result(results)

        return results

    def _represent_result(self, results: dict):
        for k, v in results.items():
            self._represent_method(f'{k}: {v}\n')

    def enable_timer(self):
        self._timer_enabled = True

    def disable_timer(self):
        self._timer_enabled = False
