# -*- coding: utf-8 -*-
"""
@author: Amit
"""

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

import PrintsForUser
import train_model
import classify
import camera
import Cheack_Dir_GUI_Input

import os
import random

global_data_set = r"C:\Users\ilano\OneDrive\Desktop\DL Project\images"
global_sorted_data_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\Data"   #sorted data direction
global_model_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\Model_sigmoid_15.model" #model direction
global_labels_path = r"C:\Users\ilano\OneDrive\Desktop\DL Project\lb_sigmoid_15.pickle" #labels (binari) direction
global_new_images_folder = r"C:\Users\ilano\OneDrive\Desktop\DL Project\NewImages"

class MainWindow(Screen):
    pass    

class OptionsWindow(Screen):

    def PredictRandom(self):
        PrintsForUser.printProcess("[INFO] Learned images...")
        self.cheakPredict(global_model_path, global_labels_path, global_data_set, 5)
        PrintsForUser.printProcess("[INFO] New images...")
        self.cheakPredict(global_model_path, global_labels_path, global_new_images_folder, 5)
    
    def cheakPredict(self, model_path, labels_path, data_set, num):
    
        list_of_images = os.listdir(data_set)
        pre = classify.ImagePredictor(model_path, labels_path)
    
        for i in range(num):
            image_name = random.choice(list_of_images)
            image_path =  data_set+ r"/" + image_name
            pre.handle_classify(image_path)
            list_of_images.remove(image_name)
            
    def takeImage(self):
        camera.takeImage()

            

class TrainWindow(Screen):
    model = ObjectProperty(None)
    label = ObjectProperty(None)
    plot = ObjectProperty(None)
    
    
    def Submit(self):
        model_path = self.model.text
        self.model.text = ""
        
        label_path = self.label.text
        self.label.text = ""
        
        plot_path = self.plot.text
        self.plot.text = ""
        
        ret_message = Cheack_Dir_GUI_Input.GetDirectory.cheak_New_Dir(model_path, False)
        if ret_message != "Success":
            self.model.text = ret_message
        
        ret_message = Cheack_Dir_GUI_Input.GetDirectory.cheak_New_Dir(label_path,False)
        if ret_message != "Success":
            self.label.text = ret_message
        
        ret_message = Cheack_Dir_GUI_Input.GetDirectory.cheak_New_Dir(plot_path, False)
        if ret_message != "Success":
            self.plot.text = ret_message
        
            
        if self.model.text == "" and self.label.text == "" and self.plot.text == "":
            os.mkdir(plot_path)
            train_obj = train_model.TrainModel(global_sorted_data_path, model_path,label_path, plot_path)
            train_obj.handle_train()
            
        global_model_path = model_path
        global_labels_path = label_path
               
             
class PredictWindow(Screen):
    image = ObjectProperty(None)
         
    def Submit(self):
        image_path = self.image.text
        self.image.text = ""
        
        ret_message = Cheack_Dir_GUI_Input.GetDirectory.cheak_Exsists_Dir(image_path, True)
        if ret_message != "Success":
            self.image.text = ret_message
        
        else:
            predict_obj = classify.ImagePredictor(global_model_path, global_labels_path)  
            predict_obj.handle_classify(image_path)
        

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('kivyfile.kv')

class myapp(App):
    def build(self):
        return (kv)

if __name__=="__main__":
    myapp().run()