import webview

class Filehandler:
    root_directory = "static"
    
    def loadHTML(this,file_name: str) -> str:
        file = open(this.root_directory+ "/views/" + file_name + ".html" , "w+")
        data = file.readlines() 
        file.close()
        return data

    def loadJS(this, window, file_name: str) -> str:     
        file = open(this.root_directory+ "/js/" + file_name + ".html" , "w+")
        data = file.readlines()
        file.close()
        window.evaluate_js(data)
        return data
