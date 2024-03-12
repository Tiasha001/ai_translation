from functools import partial
from multiprocessing.pool import Pool, ThreadPool

from time import time

from concurrent.futures import ThreadPoolExecutor
import os

from utility import (
    TranslationServiceProvider,
    FileDataExtractor,
    Tokenize,
)
from config.file_config import (
    BASE_FOLDER_PATH,
    SAMPLE_INPUT_DOC_FILE_PATH,
    SAMPLE_INPUT_PDF_FILE_PATH,
    OUTPUT_FOLDER_PATH,
)
from config.openai_config import OPENAI_INPUT_TOKEN_LENGTH
from config.message_config import InputMessages, DefaultLanguages


def collect_file(file_type):
    """
    Collects file path based on file type.

    Args:
    - file_type (str): Type of the file.

    Returns:
    str: File path.
    """
    if "pdf" == file_type:
        return SAMPLE_INPUT_PDF_FILE_PATH
    else:
        return SAMPLE_INPUT_DOC_FILE_PATH



def store_output_to_file(process, output):
    """
    Stores output to a file.

    Args:
    - process (str): Name of the process.
    - output (list): List of output items.
    """
    output_file_name = f"output_{process}_chunk_{OPENAI_INPUT_TOKEN_LENGTH}.txt"
    output_file_path = os.path.join(OUTPUT_FOLDER_PATH, output_file_name)
    with open(output_file_path, "w", encoding="utf-16") as file:
        for item in output:
            file.write("{}\n".format(item))


def execute(process, file_type, file_path, src, dest):
    """
    Executes translation process.

    Args:
    - process (str): Name of the translation process.
    - file_type (str): Type of the file.
    - file_path (str): Path of the file.
    - src (str): Source language.
    - dest (str): Destination language.

    Returns:
    tuple: Boolean indicating success or failure, and output data.
    """
    result = []
    status, content = FileDataExtractor(
        file_path=file_path, file_type=file_type
    ).get_file_data()
    if not status:
        return status, content

    ts = time()
    translate = TranslationServiceProvider(
        service_name=process, src_language=src, target_language=dest
    )
    service_verify, msg = translate.verify_service_name()
    if not service_verify:
        return service_verify, msg

    with ThreadPoolExecutor(5) as executor:
        # func = partial(translate.get_translated_data, process)
        result = executor.map(
            translate.get_translated_data, Tokenize(content).sent_max_token()
        )

    print("Took %s seconds to translate", time() - ts)

    output = list(result)
    return True, output


def main():
    """
    Main function to execute the translation process.
    """
    ts = time()
    process = input(InputMessages.ENTER_TRANSLATOR.value)
    file_type = input(InputMessages.ENTER_FILE_TYPE.value)
    src, dest = (
        DefaultLanguages.DEFAULT_SOURCE_LANGUAGE.value,
        DefaultLanguages.DEFAULT_TARGET_LANGUAGE.value,
    )

    file_path = collect_file(file_type)
    status, output = execute(process, file_type, file_path, src, dest)
    if not status:
        print(output)
        return

    store_output_to_file(process, output)
    print("Took %s seconds", time() - ts)


if __name__ == "__main__":
    main()
