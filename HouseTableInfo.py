import os
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io
import datetime

def rgbs_to_gray(rgbs):
    return ((3*(rgbs[0]>>3)) + (rgbs[1]>>1) + (rgbs[2]>>3) )

def rgb_to_gray(r, g, b):
    gray = 0.299*r + 0.587*g + 0.114*b
    return gray

class TablePoint(object):
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%d, %d)' % (self.x, self.y)
    __repr__ = __str__

class TableConfig(object):
    border_size = 5
    border_x    = 10
    border_y    = 5
    border_len  = 60
    gray        = 128


class TableHouseInfo(object):
    __file_name  = None
    __tableinfo  = []
    __row_side   = []
    __col_side   = []
    __cfg        = TableConfig()
    point_topleft     = TablePoint(0, 0)
    point_topright    = TablePoint(0, 0)
    point_bottomleft  = TablePoint(0, 0)
    point_bottomright = TablePoint(0, 0)
    row    = 0
    column = 0

    def __init__(self, filename=None):
        if filename != None:
            self.filename = filename
            self.init_table(filename)

    def reset_filename(self, filename=None):
        if filename != None:
            self.filename = filename

    def __is_matched(self, rgbs):
        if rgbs_to_gray(rgbs) < self.__cfg.gray:
            return True
        return False

    def __has_left(self, point, img):
        if point.x <= self.__cfg.border_len:
            return False
        for i in range(0, self.__cfg.border_len):
            if not self.__is_matched(img.getpixel( (point.x-i, point.y) )):
                return False
        return True

    def __has_top(self, point, img):
        if point.y <= self.__cfg.border_len:
            return False
        for i in range(0, self.__cfg.border_len):
            if not self.__is_matched(img.getpixel( (point.x, point.y-i) )):
                return False
        return True

    def __has_right(self, point, img):
        if point.x >= (img.size[0] - self.__cfg.border_len):
            return False
        for i in range(0, self.__cfg.border_len):
            if not self.__is_matched(img.getpixel( (point.x+i,point.y) )):
                return False
        return True

    def __has_bottom(self, point, img):
        if point.y >= (img.size[1] - self.__cfg.border_len):
            return False
        for i in range(0, self.__cfg.border_len):
            if not self.__is_matched(img.getpixel( (point.x, point.y+i) )):
                return False
        return True

    def __has_direction(self, point, img, c=3):
        count = 0
        if self.__has_top(point, img):
            count = count + 1
        if self.__has_left(point, img):
            count = count + 1
        if self.__has_right(point, img):
            count = count + 1
        if self.__has_bottom(point, img):
            count = count + 1
        if count >= c:
            return True
        return False

    def __set_topleft(self, img):
        max = img.size[0]
        if max < img.size[1]:
            max = img.size[1]

        for i in range(1, max):
            # adjust same
            if self.__is_matched(img.getpixel( (i-1, i-1) ) ):
                p = TablePoint(i-1, i-1)
                #print(p)
                if self.__has_right(p, img) and self.__has_bottom(p, img):
                    self.point_topleft = p
                    return True
            # adjust x
            min = i
            if min > img.size[0]:
                min = img.size[0]
            for j_x in range(0, min):
                if self.__is_matched(img.getpixel( (j_x, i) )  ):
                    p = TablePoint(j_x, i)
                    #print(p)
                    if self.__has_right(p, img) and self.__has_bottom(p, img):
                        self.point_topleft = p
                        return True
            # adjust y
            min = i
            if min > img.size[1]:
                min = img.size[1]
            for j_y in range(0, min):
                if self.__is_matched(img.getpixel( (i, j_y) ) ):
                    p = TablePoint(i, j_y)
                    #print(p)
                    if self.__has_right(p, img) and self.__has_bottom(p, img):
                        self.point_topleft = p
                        return True
        return False

    def __set_bottomright(self, img):
        m_x = img.size[0] - 1
        m_y = img.size[1] - 1
        max = m_x
        if max < m_y:
            max = m_y

        for i in range(0, max):
            # adjust x
            float_x  = m_x - i
            float_y  = m_y - i
            if float_x <= 0:
                float_x = 0
            if float_y <= 0:
                float_y = 0

            # adjust x
            for j_x in range(m_x, float_x, -1):
                if self.__is_matched(img.getpixel( (j_x, float_y) )  ):
                    p = TablePoint(j_x, float_y)
                    #print(p)
                    if self.__has_left(p, img) and self.__has_top(p, img):
                        self.point_bottomright = p
                        return True
            # adjust y
            for j_y in range(m_y, float_y, -1):
                if self.__is_matched(img.getpixel( (float_x, j_y) ) ):
                    p = TablePoint(float_x, j_y)
                    #print(p)
                    if self.__has_left(p, img) and self.__has_top(p, img):
                        self.point_bottomright = p
                        return True
        return False

    def __set_topright(self, img):
        __max = max(max(img.size[0], img.size[1]) - 1, 0)
        max_x = max(img.size[0] - 1, 0 )
        max_y = max(img.size[1] - 1, 0 )

        for i in range(0, __max):
            std_x = max_y - min(i, max_x)
            std_y = min(i, max_y)
            # adjust x
            for j_x in range(max_x, std_x, -1):
                if self.__is_matched(img.getpixel( (j_x, std_y) )  ):
                    p = TablePoint(j_x, std_y)
                    #print(p)
                    if self.__has_left(p, img) and self.__has_bottom(p, img):
                        self.point_topright = p
                        return True
            # adjust y
            for j_y in range(0, std_y):
                if self.__is_matched(img.getpixel( (std_x, j_y) ) ):
                    p = TablePoint(std_x, j_y)
                    #print(p)
                    if self.__has_left(p, img) and self.__has_bottom(p, img):
                        self.point_topright = p
                        return True
        return False

    def __set_bottomleft(self, img):
        __max = max(max(img.size[0], img.size[1]) - 1, 0)
        max_x = max(img.size[0] - 1, 0 )
        max_y = max(img.size[1] - 1, 0 )

        for i in range(0, __max):
            std_x = min(i, max_x)
            std_y = max_y - min(i, max_y)
            # adjust x
            for j_x in range(0 , std_x):
                if self.__is_matched(img.getpixel( (j_x, std_y) )  ):
                    p = TablePoint(j_x, std_y)
                    #print(p)
                    if self.__has_top(p, img) and self.__has_right(p, img):
                        self.point_bottomleft = p
                        return True
            # adjust y
            for j_y in range(max_y, std_y, -1):
                if self.__is_matched(img.getpixel( (std_x, j_y) ) ):
                    p = TablePoint(std_x, j_y)
                    #print(p)
                    if self.__has_top(p, img) and self.__has_right(p, img):
                        self.point_bottomleft = p
                        return True
        return False

    def ___set_tables(self, img):
        self.row     = 2
        self.column  = 2
        y = self.point_topleft.y
        while y < self.point_bottomright.y:
            __column      = []
            __col_count   = 2
            __find_column = False
            x             = self.point_topleft.x
            while x < self.point_bottomright.x:
                p = TablePoint(x, y)
                #print(p)
                if self.__has_tri_direction(p, img):
                    __column.append(p)
                    __col_count   = __col_count + 1
                    __find_column = True
                    x             = x + self.__cfg.border_len
                else:
                    x             = x+1
            if __find_column == True:
                self.__tableinfo.append(__column)
                self.row    = self.row + 1
                self.column = max(__col_count, self.row)
                y           = y + self.__cfg.border_len
            else:
                y           = y + 1

    def __set_sides(self, img):
        self.row     = 0
        self.column  = 0

        y = self.point_topleft.y
        while y <= self.point_bottomright.y:
            x = self.point_topleft.x
            p = TablePoint(x, y)
            if self.__has_right(p, img) and (self.__has_top(p, img) or self.__has_bottom(p, img)):
                self.__row_side.append(y)
                self.row      = self.row + 1
                y             = y + self.__cfg.border_len
            else:
                y             = y + 1

        x = self.point_topleft.x
        while x <= self.point_bottomright.x:
            y = self.point_topleft.y
            p = TablePoint(x, y)
            if self.__has_bottom(p, img) and (self.__has_left(p, img) or self.__has_right(p, img)):
                self.__col_side.append(x)
                self.column   = self.column + 1
                x             = x + self.__cfg.border_len
            else:
                x             = x + 1

    def tb(self, side_x, side_y):
        return TablePoint(self.__col_side[side_x], self.__row_side[side_y])

    def __set_tables(self, img):
        if self.row < 2 or self.column < 2:
            return
        for x in range(0, self.column - 1):
            end_x = x + 1
            for y in range(0, self.row - 1):
                end_y = y + 1
                tl = self.tb(x, y)
                br = self.tb(end_x, end_y)
                tl.x = tl.x + self.__cfg.border_x
                tl.y = tl.y + self.__cfg.border_y
                #img_new = PI.new("RGB", (br.x - tl.x, br.y - tl.y), (255, 255, 255))
                # 第一次
                img_new = img.crop((tl.x, tl.y, br.x, br.y))
                # 二值化
                # 第一次识别，非空则成功，空则第二次识别
                # 第二此识别，边界模糊化，空则第三次识别
                # 第三次识别，边界加粗，否则失败
                self.ocr_region_to_text(img_new)
                #img_new.show()

    def init_table(self, filename=None):
        if filename == None:
            if self.filename != None:
                filename = self.filename
            else:
                print("Error no init_table file name!")
                return
        print(filename)
        # how to do if lack row or increase row?
        # print self.__tableinfo[1][2]
        im = PI.open(filename)

        print(im.size)
        #im.getpixel((4,4))
        starttime = datetime.datetime.now()
        self.__set_topleft(im)
        self.__set_bottomright(im)
        #self.__set_topright(im)
        #self.__set_bottomleft(im)
        self.__set_sides(im)
        self.__set_tables(im)
        endtime = datetime.datetime.now()
        #print(self.point_topleft)
        #print(self.point_bottomright)
        #print(self.__tableinfo)
        print(self.__col_side)
        print(self.__row_side)
        #print(self.row)
        #print(self.column)
        print (endtime - starttime)
        #im.getpixel((4,4))
        #img.putpixel((4,4),(255,0,0))


        return self.__tableinfo

    def ocr_region_to_text(self, im, mode="eng"):
        tool = pyocr.get_available_tools()[0]
        #mode = tool.get_available_languages()[1]
        #print( tool.get_available_languages())
        #req_image  = []
        #final_text = []
        txt = tool.image_to_string(
            im , lang=mode,
            builder = pyocr.builders.TextBuilder()
        )
        print(txt)
        # 去除所有空格
        # 转化,为.
        return


    def ocr_picture_to_text(self, filename=None):
        if filename == None:
            if self.filename != None:
                filename = self.filename
            else:
                print("Error no ocr_picture_to_text file name!")
                return

        print(filename)
        image_jpeg = Image(filename=filename, resolution=300)
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
