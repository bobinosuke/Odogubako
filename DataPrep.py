import customtkinter as ctk
from tkinter import filedialog
import os
import uuid


class DataPrep:
    def __init__(self, main_ui):
        self.main_ui = main_ui

    def setup_ui(self, tab_frame):
        self.info_text_box = ctk.CTkTextbox(tab_frame, height=4, state='disabled')
        self.info_text_box.pack(padx=20, pady=20, fill="both", expand=True)


        self.insert_text("実行前\n\n選択フォルダ/\n    ├ キャラクター01/\n    │   ├ hogehoge.wav\n    │   └ fugaguga.wav\n"
                        "    └ キャラクター02/\n          ├ hogehoge.wav\n          └ fugaguga.wav\n\n"
                        "実行後\n\n選択フォルダ/\n    ├ {uuid1}/\n    │   ├ {uuid1}_0001.wav\n    │   └ {uuid1}_0002.wav\n"
                        "    └ {uuid2}/\n          ├ {uuid2}_0001.wav\n          └ {uuid2}_0002.wav")

        self.info_label = ctk.CTkLabel(tab_frame, text="変換前にフォルダ構造と選択フォルダが正しいかチェックすること")
        self.info_label.pack(padx=20, pady=(10, 0))

        self.select_folder_button = ctk.CTkButton(tab_frame, text="フォルダを選択", command=self.select_folder)
        self.select_folder_button.pack(padx=20, pady=(10, 20))

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.rename_subfolders_and_files(folder_path)

    def insert_text(self, text):
        self.info_text_box.configure(state='normal')
        self.info_text_box.insert('end', text)
        self.info_text_box.configure(state='disabled')

    def rename_subfolders_and_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for subdir in dirs:
                new_name = uuid.uuid4().hex[:8]
                original_subdir_path = os.path.join(root, subdir)
                new_subdir_path = os.path.join(root, new_name)
                os.rename(original_subdir_path, new_subdir_path)
                for count, filename in enumerate(os.listdir(new_subdir_path), start=1):
                    if filename.endswith('.wav'):
                        new_filename = f"{new_name}_{count:04}.wav"  # Changed count to 4 digits
                        original_file_path = os.path.join(new_subdir_path, filename)
                        new_file_path = os.path.join(new_subdir_path, new_filename)
                        os.rename(original_file_path, new_file_path)
                print(f"Renamed {subdir} to {new_name} and its files accordingly.")
