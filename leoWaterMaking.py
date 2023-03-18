from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from reportlab.pdfgen import canvas

FilesPath = "./UPLOADS/"


class WaterMark:
    def add_watermark(input_file, output_file, text):
        input_file = open('./UPLOADS/'+input_file.replace(' ', '_'), 'rb')

        pdf_reader = PdfFileReader(input_file)

        output_writer = PdfFileWriter()

        for page_num in range(pdf_reader.numPages):

            page = pdf_reader.getPage(page_num)

            packet = BytesIO()
            can = canvas.Canvas(packet)

            can.setFont("Helvetica", 10)

            watermark_text = text

            page_width = page.mediaBox.getWidth()
            page_height = page.mediaBox.getHeight()

            x = (page_width - can.stringWidth(watermark_text)) / 1
            y = (page_height - can.stringWidth(watermark_text)) / 2

            can.rotate(20)
            can.setFillAlpha(0.5)
            can.setFillColorRGB(255, 255, 255)
            can.drawString(x, y, watermark_text)
            can.save()

            packet.seek(0)

            watermark_pdf = PdfFileReader(packet)

            page.mergePage(watermark_pdf.getPage(0))

            output_writer.addPage(page)

        output_path = open('./Downloaded/'+output_file, 'wb')
        output_writer.write(output_path)

        input_file.close()
        output_path.close()
