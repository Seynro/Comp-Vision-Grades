# import module
from pdf2image import convert_from_path


def PDF_JPG_converter(image_path):

    pdf_name = image_path.replace('.jpg', '.pdf')
    
    images = convert_from_path(pdf_name, 300, poppler_path = r"C:\Users\user\Desktop\poppler-23.08.0\Library\bin")
    
    for i in range(len(images)):

	    # Save pages as images in the pdf
	    images[i].save(image_path, 'JPEG')