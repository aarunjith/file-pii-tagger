from loguru import logger
from easyocr import Reader
from pii import PII
import matplotlib.image as mpimg
from pdf2image import convert_from_path
import numpy as np

ocr = Reader(lang_list=['en'])
scanner = PII(fields=['email', 'date of birth', 'account number'])
MAX_PAGES_PDF = 5


def get_extension(filepath):
    return filepath.split(".")[-1].lower()


def process_file(file, d):
    if get_extension(file) == 'txt':
        text_file = open(file, 'r')
        text = text_file.read()
        text_file.close()
        d[file] = scanner.find_fields(text)
        logger.info(scanner.find_fields(text))

    elif get_extension(file) == 'pdf':
        # Add code for PDF parsing
        pdf_texts = []
        logger.info("Trying OCR")
        pages = [np.array(im)
                 for im in convert_from_path(file)[:MAX_PAGES_PDF]]
        logger.info(
            f'Transcribing {len(pages)} pages of the pdf {file}')
        for page in pages:
            if page.max() == 1:
                # Converting to unit8 image for easyOCR
                page = (page * 255).astype('uint8')
            else:
                page = page.astype('uint8')
            output = ocr.readtext(page)
            text = ' '.join([out[1] for out in output])
            pdf_texts.append(text)
        logger.info(f'PDF {file} Transcription Complete')
        d[file] = scanner.find_fields(text)
        logger.info(scanner.find_fields(pdf_texts))

    else:
        image = mpimg.imread(file)
        if image.max() == 1:
            # Converting to unit8 image for easyOCR
            image = (image * 255).astype('uint8')
        else:
            image = image.astype('uint8')
        output = ocr.readtext(image)
        text = ' '.join([out[1] for out in output])
        d[file] = scanner.find_fields(text)
        logger.info(scanner.find_fields(text))
