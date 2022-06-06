from cellimporter import CellImporter
from cellmodeler import CellModeler
from cellprocessor import CellProcessor
from cellclassifier import CellClassifier

cellimporter = CellImporter()
cellimporter.load_images_fld()

cellalligner = CellProcessor()
cellalligner.align_cells(cellimporter.cells)
cellalligner.crop_cells()
cellalligner.save_aligned_cells()

#cellclassifier = CellClassifier()
#cellclassifier.classify_cells(cellalligner.aligned_cells)
#cellclassifier.save_classified_cells()

cellmodeler = CellModeler()
#cellmodeler.create_cell_model(cellalligner.aligned_cells, cellclassifier.classifications, 1)
#cellmodeler.save_cell_model()
#cellmodeler.create_cell_model(cellalligner.aligned_cells, cellclassifier.classifications, 2)
#cellmodeler.save_cell_model()
#cellmodeler.create_cell_model(cellalligner.aligned_cells, cellclassifier.classifications, 3)
#cellmodeler.save_cell_model()
cellmodeler.create_cell_model_from_preclassified()
cellmodeler.save_cell_model()

