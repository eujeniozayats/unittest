from base64 import decode
import pdfplumber

class ExtractPdfInformation:
    def extract_pdf_information(self, pdf_file_path):
        pdf_information = {}

        try:
            with pdfplumber.open(pdf_file_path) as pdf:

                # Извлечение метаданных PDF файла
                pdf_information['metadata'] = pdf.metadata

                # Извлечение текста и его расположения
                text_with_location = []
                with pdfplumber.open(pdf_file_path) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        text_elements = page.extract_text(x_tolerance=2, y_tolerance=2)
                        for element in text_elements.split('\n'):
                            if element.strip():
                                text_info = {
                                    'page_number': page_number,
                                    'text': element,
                                    'x0': float('inf'),
                                    'y0': float('inf'),
                                    'x1': -1,
                                    'y1': -1
                                }
                                for char in page.chars:
                                    if element in char['text']:
                                        text_info['x0'] = min(text_info['x0'], char['x0'])
                                        text_info['y0'] = min(text_info['y0'], char['top'])
                                        text_info['x1'] = max(text_info['x1'], char['x1'])
                                        text_info['y1'] = max(text_info['y1'], char['bottom'])
                                text_with_location.append(text_info)
                pdf_information['text_with_location'] = text_with_location

                # Извлечение количества страниц в PDF файле
                pdf_information['num_pages'] = len(pdf.pages)

                # Извлечение таблиц из PDF файла
                tables = []
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    tables.extend(page_tables)
                pdf_information['tables'] = tables

                # Извлечение изображений из PDF файла (в виде словарей с информацией о каждом изображении)
                images = []
                for page_number, page in enumerate(pdf.pages, start=1):
                    page_images = page.images
                    for image_index, image in enumerate(page_images):
                        image_info = {
                            'page_number': page_number,
                            'image_index': image_index,
                            'x0': image['x0'],
                            'y0': image['y0'],
                            'x1': image['x1'],
                            'y1': image['y1'],
                            'width': image['width'],
                            'height': image['height']
                        }
                        pdf_information['images'].append(image_info)

                        # Извлечение штрихкодов из изображения
                        barcodes = []
                        with image['stream'] as img_stream:
                            image_binary = img_stream.read()
                            decoded_barcodes = decode(image_binary)
                            barcodes = [barcode.data.decode('utf-8') for barcode in decoded_barcodes]
                            pdf_information['barcodes'].extend(barcodes)
                        pdf_information['barcodes'] = barcodes

                    pdf_information['images'] = images

        except Exception as e:
            pdf_information['error'] = str(e)

        return pdf_information