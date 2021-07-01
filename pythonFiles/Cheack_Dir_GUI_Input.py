"""
by Ohad Omrad
"""

"""
this python file handle the input section
"""

import os
import PrintsForUser
import string

class GetDirectory():
    
    
    @staticmethod
    def __cheak_Launguge(path):
        """
        Get: path
        if the path in not allowed to contain hebrew letters
        this function cheak if the path contain only English letters
        """
        for ch in path:
            if not (ch in string.printable):
                return False
        
        return True
    
    @staticmethod
    def cheak_Exsists_Dir(path, flagLang):
        """
        Get: path, launguge flag -> if true -> hebrew letters will consider as an error
        this requset an exsists directory from the user and return it only the current directory exsists
        return true only if the path is valid  
        """
    
        if(flagLang):
            if(not GetDirectory.__cheak_Launguge(path)):
                return "Error - path contains hebrew letters"
        
        if not os.path.exists(path):
            return "Error - this directory is not exsists"
    
        return "Success"
    
   
    
    @staticmethod
    def cheak_New_Dir(path, flagLang):
        """
        Get: a path, a language flag
        return true if the path is vaild and new one else return false
        """

        if(flagLang):
            if(not GetDirectory.__cheak_Launguge(path)):
                return "Error - path contains hebrew letters"
       
        if(os.path.exists(path)):
            """
            cheak that the path is not allready exisist
            if it allrrady exisists return false
            """
            return "Error - this directory is allready exsists"
    
        try:
            """
            try to make a folder in the current path
            if its succed the path is valid
            else
            the path is not vaild and the function return false
            """
            os.mkdir(path)
            os.rmdir(path)
            return "Success"
         
        except:
            if(path != ""):
                return "Error - directory is not valid"
            