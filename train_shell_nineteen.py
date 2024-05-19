import os
import subprocess


training_data_dir = "/home/abdohero/train_new_font/train_nineteen/nineteenNinetySeven-ground-truth"
training_files_list = os.path.join(training_data_dir, "eng.training_files.txt")

with open(training_files_list, 'w') as f:
    for file in os.listdir(training_data_dir):
        if file.endswith(".lstmf"):
            f.write(os.path.join(training_data_dir, file) + "\n")

print(f"Generated {training_files_list} with all .lstmf files")



# TrainAnewFontWithTesseract.ipynb : https://colab.research.google.com/github/AniqueManiac/new-font-training-with-tesseract-in-google-colab/blob/main/TrainAnewFontWithTesseract.ipynb

# # install Tesseract-ocr
# subprocess.run(["chmod", "755", "-R", "tesseract/src/training/tesstrain.sh"])

# # Create files
# subprocess.run(["mkdir", "fonts", "output", "train"])

# Make the tesstrain.sh script executable
subprocess.run(["chmod", "755", "-R", "tesseract/src/training/tesstrain.sh"])

# Extract eng.lstm from eng.traineddata
subprocess.run(["combine_tessdata", "-e", "tesseract/tessdata/eng.traineddata", "eng.lstm"])

# # Remove contents of the train directory
# subprocess.run(["rm", "-rf", "train/*"])

# Remove contents of the output directory
subprocess.run(["rm", "-rf", "output/*"])

# # Remove contents of the output directory
# subprocess.run(["rm", "-rf", "fonts/.uuid"])

# # Run tesstrain.sh to generate training data
# subprocess.run(["./tesseract/src/training/tesstrain.sh",
#                 "--fonts_dir", "font_nineteen",
#                 "--fontlist", "Nineteen Ninety Seven",
#                 "--lang", "eng",
#                 "--linedata_only",
#                 "--langdata_dir", "langdata_lstm",
#                 "--tessdata_dir", "./tesseract/tessdata",
#                 "--save_box_tiff",
#                 "--maxpages", "10",
#                 "--output_dir", "train_nineteen/nineteenNinetySeven-ground-truth"])



# Set environment variable for OMP_THREAD_LIMIT
os.environ['OMP_THREAD_LIMIT'] = '16' # 16 default

# Run lstmtraining to continue training
subprocess.run(["lstmtraining",
                "--continue_from", "eng.lstm",
                "--model_output", "output/font_name",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--train_listfile", "train_nineteen/nineteenNinetySeven-ground-truth/eng.training_files.txt",
                "--max_iterations", "5000"])

# Run lstmtraining to stop training and generate the traineddata file
subprocess.run(["lstmtraining",
                "--stop_training",
                "--continue_from", "output/font_name_checkpoint",
                "--traineddata", "tesseract/tessdata/eng.traineddata",
                "--model_output", "output/ninetyseven.traineddata"])


# cmd : tesseract.exe BL_table_final_format.jpg text3.txt -l earthmomma