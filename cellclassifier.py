import os
import tkinter as tk
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as fd
from skimage.exposure import rescale_intensity
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from skimage.io import imsave


class CellClassifier(object):

    def __init__(self):
        self.cells = None
        self.current_cell_idx = 0
        self.cells_keys = None
        self.classifications = []

    def choose_phase(self, phase):
        self.classifications.append((self.cells_keys[self.current_cell_idx], phase))

        if self.current_cell_idx >= len(self.cells_keys)-1:
            self.main_window.destroy()
            self.main_window.quit()

        else:
            self.current_cell_idx += 1
            self.show_image()

    def show_image(self):
        self.ax.cla()
        self.ax.imshow(self.cells[self.cells_keys[self.current_cell_idx]], cmap="gray")
        self.canvas.draw()

    def previous_cell(self):
        self.classifications = self.classifications[:-1]
        self.current_cell_idx -= 1
        self.show_image()

    def key(self, event):
        if event.char == "1":
            self.choose_phase(1)
        elif event.char == "2":
            self.choose_phase(2)
        elif event.char == "3":
            self.choose_phase(3)
        elif event.char == "d":
            self.choose_phase("Discard")
        elif event.char == "b":
            self.previous_cell()

    def on_closing(self):
        """Creates a prompt when trying to close the main windows"""
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            self.main_window.destroy()
            self.main_window.quit()

    def classify_cells(self, aligned_cells):
        self.cells = aligned_cells
        self.cells_keys = list(self.cells.keys())

        self.main_window = tk.Tk()
        self.cell_frame = tk.Frame(self.main_window)
        self.cell_frame.pack(fill="x")
        self.button_frame = tk.Frame(self.main_window)
        self.button_frame.pack(fill="x")
        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, self.cell_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top")
        self.ax = plt.subplot(111)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
        self.ax.axis("off")
        plt.autoscale(False)

        self.phase1_button = tk.Button(
            self.button_frame, text="Phase 1", command=lambda: self.choose_phase(1))
        self.phase1_button.pack(side="left")

        self.phase2_button = tk.Button(
            self.button_frame, text="Phase 2", command=lambda: self.choose_phase(2))
        self.phase2_button.pack(side="left")

        self.phase3_button = tk.Button(
            self.button_frame, text="Phase 3", command=lambda: self.choose_phase(3))
        self.phase3_button.pack(side="left")

        self.discard_button = tk.Button(
            self.button_frame, text="Discard Cell", command=lambda: self.choose_phase("Discard"))
        self.discard_button.pack(side="left")

        self.back_button = tk.Button(self.button_frame, text="Back", command=self.previous_cell)
        self.back_button.pack(side="right")

        self.main_window.bind("<Key>", self.key)

        self.show_image()

        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main_window.mainloop()

    def save_classified_cells(self, path=None):
        if path is None:
            path = fd.askdirectory()
        
        if not os.path.exists(path + os.sep + "Phase 1"):
            os.mkdir(path + os.sep + "Phase 1")
        if not os.path.exists(path + os.sep + "Phase 2"):
            os.mkdir(path + os.sep + "Phase 2")
        if not os.path.exists(path + os.sep + "Phase 3"):
            os.mkdir(path + os.sep + "Phase 3")
        if not os.path.exists(path + os.sep + "Discarded"):
            os.mkdir(path + os.sep + "Discarded")
        
        for cell_id, cls in self.classifications:
            if cls == 1:
                imsave(path + os.sep + "Phase 1" + os.sep + cell_id + ".tif", self.cells[cell_id])
            if cls == 2:
                imsave(path + os.sep + "Phase 2" + os.sep + cell_id + ".tif", self.cells[cell_id])
            if cls == 3:
                imsave(path + os.sep + "Phase 3" + os.sep + cell_id + ".tif", self.cells[cell_id])
            if cls == "Discard":
                imsave(path + os.sep + "Discarded" + os.sep + cell_id + ".tif", self.cells[cell_id])

