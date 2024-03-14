import tiktoken 
import os
from config.openai_config import OPENAI_MODEL, OPENAI_INPUT_TOKEN_LENGTH

from file_processor import PdfProcessor, DocProcessor
from translation import OpenAITranslate, GoogleTranslate, GoogleCloudtranslate
from config.message_config import (
    InvalidInputMessages, FileTypes, TranlatorTypes,
    DefaultLanguages
)

class Tokenize:
    """
    Tokenizes text data.

    Attributes:
    - __token (str): Token for encoding.
    - __token_length (int): Length of the token.
    - __file_data (list): List of text data.
    - __file_length (int): Length of the text data list.
    """
    def __init__(self, file_data) -> None:
        """
        Initializes the Tokenize object.

        Args:
        - file_data (list): List of text data.
        """
        self.__token = tiktoken.encoding_for_model(OPENAI_MODEL)
        self.__token_length = OPENAI_INPUT_TOKEN_LENGTH
        self.__file_data = file_data
        self.__file_length = len(file_data) 
        print(self.__file_length)
    
    def sent_max_token(self):
        """
        Iterates through the text data and yields sentences with maximum token length.

        Yields:
        list: List containing sentences with maximum token length.
        """
        count = 0
        start = 0
        for i in range(self.__file_length):
            l= len(self.__token.encode(self.__file_data[i]))
            
            # 1. if the one element contents words of more than or equals to the chunk size then 
            # then particular element should be returned.
            # 2. if it reaches to file length then also same is applicable.
            if (l >= self.__token_length)  or (i==self.__file_length-1):
                print(start, i+1)
                yield [", ".join(self.__file_data[start:i+1])]
                start = i+1
                l = 0
                count = 0
                
            count+=l
            if count>self.__token_length:
                print(start, i)
                yield [", ".join(self.__file_data[start:i])]
                start = i 
                count = 0 
            

                                
class FileDataExtractor():
    """
    Extracts data from different file types.

    Attributes:
    - file_path (str): File path.
    - file_type (str): File type.
    """
    
    def __init__(self, file_path, file_type) -> None:
        """
        Initializes the FileDataExtractor object.

        Args:
        - file_path (str): File path.
        - file_type (str): File type.
        """
        self.file_path = file_path
        self.file_type = file_type
        
        
    def get_file_data(self):
        """
        Retrieves data from the file.

        Returns:
        tuple: Boolean indicating success or failure, and extracted file data.
        """
        
        if self.file_type not in ["pdf", "doc", "docx"]:
            return False, InvalidInputMessages.INVALID_FILE_TYPE.value
        
        
        if "pdf" in self.file_type:
            page_content = PdfProcessor(self.file_path).separate_data_per_line()
        else:
            page_content = DocProcessor(self.file_path).extract_data()
            
        return True, page_content
        
      
      
class TranslationServiceProvider():
    """
    Provides translation services.

    Attributes:
    - __processor_mapping (dict): Mapping of service names to processor classes.
    - src_language (str): Source language.
    - target_language (str): Target language.
    - service_name (str): Service name.
    """
    def __init__(self, service_name,
                 src_language=DefaultLanguages.DEFAULT_SOURCE_LANGUAGE.value, 
                 target_language=DefaultLanguages.DEFAULT_TARGET_LANGUAGE.value
                ) -> None:
        """
        Initializes the TranslationServiceProvider object.

        Args:
        - service_name (str): Service name.
        - src_language (str): Source language.
        - target_language (str): Target language.
        """
        
        self.__processor_mapping = {
            "openai":OpenAITranslate,
            "google":GoogleCloudtranslate
        }
        self.src_language=src_language
        self.target_language=target_language
        self.service_name=service_name
        
    def verify_service_name(self):   
        """
        Verifies the service name.

        Returns:
        tuple: Boolean indicating success or failure, and error message if any.
        """
        if self.service_name not in TranlatorTypes.get_list():
            return False, InvalidInputMessages.INVALID_SERVICE_TYPE.value
        return True, None
      
      
    def format_input_text(self, input_text):   
        """
        Formats the input text.

        Args:
        - input_text: Input text.

        Returns:
        tuple: Boolean indicating success or failure, and formatted input text.
        """
        if isinstance(input_text,list) and len(input_text)==1:
            input_text=input_text[0]
            return True, input_text
        
        elif isinstance(input_text, str):
            return True, input_text
        
        else: 
            print(type(input_text), len(input_text))
            print("\n\ninvalid text\n\n")
            return False, ''
        
        
    def get_translated_data(self, input_text):
        """
        Retrieves translated data.

        Args:
        - input_text: Input text.

        Returns:
        str: Translated text.
        """
        _status, input_text = self.format_input_text(input_text)
        if _status:
            service_class = self.__processor_mapping[self.service_name](
                src_language=self.src_language, target_language=self.target_language, 
                input_text=input_text
            )
            tranlated_text = service_class.translate()
            
            return tranlated_text
        
        
    