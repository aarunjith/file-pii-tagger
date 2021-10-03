from loguru import logger
import re

class PII:
    '''
    PII Identifier

    '''
    def __init__(self, fields=['email', 'date of birth', 'account number']):
        self.pii_fields = fields
        self.email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def find_fields(self, text):
        '''Check the presence of potential PII fields in the input string
            Inputs:
                text : str/List -> String/List of Strings from the document
            Outputs:
                List(boolean) -> Boolean indicating the presence of PII field
        '''
        if isinstance(text, list):
            text = '\n'.join(text).lower()
        else:
            text = text.lower()
        
        result = {}
        for field in self.pii_fields:
            if field in text:
                logger.info(f'Found {field} in the document')
                result[field] = True
            else:
                result[field] = False
                
            if field == 'email':
                if re.search(self.email_regex, text):
                    logger.info('Found valid email addresses in the document')
                    result[field] = True
                else:
                    result[field] = False

        return result