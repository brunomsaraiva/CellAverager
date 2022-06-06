import cv2 as cv
import os
import numpy as np
from skimage.io import imread
from tkinter import filedialog as fd

class CellImporter(object):

    def __init__(self):
        self.cells = None

    def load_images_fld(self, path=None):
        if path is None:
            path = fd.askdirectory()

        self.cells = {}

        for cell in os.listdir(path):
            cell_id = cell.split(".")[0]

            tmp_img = imread(path + os.sep + cell)
            tmp_img = cv.copyMakeBorder(tmp_img,10,10,10,10,cv.BORDER_CONSTANT,value=0)

            self.cells[cell_id] = tmp_img

    def load_report_data(self, path=None):
        if path is None:
            path = fd.askdirectory()

        for fld in os.listdir(path):

            report_path = path + os.sep + fld
            print(fld)
            image_name = fld.split("_")[1]

            cells_path = report_path + os.sep + "_cell_data" + os.sep + "fluor"
            cells_list = os.listdir(cells_path)
            self.cells = {}

            for cell in cells_list:
                cell_id = image_name + "_" + cell.split(".")[0]

                tmp_img = imread(cells_path + os.sep + cell)
                tmp_img = cv.copyMakeBorder(tmp_img,10,10,10,10,cv.BORDER_CONSTANT,value=0)

                self.cells[cell_id] = tmp_img[:, int(tmp_img.shape[1]/2):]

