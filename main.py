from timeit import time
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from natsort import natsorted
import glob, os, shutil
from pathlib import Path

BASE_PATH = os.getcwd()
path_main_pdf = os.path.join(BASE_PATH, 'pdf_original/Django 2.1.pdf')
input_PDF = PdfFileReader(open(path_main_pdf, 'rb'))


def clean_after_work():
    files = glob.glob(f'{BASE_PATH}/merge/*.pdf')
    for f in files:
        try:
            time.sleep(0.02)
            os.remove(f)
        except OSError as e:
            print("Ошибка: %s : %s" % (f, e.strerror))
    print('Очистка папки выполнена!')


def split_pdf_pages(*args):
    clean_after_work()
    a, b = args
    for i in range(a, b+1):
        output = PdfFileWriter()
        new_File_PDF = input_PDF.getPage(i-1)
        output.addPage(new_File_PDF)
        output_Name_File = BASE_PATH + "/merge/SomePDF" + str(i + 1) + ".pdf"
        outputStream = open(output_Name_File, 'wb')
        output.write(outputStream)
        outputStream.close()
    merge_pdf(*args)


def merge_pdf(*args):
    # Получаем список полных путей к указанным страницам в папке merge
    pdf_glob = glob.glob(BASE_PATH + '/merge/*.pdf')

    # Создаем путь к файлу типа (600, 673).pdf
    new_merge_pdf = Path('merge/'f"{args}"'.pdf')

    # Создаем экземпляр класса
    merge_pdfs = PdfFileMerger()

    for i in natsorted(pdf_glob):
        # Каждый файл открываем, читаем и добавляем в сортированном порядке
        merge_pdfs.append(i)


    # Записываем в новый файл список merge_pdfs
    merge_pdfs.write(open(new_merge_pdf, 'wb'))
    merge_pdfs.close()


    print(f'Файл {args} создан!')
    shutil.move(f'{BASE_PATH}/merge/{args}.pdf', f'{BASE_PATH}/create/{args}.pdf')



split_pdf_pages(66, 99)
time.sleep(5)
split_pdf_pages(301, 400)
time.sleep(5)
split_pdf_pages(501, 600)

