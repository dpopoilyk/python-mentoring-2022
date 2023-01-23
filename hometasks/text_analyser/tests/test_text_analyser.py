from unittest.mock import Mock


def test_number_of_characters(text_analyser):
    chars_count = text_analyser.number_of_characters()
    assert chars_count == 28


def test_number_of_words(text_analyser):
    words_count = text_analyser.number_of_words()
    assert words_count == 5


def test_number_of_sentences(text_analyser):
    sent_count = text_analyser.number_of_sentences()
    assert sent_count == 3


def test_frequency_of_characters(text_analyser):
    freq_chars = text_analyser.frequency_of_characters()
    assert freq_chars == [
        (" ", 4),
        ("t", 4),
        ("e", 3),
        ("W", 2),
        ("S", 1),
        ("u", 1),
        ("p", 1),
        ("r", 1),
        (":", 1),
        ("s", 1),
        (",", 1),
        ("x", 1),
        (".", 1),
        ("O", 1),
        ("M", 1),
        ("G", 1),
        ("!", 1),
        ("o", 1),
        (";", 1),
    ]


def test_frequency_of_characters_percent(text_analyser):
    freq_chars = text_analyser.frequency_of_characters_percent()
    assert freq_chars == [
        ("S", 3.571428571428571),
        ("u", 3.571428571428571),
        ("p", 3.571428571428571),
        ("e", 10.714285714285714),
        ("r", 3.571428571428571),
        (":", 3.571428571428571),
        (" ", 14.285714285714285),
        ("t", 14.285714285714285),
        ("s", 3.571428571428571),
        (",", 3.571428571428571),
        ("x", 3.571428571428571),
        (".", 3.571428571428571),
        ("O", 3.571428571428571),
        ("M", 3.571428571428571),
        ("G", 3.571428571428571),
        ("!", 3.571428571428571),
        ("W", 7.142857142857142),
        ("o", 3.571428571428571),
        (";", 3.571428571428571),
    ]


def test_avg_word_length(text_analyser):
    avg_length = text_analyser.avg_word_length()
    assert avg_length == 4


def test_avg_sentence_length(text_analyser):
    avg_length = text_analyser.avg_sentence_length()
    assert avg_length == 2


def test_most_used_words(text_analyser):
    most_used = text_analyser.most_used_words()
    assert most_used == ["super", "test", "text", "omg", "wow"]


def test_longest_words(text_analyser):
    longest = text_analyser.longest_words()
    assert longest[0] == "super"


def test_shortest_words(text_analyser):
    shortest = text_analyser.shortest_words()
    assert shortest[-1] == "super"


def test_longest_sentences(text_analyser):
    longest = text_analyser.longest_sentences()
    assert longest[0] == "Super: test, text"


def test_shortest_sentences(text_analyser):
    shortest = text_analyser.shortest_sentences()
    assert shortest[0] == "OMG"


def test_number_of_palindromes(text_analyser):
    palindromes_count = text_analyser.number_of_palindromes()
    assert palindromes_count == 1


def test_longest_palindromes(text_analyser):
    longest_palindromes = text_analyser.longest_palindromes()
    assert longest_palindromes == ["wow"]


def test_is_text_palindrome(text_analyser):
    is_pal = text_analyser.is_text_palindrome()
    assert is_pal is False


def test_reversed_text(text_analyser):
    rev = text_analyser.reversed_text()
    assert rev == ";WoW !GMO .txet ,tset :repuS"


def test_reversed_words(text_analyser):
    rev_words = text_analyser.text_reversed_words()
    assert rev_words == "WoW; OMG! text. test, Super:"


def test_run_full_analysis(text_analyser):
    mock = Mock()
    text_analyser.number_of_characters = mock
    text_analyser.number_of_words = mock
    text_analyser.number_of_sentences = mock
    text_analyser.frequency_of_characters = mock
    text_analyser.frequency_of_characters_percent = mock
    text_analyser.avg_word_length = mock
    text_analyser.avg_sentence_length = mock
    text_analyser.most_used_words = mock
    text_analyser.longest_words = mock
    text_analyser.shortest_words = mock
    text_analyser.longest_sentences = mock
    text_analyser.shortest_sentences = mock
    text_analyser.number_of_palindromes = mock
    text_analyser.longest_palindromes = mock
    text_analyser.is_text_palindrome = mock
    text_analyser.reversed_text = mock
    text_analyser.text_reversed_words = mock

    text_analyser.run_full_analysis()

    assert mock.call_count == 17


def test_timer_switching(text_analyser):
    text_analyser.enable_timer()
    assert text_analyser._timer_enabled is True

    text_analyser.disable_timer()
    assert text_analyser._timer_enabled is False
