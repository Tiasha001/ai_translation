'''config file to store file info'''
import os 

BASE_FOLDER_PATH = "C:/Users/tiash/OneDrive/Desktop/visionias/ai_project"

INPUT_FOLDER_NAME = "translation_inputs"
INPUT_FOLDER_PATH = os.path.join(BASE_FOLDER_PATH, INPUT_FOLDER_NAME)

SAMPLE_PDF_FILE_NAME = "8407543ffff-gs-pre-mini-test_3152_modern-indian-history-1_e_2021.pdf"
# SAMPLE_PDF_FILE_NAME = "840754bd1f7-gs-pre-mini-test_3232_polity-1_e_2021.pdf"
# SAMPLE_PDF_FILE_NAME = "8407542bff9-1_gs_pre_test_4417_e_2024.pdf"

SAMPLE_DOC_FILE_NAME = "1_CURRENT_AFFAIRS_JANUARY_2023.docx"

SAMPLE_INPUT_PDF_FILE_PATH = os.path.join(INPUT_FOLDER_PATH, SAMPLE_PDF_FILE_NAME)
SAMPLE_INPUT_DOC_FILE_PATH = os.path.join(INPUT_FOLDER_PATH, SAMPLE_DOC_FILE_NAME)


OUTPUT_FOLDER_NAME = "translation_outputs"
OUTPUT_FOLDER_PATH = os.path.join(BASE_FOLDER_PATH, OUTPUT_FOLDER_NAME)
