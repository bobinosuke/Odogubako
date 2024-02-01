import os
import numpy as np
import librosa
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import customtkinter as ctk
from tkinter import filedialog

class Classifier:
    def __init__(self, main_ui):
        self.main_ui = main_ui
        self.input_dir = None
        self.output_dir = None
        self.model = load_model('speech_classification_model.h5')
        self.input_dir_label = None
        self.output_dir_label = None

    def setup_ui(self, tab_frame):
        self.standard_font = ("Segoe UI")
    
        frame1 = ctk.CTkFrame(tab_frame)
        frame1.pack(padx=20, pady=10, fill="both")
        self.info_text_box1 = ctk.CTkTextbox(frame1, height=150, state='disabled')
        self.info_text_box1.pack(fill="both", expand=True)
        self.insert_text(self.info_text_box1, "発話時のBGMの有無を分類し、speechとspeech_withBGMの2つのフォルダに仕分けるプログラムです\n\n"
                        "入力ディレクトリにBGMの有無を仕分けたいwavファイルを入れてください(事前にVADで発話部分だけ2-12秒程度に切り出してください)\n\n"
                        "出力ディレクトリにはspeechとspeech_withBGMフォルダが自動生成されそのなかに仕分けられたwavが入ります")

        # 入力ディレクトリ選択ボタン
        input_dir_button = ctk.CTkButton(tab_frame, text="入力ディレクトリを選択", command=self.select_input_dir)
        input_dir_button.pack(pady=(10, 5))
        # 入力ディレクトリ表示ラベル
        self.input_dir_label = ctk.CTkLabel(tab_frame, text="選択された入力ディレクトリ: なし")
        self.input_dir_label.pack(pady=(0, 20))
        
        # 出力ディレクトリ選択ボタン
        output_dir_button = ctk.CTkButton(tab_frame, text="出力ディレクトリを選択", command=self.select_output_dir)
        output_dir_button.pack(pady=(0, 5))
        # 出力ディレクトリ表示ラベル
        self.output_dir_label = ctk.CTkLabel(tab_frame, text="選択された出力ディレクトリ: なし")
        self.output_dir_label.pack(pady=(0, 20))
        
        # ファイル分類開始ボタン
        classify_button = ctk.CTkButton(tab_frame, text="ファイルを分類", command=self.classify_files)
        classify_button.pack(pady=(0, 20))

    def insert_text(self, text_box, text):
        text_box.configure(state='normal')
        text_box.insert('end', text)
        text_box.configure(state='disabled')

    def select_input_dir(self):
        self.input_dir = filedialog.askdirectory(title="入力ディレクトリを選択")
        if self.input_dir:  # ディレクトリが選択された場合のみ更新
            self.input_dir_label.configure(text=f"選択された入力ディレクトリ: {self.input_dir}")
        else:
            self.input_dir_label.configure(text="選択された入力ディレクトリ: なし")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title="出力ディレクトリを選択")
        if self.output_dir:  # ディレクトリが選択された場合のみ更新
            self.output_dir_label.configure(text=f"選択された出力ディレクトリ: {self.output_dir}")
        else:
            self.output_dir_label.configure(text="選択された出力ディレクトリ: なし")

    def preprocess_file(self, file_path, n_mels=128, max_pad_len=32):
        signal, sr = librosa.load(file_path, sr=None)
        mel = librosa.feature.melspectrogram(y=signal, sr=sr, n_mels=n_mels)
        mel_db = librosa.power_to_db(mel, ref=np.max)
        zcr = librosa.feature.zero_crossing_rate(signal)[0]

        # パディング処理
        mel_db_padded = pad_sequences([mel_db.T], maxlen=max_pad_len, dtype='float32', padding='post', truncating='post', value=0)
        zcr_padded = pad_sequences([zcr.reshape(-1, 1)], maxlen=max_pad_len, dtype='float32', padding='post', truncating='post', value=0)

        # 正規化処理
        mel_db_padded = (mel_db_padded - np.min(mel_db_padded)) / (np.max(mel_db_padded) - np.min(mel_db_padded))
        zcr_padded = (zcr_padded - np.min(zcr_padded)) / (np.max(zcr_padded) - np.min(zcr_padded))

        return mel_db_padded[0], zcr_padded[0]

    def classify_files(self):
        if not self.input_dir or not self.output_dir:
            print("入力ディレクトリまたは出力ディレクトリが選択されていません。")
            return
        print("ファイルの分類を開始します。")

        speech_dir = os.path.join(self.output_dir, 'speech')
        speech_withBGM_dir = os.path.join(self.output_dir, 'speech_withBGM')

        os.makedirs(speech_dir, exist_ok=True)
        os.makedirs(speech_withBGM_dir, exist_ok=True)

        for filename in os.listdir(self.input_dir):
            if filename.endswith('.wav'):
                file_path = os.path.join(self.input_dir, filename)
                X_mel, X_zcr = self.preprocess_file(file_path)
                # バッチ次元を追加
                X_mel = np.expand_dims(X_mel, axis=0)  
                X_zcr = np.expand_dims(X_zcr, axis=0)  
                prediction = self.model.predict([X_mel, X_zcr])
                predicted_label = np.argmax(prediction, axis=1)[0]
                print(f"{filename} は {predicted_label} に分類されました")

                # 予測されたラベルに基づいてファイルを移動
                if predicted_label == 0:
                    destination = speech_dir
                else:
                    destination = speech_withBGM_dir
                os.rename(file_path, os.path.join(destination, filename))

                print(f"{filename} を {destination} に移動しました。")
            else:
                print(f"{filename} は.wavファイルではないためスキップされました。")

        print("ファイルの仕分けが完了しました。")
