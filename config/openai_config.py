'''
config file to store openai credentials
'''

FIRST_PROMPT_INSTRUCTION = '''Translate the following {src_lang} text to {desc_lang}. Translation should flow well, have high readability, 
                            should be medium complex. Each and every word should be translated. each sentence should be completed. 
                            Translate each question and all of their options. Ordering should be properly maintained. 
                            Serial no of the questions should be correct and properly displayed. Don't give the answer or skip any question. 
                            Only translate as instructed.
                            '''
        
VALIDATE_TRANSLATION_INSTRUCTION = "correct the translation text in {desc_lang} to make the flow better and more consistent with theme of questions and options"


MAXIMUM_RETRY_VALUE = 5

OPENAI_MODEL = "gpt-3.5-turbo"

OPENAI_INPUT_TOKEN_LENGTH = 500