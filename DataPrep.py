import customtkinter as ctk
from tkinter import filedialog
import os
import uuid


class DataPrep:
    def __init__(self, main_ui):
        self.main_ui = main_ui

    def setup_ui(self, tab_frame):
        self.standard_font = ("Segoe UI")
        # 最初のテキストボックス用のフレームを作成し、高さを大きく設定
        frame1 = ctk.CTkFrame(tab_frame)
        frame1.pack(padx=20, pady=10, fill="both")
        self.info_text_box1 = ctk.CTkTextbox(frame1, height=310, state='disabled')
        self.info_text_box1.pack(fill="both", expand=True)
        self.insert_text(self.info_text_box1, "実行前\n\n選択フォルダ/\n    ├ キャラクター01/\n    │   ├ hogehoge.wav\n    │   └ fugaguga.wav\n"
                        "    └ キャラクター02/\n          ├ hogehoge.wav\n          └ fugaguga.wav\n\n"
                        "実行後\n\n選択フォルダ/\n    ├ {uuid1}/\n    │   ├ {uuid1}_0001.wav\n    │   └ {uuid1}_0002.wav\n"
                        "    └ {uuid2}/\n          ├ {uuid2}_0001.wav\n          └ {uuid2}_0002.wav")

        # 2番目のテキストボックス用のフレームを作成し、高さを小さく設定
        frame2 = ctk.CTkFrame(tab_frame)
        frame2.pack(padx=10, pady=20, fill="both")
        self.info_text_box2 = ctk.CTkTextbox(frame2, height=150, state='disabled')
        self.info_text_box2.pack(fill="both", expand=True)
        self.insert_text(self.info_text_box2, "変換前にフォルダ構造と選択フォルダが正しいかチェックすること\n\n"
                        "事故防止のため選択フォルダ内にwavファイル以外のファイルが含まれている場合警告を出します。"
                        "その場合、ターミナルでYを入力するまで処理を開始しません。\n\n"
                        "選択フォルダーのPathが表示されるので正しいものを選んでいるか確認してください")

        self.select_folder_button = ctk.CTkButton(tab_frame, text="フォルダを選択", command=self.select_folder)
        self.select_folder_button.pack(padx=20, pady=(10, 20))

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.rename_subfolders_and_files(folder_path)

    def insert_text(self, text_box, text):
        text_box.configure(state='normal')
        text_box.insert('end', text)
        text_box.configure(state='disabled')

    def rename_subfolders_and_files(self, folder_path):
        non_wav_files_found = False
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not file.endswith('.wav'):
                    non_wav_files_found = True
                    break

        if non_wav_files_found:
            print(f"警告: あなたが変換しようとしているフォルダは{folder_path}です。本当に変換しますか？ Y/N")
            user_input = input()
            if user_input.lower() != 'y':
                print("処理を中止しました。")
                return

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
