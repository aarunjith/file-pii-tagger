from typer import Typer
from loguru import logger
from tqdm import tqdm
import os
from utils import process_file
from multiprocessing import Process, Manager


cpus = os.cpu_count()
logger.info(f'Found {cpus} Cores to parellise')

cli = Typer()


@cli.command()
def tag_folder(folder=None, extentions=['png', 'jpg', 'jpeg', 'pdf', 'txt'], parallel=False):
    if os.path.isdir(folder):
        files = [f'{folder}/{fn}' for fn in os.listdir(folder)
                 if any(fn.endswith(ext) for ext in extentions)]
        logger.info(f'Found {len(files)} valid files')

    else:
        logger.info(f'Path {folder} is not a valid directory')

    if parallel:
        logger.info(f"Multiprocessing")
        with Manager() as manager:
            d = manager.dict()
            ps = [Process(target=process_file, args=(file, d),
                          ) for file in files]
            for p in ps:
                p.start()
            for p in ps:
                p.join()

    else:
        d = {}
        for file in files:
            process_file(file, d)
        logger.info(d)


if __name__ == "__main__":
    cli()
