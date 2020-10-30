from imageai.Detection.Custom import DetectionModelTrainer

manaf = DetectionModelTrainer()
manaf.setModelTypeAsYOLOv3()
manaf.setDataDirectory(data_directory="AI-ny")
manaf.setTrainConfig(object_names_array=["Kartong", "Plast", "Metall"], batch_size=2, num_experiments=180, train_from_pretrained_model="pretrained-yolov3.h5")
manaf.trainModel()
