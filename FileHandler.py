


class Findhandler:
    root_directory = "static"
    
    def loadHTML(this,file_name: str):
        file = open(this.root_directory + file_name + ".html" , "w+")
        data = file.readlines() 
        return data