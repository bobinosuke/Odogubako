import subprocess
from tkinter import messagebox, filedialog
import customtkinter as ctk

class Downloader:
    def __init__(self, main_ui):
        self.main_ui = main_ui

    def download_video(self):
        url = self.url_entry.get()
        selected_format = self.search_format_var.get()
        directory = filedialog.askdirectory(title='ダウンロード先を指定')
        if directory:
            if selected_format == "default":
                command = f'yt-dlp -f best -o "{directory}/%(title)s.%(ext)s" {url}'
            else:
                command = f'yt-dlp -f bestaudio --extract-audio --audio-format {selected_format} -o "{directory}/%(title)s.%(ext)s" {url}'
            subprocess.call(command, shell=True)
            messagebox.showinfo("成功", "ダウンロードが完了しました")
        else:
            messagebox.showwarning("警告", "ダウンロード先が指定されていません")

    def download_top_search_result(self):
        search_keyword = self.search_entry.get()
        selected_format = self.search_format_var.get()
        top_count = self.get_slider_value()  # スライダーの値を取得
        directory = filedialog.askdirectory(title='ダウンロード先を指定')
        if search_keyword and directory and top_count > 0:
            if selected_format == "default":
                command = f'yt-dlp -f best -o "{directory}/%(title)s.%(ext)s" "ytsearch{top_count}:{search_keyword}"'
            else:
                command = f'yt-dlp -f bestaudio --extract-audio --audio-format {selected_format} -o "{directory}/%(title)s.%(ext)s" "ytsearch{top_count}:{search_keyword}"'
            subprocess.call(command, shell=True)
            messagebox.showinfo("成功", f"検索結果のトップ{top_count}動画を{selected_format}形式でダウンロードが完了しました: {directory}")
        else:
            if not search_keyword:
                messagebox.showwarning("警告", "検索キーワードが入力されていません")
            if not directory:
                messagebox.showwarning("警告", "ダウンロード先が指定されていません")

    def setup_ui(self, tab_frame):
        self.search_format_var = ctk.StringVar(value="wav")  # Changed the initial value to "wav"
        self.top_count_var = ctk.StringVar(value="1")

        self.setup_downloader_tab(tab_frame)

    def setup_downloader_tab(self, tab_frame):
            search_label = ctk.CTkLabel(tab_frame, text="フォーマット形式:")
            search_label.pack(pady=(20, 0))

            search_formats = ["default", "wav", "mp3",]
            search_format_menu = ctk.CTkOptionMenu(tab_frame, variable=self.search_format_var, values=search_formats)
            search_format_menu.pack(pady=(0, 10))

            url_label = ctk.CTkLabel(tab_frame, text="URL (yt-dlpで対応しているサイトのみ)")
            url_label.pack(pady=(0, 0))

            self.url_entry = ctk.CTkEntry(tab_frame, width=400)
            self.url_entry.pack(pady=(0, 10))

            download_button = ctk.CTkButton(tab_frame, text="ダウンロード", command=self.download_video)
            download_button.pack(pady=(5, 10))

            search_label = ctk.CTkLabel(tab_frame, text="キーワード検索  例: 〇〇 同時視聴")
            search_label.pack(pady=(10, 0))

            self.search_entry = ctk.CTkEntry(tab_frame, width=400)
            self.search_entry.pack(pady=(0, 10))

            search_button = ctk.CTkButton(tab_frame, text="検索してダウンロード", command=self.download_top_search_result)
            search_button.pack(pady=(5, 10))

            top_count_label = ctk.CTkLabel(tab_frame, text="キーワード検索でダウンロードするファイルの数:")
            top_count_label.pack(pady=(10, 0))
            self.top_count_slider = ctk.CTkSlider(tab_frame, from_=1, to=10, number_of_steps=9)
            self.top_count_slider.set(1)  # スライダーの初期値を1に設定
            self.top_count_slider.pack(pady=(10, 10))
            self.top_count_value_label = ctk.CTkLabel(tab_frame, text="選択値: 1")
            self.top_count_value_label.pack(pady=(0, 10))
            self.top_count_slider.configure(command=self.update_slider_value_label)
    
    def update_slider_value_label(self, value):
        self.top_count_value_label.configure(text=f"選択値: {int(float(value))}")
    
    def get_slider_value(self):
        return int(self.top_count_slider.get())
    