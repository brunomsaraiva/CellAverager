import os
import numpy as np
from tkinter import filedialog as fd
from skimage.io import imsave, imread
from skimage.transform import resize
from skimage.exposure import rescale_intensity


class CellModeler(object):

    def __init__(self):
        self.cell_model = None
        self.mean_x = 0
        self.mean_y = 0

    def resize_cells(self, cells):
        tmp = []
        for cell in cells:
            tmp.append(resize(cell, (self.mean_x, self.mean_y)))

        return np.array(tmp)

    def create_cell_average(self, cells):
        model_cell = np.zeros((self.mean_x, self.mean_y))
        for cell in rescale_intensity(np.array(cells)):
            model_cell += cell

        model_cell /= float(len(cells))

        #model_cell_average = np.mean(model_cell[np.nonzero(model_cell)])
        #model_cell /= model_cell_average

        return model_cell

    def create_cell_model_from_preclassified(self, path=None):
        if path is None:
            path = fd.askdirectory()
        
        selected_cells = []
        xs = []
        ys = []

        for cell in os.listdir(path):
            cell = imread(path + os.sep + cell)
            selected_cells.append(cell)
            xs.append(cell.shape[0])
            ys.append(cell.shape[1])

        self.mean_x = int(np.mean(np.array(xs)))
        self.mean_y = int(np.mean(np.array(ys)))
        
        selected_cells = self.resize_cells(selected_cells)

        self.cell_model = self.create_cell_average(selected_cells)

    def create_cell_model(self, cells, classifications, phase):
        selected_cells = []
        xs = []
        ys = []

        for classification in classifications:
            cell_id, p = classification
            if p == phase:
                selected_cells.append(cells[cell_id])
                xs.append(cells[cell_id].shape[0])
                ys.append(cells[cell_id].shape[1])
        
        self.mean_x = int(np.mean(np.array(xs)))
        self.mean_y = int(np.mean(np.array(ys)))
        
        selected_cells = self.resize_cells(selected_cells)

        self.cell_model = self.create_cell_average(selected_cells)

    def save_cell_model(self, path=None):
        if path is None:
            path = fd.asksaveasfilename()

        imsave(path + ".tif", self.cell_model)

