import os
import sys

import requests
import click
import multiprocessing

from consts import ANALYSE_RESULTS_PATH
from entities import ResourceMeta, ResourcesTypes
from utils import get_execution_logger, get_logger
from datetime import datetime
from text_analyser import TextAnalyser

logger = get_logger(__name__)
execution_logger = get_execution_logger(__name__)


@click.command()
@click.option('--file', '-f', help='Path to file.', type=str, multiple=True)
@click.option('--resource', '-r', help='Url to file.', type=str, multiple=True)
def main(file, resource):
    if not file and not resource:
        logger.error("No any file or resource provided.",
                     extra={"type_of_resource": "No resource", "name_of_resource": "No resource"})
        sys.exit(1)

    execution_date = datetime.now()

    with multiprocessing.Pool(5) as pool:
        for f in file:
            pool.apply_async(process_file, (f, ResourceMeta(type=ResourcesTypes.FILE, name=f, execution_date=execution_date)))

        for r in resource:
            pool.apply_async(process_resource, (r, ResourceMeta(type=ResourcesTypes.FILE, name=f, execution_date=execution_date)))

        pool.close()
        pool.join()

def _metadata_to_extra_logs(metadata: ResourceMeta):
    return {
        "type_of_resource": metadata.type.value,
        "name_of_resource": metadata.name
    }

def process_file(file_path, metadata: ResourceMeta = None):
    """
    process text from a local directory file
    """

    execution_logger.info(f'Start processing text from file [{file_path}]', extra=_metadata_to_extra_logs(metadata))
    if os.path.exists(file_path):
        try:
            with open(file_path) as file:
                run_analysis(
                    file.read(),
                    metadata=metadata)
        except Exception as e:
            execution_logger.error(f'Error when opening the file: {e}', extra=_metadata_to_extra_logs(metadata))
            return
    else:
        execution_logger.error(f"Path [{file_path}] does not exists.", extra=_metadata_to_extra_logs(metadata))


def process_resource(resource, metadata: ResourceMeta = None):
    """
    process text from foreign resource (http/https)
    """
    execution_logger.info(f'Start processing text from resource [{resource}]', extra=_metadata_to_extra_logs(metadata))
    try:
        response = requests.get(resource)
        if response.status_code == 200:
            run_analysis(
                response.text,
                metadata=metadata
            )
        else:
            execution_logger.error(f'Got invalid response from url: [{resource}]', extra=_metadata_to_extra_logs(metadata))
            return
    except Exception as e:
        execution_logger.error(f'Error processing the request: {e}, url: [{resource}]', extra=_metadata_to_extra_logs(metadata))


def run_analysis(text: str, metadata: ResourceMeta = None):
    """
    run analysis and save results into a file
    """

    if not os.path.exists(ANALYSE_RESULTS_PATH):
        os.mkdir(ANALYSE_RESULTS_PATH)

    with open(os.path.join(ANALYSE_RESULTS_PATH, f'analysis_results_{datetime.now().isoformat()}.txt'), 'w') as file:
        if metadata:
            file.write(f"{'*' * 20}\nMetadata:\n")
            for k, v in metadata.__dict__.items():
                file.write(f"\t{k}: {v}\n")
            file.write(f'{"*" * 20}\n')

        analyser = TextAnalyser(text, represent_method=file.write)
        analyser.enable_timer()
        analyser.run_full_analysis(represent_results=True)

    execution_logger.info("Execution finished.", extra=_metadata_to_extra_logs(metadata))


if __name__ == '__main__':
    main()
