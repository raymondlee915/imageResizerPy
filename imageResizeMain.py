import os
import glob
import concurrent.futures
from shutil import copyfile
import re
from PIL import Image

#  this file will resize the images in input_folder and save them into output_folder, 
input_folder = "input"
output_folder = "output"
max_dimension = 2000

output_folder += "\\" + str(max_dimension)

if os.path.exists(output_folder) == False:
    os.makedirs(output_folder)

def resizeImage(image_path):
    if os.path.isfile(image_path) == False:
        return
    im = Image.open(image_path)

    originalWidth = im.size[0]
    originalHeight = im.size[1]

    # output_folder = output_folder + "/" + str(max_dimension)

    # if os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    print("input path: ", image_path)
    newpath = image_path.replace(input_folder, output_folder )
    print("new path: ", newpath)
    directory = os.path.dirname(newpath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    if originalHeight>max_dimension or originalWidth > max_dimension:
        if originalWidth>originalHeight:
            newWidth = max_dimension
            newHeight = int(originalHeight*newWidth/originalWidth)
        else:
            newHeight = max_dimension
            newWidth = int(originalWidth*newHeight/originalHeight)        

        im.resize((newWidth, newHeight)).save(newpath)
    else:
        im.save(newpath)

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        image_list = glob.glob(input_folder+"\\**\\*.jpg")
        for img_path, out_file in zip(image_list, executor.map(resizeImage, image_list)):
            print(img_path.split("\\")[-1], ',', out_file, ', processed')


if __name__ == '__main__':
    main()
    # resizeImage("input/MB1010191904010083-0_002 (35218604)-16.jpg")
    print('done')
