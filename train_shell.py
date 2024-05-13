import os
import subprocess

# Make the tesstrain.sh script executable
subprocess.run(["chmod", "755", "-R", "tesseract/src/training/tesstrain.sh"])

# Extract eng.lstm from eng.traineddata
subprocess.run(["combine_tessdata", "-e", "tesseract/tessdata/eng.traineddata", "eng.lstm"])

# Remove contents of the train directory
subprocess.run(["rm", "-rf", "train/*"])

# Run tesstrain.sh to generate training data
subprocess.run(["./tesseract/src/training/tesstrain.sh",
                "--fonts_dir", "fonts",
                "--fontlist", "Earth Momma",
                "--lang", "eng",
                "--linedata_only",
                "--langdata_dir", "langdata_lstm",
                "--tessdata_dir", "./tesseract/tessdata",
                "--save_box_tiff",
                "--maxpages", "10",
                "--output_dir", "train"])

# Remove contents of the output directory
subprocess.run(["rm", "-rf", "output/*"])

# Set environment variable for OMP_THREAD_LIMIT
os.environ['OMP_THREAD_LIMIT'] = '16'

# Run lstmtraining to continue training
subprocess.run(["lstmtraining",
                "--continue_from", "eng.lstm",
                "--model_output", "output/font_name",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--train_listfile", "train/eng.training_files.txt",
                "--max_iterations", "400"])

# Run lstmtraining to stop training and generate the traineddata file
subprocess.run(["lstmtraining",
                "--stop_training",
                "--continue_from", "output/font_name_checkpoint",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--model_output", "output/earthmomma.traineddata"])
