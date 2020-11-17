# AC295-practium2
## Introduction
In this practicum, we build a multimodal deep learning model to perform visual question answering tasks. Our teacher model takes advantage of transfer learning on both image and text data, and it achieves a 47% accuracy on the validation data. For additional features, we convert our dataset into TFRecords, apply distillation and pruning to compress the final model.

## Video Link:

## List of Code Files

**VQA_models.ipynb**: This notebook downloads the original data and pre-process them directly. It contains a final model, followed by model **distillation** and model **pruning**.

**TFrecord.ipynb**: This notebook implements one of the additional feature: Convert dataset to **TFRecords**. After pre-processing both images and questions, we save the new dataset to TFRecords. Then, we load the TFRecord data and train our final model.


## Model History Files

Vqa_model_test_metrics.json

Vqa_model_test_train_history.json
