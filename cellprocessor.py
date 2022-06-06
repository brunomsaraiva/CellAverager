import os
import math
import numpy as np
from skimage.io import imsave
from skimage.filters import threshold_isodata
from skimage.transform import rotate
from skimage.morphology import binary_erosion
from sklearn.decomposition import PCA
from tkinter import filedialog as fd


class CellProcessor(object):

    def __init__(self):
        self.aligned_cells = None

    def calculate_cell_outline(self, binary):
        outline = binary * (1 - binary_erosion(binary))

        return outline

    def calculate_major_axis(self, outline):
        x, y = np.nonzero(outline)
        x = [[val] for val in x]
        y = [[val] for val in y]
        coords = np.concatenate((x, y), axis=1)

        pca = PCA(n_components=1)
        pca.fit(coords)

        pos_x, pos_y = pca.mean_
        eigenvector_x, eigenvector_y = pca.components_[0]
        eigenval = pca.explained_variance_[0]

        return [[pos_x-eigenvector_x*eigenval, pos_y-eigenvector_y*eigenval], [pos_x+eigenvector_x*eigenval, pos_y+eigenvector_y*eigenval]]

    def calculate_axis_angle(self, major_axis):
        x0, y0 = major_axis[0]
        x1, y1 = major_axis[1]

        if x0 - x1 == 0:
            angle = 0.0

        elif y0 - y1 == 0:
            angle = 90.0

        else:
            if y1 > y0:
                if x1 > x0:
                    direction = -1
                    opposite = x1 - x0
                    adjacent = y1 - y0
                else:
                    direction = 1
                    opposite = x0 - x1
                    adjacent = y1 - y0

            elif y0 > y1:
                if x1 > x0:
                    direction = 1
                    opposite = x1 - x0
                    adjacent = y0 - y1
                else:
                    direction = -1
                    opposite = x0 - x1
                    adjacent = y0 - y1

            angle = math.degrees(math.atan(opposite/adjacent)) * direction

        if angle != 0:
            angle = 90.0 - angle
        else:
            angle = 90

        return angle

    def calculate_rotation_angle(self, cell):
        binary = cell > threshold_isodata(cell)
        outline = self.calculate_cell_outline(binary)
        major_axis = self.calculate_major_axis(outline)

        return self.calculate_axis_angle(major_axis)

    def align_cells(self, cells):
        self.aligned_cells = {}
        for cell_id in cells.keys():
            print(cell_id)
            tmp_cell = np.array(cells[cell_id])
            self.aligned_cells[cell_id] =  rotate(tmp_cell, self.calculate_rotation_angle(tmp_cell))

    def remove_background(self, cell):
        binary = cell > threshold_isodata(cell)

        top_x, left_y = 0, 0
        bot_x, right_y = cell.shape[0], cell.shape[1]

        for i in range(0, int(cell.shape[0]/2), 1):
            if np.sum(binary[i]) == 0:
                top_x = i+1

        for i in range(int(cell.shape[0])-1, int(cell.shape[0]/2), -1):
            if np.sum(binary[i]) == 0:
                bot_x = i

        for i in range(0, int(cell.shape[1]/2), 1):
            if np.sum(binary[:, i]) == 0:
                left_y = i+1

        for i in range(int(cell.shape[1])-1, int(cell.shape[1]/2), -1):
            if np.sum(binary[:, i]) == 0:
                right_y = i

        return np.array(cell[top_x:bot_x, left_y:right_y])

    def crop_cells(self):
        for cell_id in self.aligned_cells.keys():
            self.aligned_cells[cell_id] = self.remove_background(self.aligned_cells[cell_id])

    def save_aligned_cells(self):
        path = fd.askdirectory()
        for cell_id in self.aligned_cells.keys():
            imsave(path + os.sep + cell_id + ".png", self.aligned_cells[cell_id])

