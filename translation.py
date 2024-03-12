import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

from openai import OpenAI, RateLimitError, AsyncOpenAI
from googletrans import Translator
from tenacity import retry, retry_if_exception_type, wait_fixed

from config.openai_config import (
    FIRST_PROMPT_INSTRUCTION, 
    VALIDATE_TRANSLATION_INSTRUCTION, 
    MAXIMUM_RETRY_VALUE,
    OPENAI_MODEL,
)

load_dotenv()

class Translation(ABC):
    """Abstract Factory Interface"""

    def __init__(self, src_language, target_language, input_text) -> None:
        """
        Initializes the Translation object.

        Args:
        - src_language (str): Source language code.
        - target_language (str): Target language code.
        - input_text (str): Text to be translated.
        """
        self.__src_language = src_language
        self.__target_language = target_language
        self.__input_text = input_text
        
    @abstractmethod
    def translate(self):
        """
        Abstract method to perform translation.

        This method should be implemented by subclasses.
        """
        pass


    
class OpenAITranslate(Translation):
    """Subclass of Translation for translation using OpenAI.
    * Attributes:
        - __openai_key (str): OpenAI API key.
        - __client (OpenAI): OpenAI client object.
        - first_instruction (str): First prompt instruction for translation.
        - revalidate_instruction (str): Revalidation instruction for translation.
            
    * parent Attribute - 
        - src_language (str): Source language code.
        - target_language (str): Target language code.
        - input_text (str): Text to be translated.
    """
    
    
    def __init__(self, *args, **kwargs):
        """
           initialize variables. 
        """
        super().__init__(*args, **kwargs)
        
        self.__openai_key = os.environ.get("OPENAI_API_KEY")
        self.__client =OpenAI(api_key=self.__openai_key, max_retries=MAXIMUM_RETRY_VALUE)
        
        self.first_instruction = FIRST_PROMPT_INSTRUCTION.format(
                                    src_lang=self._Translation__src_language,
                                    desc_lang=self._Translation__target_language
                                )
        self.revalidate_instruction = VALIDATE_TRANSLATION_INSTRUCTION.format(
                                    desc_lang=self._Translation__target_language
                                )

    @retry(retry=retry_if_exception_type(RateLimitError), wait=wait_fixed(5))
    def first_conversion(self):
        """
        Perform the first conversion for translation.

        Returns:
        str: Translated text from the first conversion.
        """
        
        response = self.__client.chat.completions.create(
        model=OPENAI_MODEL,
        
        messages=[
            {
            "role": "system",
            "content": self.first_instruction
            },
            {
            "role": "user",
            "content": self._Translation__input_text
            }
        ],
        )
        print("finish reason:",response.choices[0].finish_reason, ", token info:", response.usage)
        return response.choices[0].message.content
    
    
    @retry(retry=retry_if_exception_type(RateLimitError), wait=wait_fixed(5))
    def revalidate_conversion(self, first_translation_result):
        """
        Perform the revalidation conversion for translation.

        Args:
        first_translation_result (str): Result from the first conversion.

        Returns:
        str: Revalidated translated text.
        """
        response = self.__client.chat.completions.create(
        model=OPENAI_MODEL,
        
        messages=[
            {
            "role": "system",
            "content": self.revalidate_instruction
            },
            {
            "role": "user",
            "content": first_translation_result
            }
        ],
        )
        return response.choices[0].message.content
    
    
    def translate(self):
        """
        Perform the translation.

        Returns:
        str: Translated text.
        """
        return self.revalidate_conversion(self.first_conversion())



class GoogleTranslate(Translation):
    """Subclass of Translation for translation using OpenAI.
    * Attributes:
        - __g_translator (OpenAI): google client object.
                
    * parent Attribute - 
        - src_language (str): Source language code.
        - target_language (str): Target language code.
        - input_text (str): Text to be translated."""
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__g_translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
            ])
        
        
    def translate(self): 
        """
        Perform the translation using Google Translate API.

        Returns:
        str: Translated text.
        """
        try:
            text_to_translate = self.__g_translator.translate(self._Translation__input_text, 
                                                        src= self._Translation__src_language,
                                                        dest= self._Translation__target_language
                                                        )
                
            # Storing the translated text in text variable 
            text = text_to_translate.text
            return text

        
        except Exception as e:
            print(f"Unable to provide Required Output : {e}")
            return None

       