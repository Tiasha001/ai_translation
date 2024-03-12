'''enum config classes'''
from enum import Enum

class ExtendedEnum(Enum):
    @classmethod
    def get_list(cls):
        return list(map(lambda c: c.value, cls))

class TranlatorTypes(ExtendedEnum):
    OPENAI = "openai"
    GOOGLE = "google"
    
class FileTypes(ExtendedEnum):
    PDF = "pdf"
    DOC = "doc"
    DOCX = "docx"
    
class DefaultLanguages(Enum):
    DEFAULT_SOURCE_LANGUAGE = "English"
    DEFAULT_TARGET_LANGUAGE = "Hindi"
    
class InputMessages(Enum):
    ENTER_TRANSLATOR = f"Enter the translator type - {TranlatorTypes.get_list()} : "
    ENTER_FILE_TYPE = f"Enter the file type - {FileTypes.get_list()} : "
    ENTER_SOURCE_AND_TARGET_LANGUAGE = "Enter source and target language(separated by comma): "
    
class InvalidInputMessages(Enum):
    INVALID_FILE_TYPE = f"INVALID FILE TYPE PROVIDED. PLEASE SELECT ANYTHING AMONG THESE : {FileTypes.get_list()}"
    INVALID_SERVICE_TYPE = f"INVALID SERVICE TYPE PROVIDED. PLEASE SELECT ANYTHING AMONG THESE : {TranlatorTypes.get_list()}"