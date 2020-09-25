from imageai.Detection.Custom import DetectionModelTrainer
import os

#Ändra till sina egna
D_PATH = ""
Model_Path = ""


manaf = DetectionModelTrainer()
manaf.setModelTypeAsYOLOv3()
manaf.setDataDirectory(data_directory=PATH)
manaf.setTrainConfig(object_names_array=[], batch_size=8, num_experiments=100, train_from_pretrained_model=Model_Path)
manaf.trainModel()
