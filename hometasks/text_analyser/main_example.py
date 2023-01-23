from text_analyser import TextAnalyser
import os


if __name__ == "__main__":
    with open(
            os.path.join(os.path.dirname(__file__), "sample_text.txt")
    ) as file:
        analyser = TextAnalyser(file.read())

    analyser.enable_timer()
    analyser.print_full_analysis()
