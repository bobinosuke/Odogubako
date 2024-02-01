from tkinter import messagebox, filedialog
import ffmpeg
import customtkinter as ctk
import os

FONT_TYPE = "meiryo"

class Converter:
    def __init__(self, main_ui):
        self.main_ui = main_ui

    def select_file(self):
        # 選択された入力フォーマットに基づいてファイルタイプを制限する
        selected_format = self.input_format_combobox.get()
        filetypes = [(f'{selected_format} ファイル', f'*.{selected_format}')]
        filename = filedialog.askopenfilename(
            title='変換するファイルを選択',
            initialdir='./downloads',
            filetypes=filetypes
        )
        return filename

    def convert_file(self, file_path, output_format):
        output_path = file_path.rsplit(".", 1)[0] + f'.{output_format}'
        try:
            # ffmpeg-pythonを使用してファイルを変換
            ffmpeg.input(file_path).output(output_path).run(overwrite_output=True)
            messagebox.showinfo("成功", f"ファイルの変換が完了しました: {output_path}")
        except ffmpeg.Error as e:
            messagebox.showerror("エラー", f"変換中にエラーが発生しました: {e.stderr.decode()}")

    def convert(self):
        file_path = self.select_file()  
        if file_path:
            output_format = self.format_combobox.get()
            self.convert_file(file_path, output_format)

    def convert_folder(self):
        folder_path = filedialog.askdirectory(
            title='変換するフォルダを選択'
        )
        if folder_path:
            output_format = self.format_combobox.get()
            input_format = self.input_format_combobox.get()
            for file in os.listdir(folder_path):
                if file.endswith(f'.{input_format}'):
                    file_path = os.path.join(folder_path, file)
                    self.convert_file(file_path, output_format)

    def setup_ui(self, tab_frame):
        self.format_var = ctk.StringVar(value="wav")
        self.setup_converter_tab(tab_frame)

    def setup_converter_tab(self, tab_frame):
        self.fonts = (FONT_TYPE)
        
        input_format_label = ctk.CTkLabel(tab_frame, text="変換前のフォーマットを入力または選択:", font=self.fonts)
        input_format_label.pack(pady=(10, 0))
        
        self.input_format_combobox = ctk.CTkComboBox(tab_frame, values=["wav", "mp3", "ogg", "flac", "mp4", "avi"])
        self.input_format_combobox.pack(pady=(0, 10))

        url_label = ctk.CTkLabel(tab_frame, text="変換後のフォーマットを入力または選択:", font=self.fonts)
        url_label.pack(pady=(10, 0))
        
        self.format_combobox = ctk.CTkComboBox(tab_frame, values=["wav", "mp3", "ogg", "flac", "mp4", "avi"])
        self.format_combobox.pack(pady=(0, 10))

        url_label = ctk.CTkLabel(tab_frame, text="変換したいファイルを選択:", font=self.fonts)
        url_label.pack(pady=(10, 0))

        convert_button = ctk.CTkButton(tab_frame, text="ファイルを選択", command=self.convert, font=self.fonts)
        convert_button.pack(pady=(0, 10))

        url_label = ctk.CTkLabel(tab_frame, text="変換したいフォルダを選択:", font=self.fonts)
        url_label.pack(pady=(10, 0))

        convert_folder_button = ctk.CTkButton(tab_frame, text="フォルダを選択", command=self.convert_folder, font=self.fonts)
        convert_folder_button.pack(pady=(0, 20))
