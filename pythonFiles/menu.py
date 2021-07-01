"""
by Ohad Omrad
"""


"""
this is the main python file that manege the program according to the user choicess
"""
import os
import train_model
import classify
import Cheak_Dir
import PrintsForUser
import random
import camera

def options():
    """
    This function prints for the user his options (UI)
    """
    PrintsForUser.printOptions("******************************************")
    PrintsForUser.printOptions("*          USER INTERFACE                *")
    PrintsForUser.printOptions("*                                        *")
    PrintsForUser.printOptions("*   Enter 1 --> train the model          *")
    PrintsForUser.printOptions("*   Enter 2 --> predict an image         *")
    PrintsForUser.printOptions("*   Enter 3 --> predict random images    *")
    PrintsForUser.printOptions("*   Enter 4 --> take an image            *")
    PrintsForUser.printOptions("*   Enter space bar --> exit             *")
    PrintsForUser.printOptions("*                                        *")
    PrintsForUser.printOptions("******************************************")


def case_One(sorted_data_path):
    """
    Get: the path to the updated sorted data set
    return: the model path and the labels path
           the mpdel path -> contains the trained model
           the labels path - contains the labels for each images (for the predict)

    this function call to the handle_train() fanction that locaited in train_model.py file
    """
    
    model_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output model: ")
    lb_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output label binarizer: ")
    
    while model_path == lb_path:
        PrintsForUser.printError("Error - file will be override")
        lb_path = Cheak_Dir.GetDirectory.get_New_Dir("Enter the full path (with the name) to output label binarizer: ")
            
    plot_dir = Cheak_Dir.GetDirectory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ")
    
    while model_path == plot_dir or lb_path == plot_dir:
        PrintsForUser.printError("Error - file will be override")
        plot_dir = Cheak_Dir.GetDirectory.get_New_Dir("Enter the folder directory to output accuracy/loss plot: ")

    os.mkdir(plot_dir)
    
    train_obj = train_model.TrainModel(sorted_data_path, model_path,lb_path, plot_dir)
    
    train_obj.handle_train() 
    
    return model_path, lb_path


def case_Two(model_path, labels_path):
    """
    Get: the path to the trained model
         the path to the images labels
    
    this function call to the handle_classify() fanction that locaited in classify.py file
    """
    
    image_path = Cheak_Dir.GetDirectory.is_Exsists("Enter the image path:\nPath Must be in English!", True)
    predict_obj = classify.ImagePredictor(model_path, labels_path)  
    predict_obj.handle_classify(image_path)

def case_Three(model_path, labels_path, data_set, new_images_folder):
    """
    Get: the path to the trained model
         the path to the images labels
         the data set
         a folder with unlearned images
    this function predict 11 random images from each folder
    """
    PrintsForUser.printProcess("[INFO] Learned images...")
    cheakPredict(model_path, labels_path, data_set, 5)
    PrintsForUser.printProcess("[INFO] New images...")
    cheakPredict(model_path, labels_path, new_images_folder, 5)
    

   
def cheakPredict(model_path, labels_path, data_set, num):
    
    list_of_images = os.listdir(data_set)
    pre = classify.ImagePredictor(model_path, labels_path)
    
    for i in range(num):
        image_name = random.choice(list_of_images)
        image_path =  data_set+ r"/" + image_name
        pre.handle_classify(image_path)
        list_of_images.remove(image_name)
        
        
    
def menu():
    flag = True
    options()
    """
    defult directories
    this directoties change according to the user activity
    """
    #directories_file.create_directories_file()
    
    data_set = r"C:\Users\ilano\OneDrive\Desktop\DL Project\images"
    sorted_data_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\Data"
    model_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\Model_sigmoid_15.model"
    labels_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\lb_sigmoid_15.pickle"
    new_images_folder = r"C:\Users\ilano\OneDrive\Desktop\DL Project\NewImages"
    
    while(flag):
        PrintsForUser.printOptions("--> Your Choice: ")
        choice = input("Enter: ")
        
    
        if choice == '1':
            """
            if the use enter 1 -> the directory of the model and the labeld will be updated
            """
            model_path,labels_path =  case_One(sorted_data_path)
            PrintsForUser.printProcess("[INFO] Using trained model")
         
        if choice == '2':
            """
            if the use enter 3 -> the program will use the updated directory and predict the image
            """
            case_Two(model_path,labels_path)
            
        if choice == '3':
            case_Three(model_path,labels_path, data_set, new_images_folder)
            
        if choice == '4':
            camera.takeImage()
              
            
        if choice == ' ':
            PrintsForUser.printProcess("[INFO] Exiting...")
            flag = False
    
    
if __name__ == "__main__":
    menu()