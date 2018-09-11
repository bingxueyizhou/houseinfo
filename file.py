#!/usr/bin/env python2
import requests
import rarfile
import os
from wand.image import Image
from PIL import Image as PI
import io
from TableHouseInfo import TableHouseInfo

RAR_FILE_NAME="tmp.rar"
RAR_DIR_NAME ="tmp_rar"
PDF_FILE_NAME = RAR_DIR_NAME+"/123.pdf"

class FileTool(object):

    def download_file_from_url(self, url, name=RAR_FILE_NAME):
        r = requests.get(url)
        with open(name,'wb') as f:
            f.write(r.content)

    def un_rar(self, file_name=RAR_FILE_NAME):
        """unrar zip file"""
        tmp_dir = os.getcwd()
        rar     = rarfile.RarFile(tmp_dir+"/"+file_name)
        if os.path.isdir(RAR_DIR_NAME):
            pass
        else:
            os.mkdir(RAR_DIR_NAME)
        os.chdir(RAR_DIR_NAME)
        rar.extractall()
        rar.close()
        os.chdir(tmp_dir)

'''
    def ocr_pdf_to_text(self, file_name=PDF_FILE_NAME):
        print(file_name)
        tmp_dir    = os.getcwd()
        image_pdf  = Image(filename=tmp_dir+"/"+file_name, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')
        tool = pyocr.get_available_tools()[0]
        lang = tool.get_available_languages()[1]
        print( tool.get_available_languages() )
        req_image = []
        final_text = []
        print("pdf to picture...")
        count=0
        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))
            with open(tmp_dir+"/"+RAR_DIR_NAME+("/pic_%d.jpeg"%count), 'w') as json_f:
                json_f.write(  img_page.make_blob('jpeg')  )
            count = count + 1
        return
        print("OCR ing...")
        count=0
        for img in req_image:
            txt = tool.image_to_string(
                PI.open(io.BytesIO(img)),
                lang='number',
                builder=pyocr.builders.TextBuilder()
            )
            print(txt)
            final_text.append(txt)
            count=count+1
            print('%d / %d'%(count,len(req_image) ))

        with open(tmp_dir+"/"+RAR_DIR_NAME+"/123.txt", 'w') as json_f:
            for line in final_text:
                json_f.write(  line  )
        return

    def ocr_picture_to_text(self, file_name="pic_x.jpeg"):
        print(file_name)
        tmp_dir    = os.getcwd()
        image_jpeg = Image(filename=tmp_dir+"/"+RAR_DIR_NAME+"/"+file_name, resolution=300)
        tool = pyocr.get_available_tools()[0]
        lang = tool.get_available_languages()[1]
        print( tool.get_available_languages())
        req_image  = []
        final_text = []
        print("OCR ing...")
        txt = tool.image_to_string(
            PI.open(io.BytesIO(image_jpeg.make_blob('jpeg'))),
            lang='eng',
            builder=pyocr.builders.TextBuilder()
        )
        print txt
        return
'''
def main():
    filetool = FileTool();
    #filetool.download_file_from_url("https://www.cdfangxie.com/Public/uploadfile/file/20180504/20180504185439_36044.rar")
    #filetool.un_rar()
    #filetool.ocr_pdf_to_text()
    #filetool.ocr_picture_to_text()
    tableinfo = TableHouseInfo(os.getcwd()+"/"+RAR_DIR_NAME+"/pic_0.jpeg")
    #tableinfo.ocr_picture_to_text()

    return

if __name__ == '__main__':
    main()
