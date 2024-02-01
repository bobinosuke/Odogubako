import customtkinter as ctk
import Downloader
import Converter
import DataPrep
import classification  

class MainUI:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.standard_font = ("Yu Gothic UI")
        
        downloader_tab = self.tabview.add("ダウンローダー")
        dataprep_tab = self.tabview.add("匿名化&識別子振り分け")
        converter_tab = self.tabview.add("コンバーター")
        classification_tab = self.tabview.add("BGMの有無を検出")  
        
        self.downloader = Downloader.Downloader(self)
        self.converter = Converter.Converter(self)
        self.dataprep = DataPrep.DataPrep(self)
        self.classifier = classification.Classifier(self)  
        
        self.downloader.setup_ui(downloader_tab)
        self.converter.setup_ui(converter_tab)
        self.dataprep.setup_ui(dataprep_tab)
        self.classifier.setup_ui(classification_tab)  

    def setup_ui(self):
        self.tabview = ctk.CTkTabview(master=self.root)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

# アプリケーションの実行
root = ctk.CTk()
root.title("Odogubako")  
root.minsize(500, 500)

ui = MainUI(root)

root.mainloop()