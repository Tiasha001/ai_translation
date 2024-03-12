import os
from abc import ABC, abstractmethod
import docx2txt
from PyPDF2 import PdfReader


class ProcessFiles(ABC):
    """
    Abstract Factory Interface for processing files.
    """

    def __init__(self, file) -> None:
        self.file = file
        
    
    @abstractmethod
    def extract_data(self):
        """
        Abstract method to extract data from the file.
        """
        pass


class PdfProcessor(ProcessFiles):
    """
    Subclass of ProcessFiles for processing PDF files.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the PdfProcessor object.

        Args:
        - file: file path in str
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def extract_data(self):
        """
        Extracts data from the PDF file.

        Returns:
        PdfReader: PDF reader object.
        """
        file = self.file
        reader = PdfReader(file)
        return reader
    
    def separate_data_per_page(self):
        """
        Separates data per page from the PDF file.

        Returns:
        list: List of strings, each containing data from one page.
        """
        file_data = self.extract_data()
        # read page-wise data 
        page_content = [x.extract_text().replace("\n", " ") for x in file_data.pages]
        return page_content
    
    
    def get_data_in_single_string(self):
        """
        Retrieves all data from the PDF file as a single string.

        Returns:
        str: All data from the PDF file in a single string.
        """
        file_data = self.extract_data()
        # read all the data in a single string 
        content = ",\n".join([x.extract_text().replace("\n", " ") for x in file_data.pages])
        return content
    
    
    def separate_data_per_line(self):
        """
        Separates data per line from the PDF file.

        Returns:
        list: List of strings, each containing data from one line.
        """
        file_data = self.extract_data()
        # read line-wise data 
        content = [x.extract_text().strip().split("\n") for x in file_data.pages]
        result = [j for sub in content for j in sub]
        return result

    
class DocProcessor(ProcessFiles):
    """
    Subclass of ProcessFiles for processing DOCX files.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initializes the PdfProcessor object.

        Args:
        - file: file path in str
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
    
    
    def extract_data(self):
        """
        Extracts data from the DOCX file.

        Returns:
        list: List of strings, each containing a line of text from the DOCX file.
        """
        text = docx2txt.process(self.file)
        # return text
        lines = text.split('\n')
        return lines
    