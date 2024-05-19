import os
import subprocess



# TrainAnewFontWithTesseract.ipynb : https://colab.research.google.com/github/AniqueManiac/new-font-training-with-tesseract-in-google-colab/blob/main/TrainAnewFontWithTesseract.ipynb

# # install Tesseract-ocr
# subprocess.run(["chmod", "755", "-R", "tesseract/src/training/tesstrain.sh"])

# # Create files
# subprocess.run(["mkdir", "fonts", "output2", "train2"])

# Make the tesstrain.sh script executable
subprocess.run(["chmod", "755", "-R", "tesseract/src/training/tesstrain.sh"])

# Extract eng.lstm from eng.traineddata
subprocess.run(["combine_tessdata", "-e", "tesseract/tessdata/eng.traineddata", "eng.lstm"])

# Remove contents of the train directory
subprocess.run(["rm", "-rf", "train2/*"])

# Remove contents of the output directory
subprocess.run(["rm", "-rf", "output2/*"])

# # Remove contents of the output directory
# subprocess.run(["rm", "-rf", "fonts/.uuid"])

# Run tesstrain.sh to generate training data
subprocess.run(["./tesseract/src/training/tesstrain.sh",
                "--fonts_dir", "font_earthMomma",
                "--fontlist", "Earth Momma",
                "--lang", "eng",
                "--linedata_only",
                "--langdata_dir", "langdata_lstm",
                "--tessdata_dir", "./tesseract/tessdata",
                "--save_box_tiff",
                "--output_dir", "train2"])



# Set environment variable for OMP_THREAD_LIMIT
os.environ['OMP_THREAD_LIMIT'] = '16' # 16 default

# Run lstmtraining to continue training
subprocess.run(["lstmtraining",
                "--continue_from", "eng.lstm",
                "--model_output", "output2/font_name",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--train_listfile", "train2/eng.training_files.txt",
                "--max_iterations", "2000"])

# Run lstmtraining to stop training and generate the traineddata file
subprocess.run(["lstmtraining",
                "--stop_training",
                "--continue_from", "output2/font_name_checkpoint",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--model_output", "output2/earthMomma.traineddata"])


# cmd : tesseract.exe BL_table_final_format.jpg text3.txt -l earthmomma