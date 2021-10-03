from easyocr import Reader
from typer import Typer
from loguru import logger
from utils import get_extension
from pii import PII
import matplotlib.image as mpimg
from pdf2image import convert_from_path
from tqdm import tqdm
import numpy as np
import os


cli = Typer()
ocr = Reader(lang_list = ['en'])
scanner = PII(fields=['email', 'date of birth', 'account number'])
MAX_PAGES_PDF = 5

@cli.command()
def tag_folder(folder=None, extentions=['png', 'jpg', 'jpeg', 'pdf', 'txt']):
    if os.path.isdir(folder):
        files = [f'{folder}/{fn}' for fn in os.listdir(folder)
                if any(fn.endswith(ext) for ext in extentions)]
        logger.info(f'Found {len(files)} valid files')
        for file in tqdm(files):
            logger.info(f'Processing {file}')
            if get_extension(file) == 'txt':
                text_file = open(file, 'r')
                text = text_file.read()
                text_file.close()
                logger.info(scanner.find_fields(text))

            elif get_extension(file) == 'pdf':
                # Add code for PDF parsing
                pdf_texts = []
                logger.info("Trying OCR")
                pages = [np.array(im) for im in convert_from_path(file)[:MAX_PAGES_PDF]]
                logger.info(f'Transcribing {len(pages)} pages of the pdf {file}')
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
                logger.info(scanner.find_fields(text))


            
    else:
        logger.info(f'Path {folder} is not a valid directory')

if __name__ == "__main__":
    cli()