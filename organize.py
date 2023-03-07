import os, sys
import zipfile
import shutil
from PIL import Image

def extract_file(filepath):
    if zipfile.is_zipfile(filepath): 
        with zipfile.ZipFile(filepath) as item:
            item.extractall()

def read_first_line(file):
    with open(file, 'rt') as fd:
         first_line = fd.readline()
    return first_line[:-1]

def find_all_text_files(input_path):
    all_text_files = []
    for file in os.listdir("./"+input_path):
        if file.endswith(".txt"):
            all_text_files.append(file)
    return all_text_files


def move_images(file, object_type, filepath, input_path, output_path):
    if file.endswith(".jpg"):
        os.rename("./"+input_path+file, "./"+input_path+"image.jpg")
    if file.endswith(".png"):
        im = Image.open(r"./"+input_path+file)
        im.save(r"./"+input_path+"image.jpg","JPEG")
        os.remove("./"+input_path+file)
    if file.endswith(".bmp"):
        im = Image.open(r"./"+input_path+file)
        im.save(r"./"+input_path+"image.jpg", "JPEG")
        os.remove("./"+input_path+file)   
    shutil.move("./"+input_path+"image.jpg", "./"+output_path+object_type+"/"+filepath[:-4]+"/image.jpg")
    return 0

def move_segementaion(file, object_type, filepath, input_path, output_path):
    if file.endswith(".gif"):
        os.rename("./"+input_path+file, "./"+input_path+"segmentation.gif")
    if file.endswith(".tif"):
        im = Image.open(r"./"+input_path+file)
        im.save(r"./"+input_path+"segmentation.gif","GIF")
        os.remove("./"+input_path+file)
    shutil.move("./"+input_path+"segmentation.gif", "./"+output_path+object_type+"/"+filepath[:-4]+"/segmentation.gif")
    return 0

def reorder_files(input_path, output_path):
    set = {""}
    all_text_files = find_all_text_files(input_path)
    metadata_file = open('metadata_overview.txt', 'w+')
    metadata_file.write("The org_data is an organized folders of similar objects and have five attributes - photo, object, histogram,segmentaion and statistcs\n\n")
    for file in all_text_files:
        object_type = (read_first_line("./"+input_path+file))
        set.add(object_type)
        for rest_files in os.listdir("./"+input_path):
            if rest_files.startswith(file[:-4]):
                if not os.path.exists("./"+output_path+object_type+"/"+file[:-4]):
                    os.makedirs("./"+output_path+object_type+"/"+file[:-4])
                if rest_files.endswith(".jpg") or rest_files.endswith(".png") or rest_files.endswith(".bmp"):
                    move_images(rest_files, object_type, file, input_path, output_path)
                if rest_files.endswith(".txt"):
                    os.rename("./"+input_path+rest_files, "./"+input_path+"object.txt")
                    shutil.move("./"+input_path+"object.txt", "./"+output_path+object_type+"/"+file[:-4]+"/object.txt")
                if rest_files.endswith(".tsv"):
                    os.rename("./"+input_path+rest_files, "./"+input_path+"histogram.tsv")
                    shutil.move("./"+input_path+"histogram.tsv", "./"+output_path+object_type+"/"+file[:-4]+"/histogram.tsv")
                if rest_files.endswith(".tif") or rest_files.endswith("gif"):
                    move_segementaion(rest_files, object_type, file, input_path, output_path)
                if rest_files.endswith(".csv"):
                    os.rename("./"+input_path+rest_files, "./"+input_path+"statistics.csv")
                    shutil.move("./"+input_path+"statistics.csv", "./"+output_path+object_type+"/"+file[:-4]+"/statistics.csv")
    metadata_file.write("The Objects are:")
    for types in set:
        metadata_file.write(types + "\n") 

    metadata_file.flush()    
    metadata_file.close()


if __name__ == '__main__':

    reorder_files(sys.argv[1], sys.argv[2])



