import pytest

from text_analyser import TextAnalyser


@pytest.fixture(scope="function")
def text_analyser():
    return TextAnalyser("Super: test, text. OMG! WoW;")
