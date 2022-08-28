import os
import sys
import requests
import click
import multiprocessing
from utils import get_logger
from datetime import datetime
from text_analyser import TextAnalyser

logger = get_logger()


@click.command()
@click.option('--file', '-f', help='Path to file.', type=str, multiple=True)
@click.option('--resource', '-r', help='Url to file.', type=str, multiple=True)
def main(file, resource):
    if not file and not resource:
        logger.error("No any file or resource provided.")
        sys.exit(1)

    with multiprocessing.Pool(5) as pool:
        for f in file:
            pool.apply_async(process_file, (f,))

        for r in resource:
            pool.apply_async(process_resource, (r, ))
        pool.close()
        pool.join()


def process_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path) as file:
                analyser = TextAnalyser(file.read())
        except Exception as e:
            logger.error(f'Error when opening the file: {e}')
            return

        run_analysis(analyser, header=f'Text from path: {file_path}')
    else:
        logger.error(f"Path [{file}] does not exists.")


def process_resource(resource):
    try:
        response = requests.get(resource)
        if response.status_code == 200:
            analyser = TextAnalyser(response.text)
            run_analysis(analyser, header=f'Text from url: {resource}')
        else:
            logger.error(f'Got invalid response from url: [{resource}]')
            return
    except Exception as e:
        logger.error(f'Error processing the request: {e}, url: [{resource}]')


def run_analysis(analyser: TextAnalyser, header: str = None):
    directory = './results'
    if not os.path.exists(directory):
        os.mkdir(directory)
    analyser.enable_timer()
    analyser.analyse_to_file(
        os.path.join(directory, f'analysis_results_{datetime.now().isoformat()}'),
        header=header
    )


if __name__ == '__main__':
    main()
