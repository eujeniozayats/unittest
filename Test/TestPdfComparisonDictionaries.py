import unittest
from Data.ExtractPdfInformation import ExtractPdfInformation


class TestPdfExtraction(unittest.TestCase):

    def test_compare_dictionaries(self):
        pdf_file_path_first = '../Data/File/test_task.pdf'
        pdf_file_path_second = '../Data/File/test_task.pdf'

        extractor = ExtractPdfInformation()

        dictionary_first = extractor.extract_pdf_information(pdf_file_path_first)
        dictionary_second = extractor.extract_pdf_information(pdf_file_path_second)

        # Выводим словари в консоль
        print("First PDF Dictionary:")
        print(dictionary_first)

        print("Second PDF Dictionary:")
        print(dictionary_second)

        self.assertDictEqual(dictionary_first, dictionary_second)