import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSlider, QPushButton, QLabel, QSpinBox, QComboBox,
                             QFileDialog, QCheckBox, QGroupBox, QDialog, QScrollArea, QListWidget)
from PyQt5.QtCore import (Qt, QTimer, QPoint, QThread, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import QPalette, QColor, QFont
import pyaudio
import numpy as np
import pygame
import wave
import struct
import threading
import time

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("设置")
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 680)
        self.update_dialog_style()
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("⚙️ 设置")
        title.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00d9ff;")
        main_layout.addWidget(title)
        
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题")
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['暗色', '浅色'])
        self.theme_combo.currentIndexChanged.connect(parent.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        main_layout.addLayout(theme_layout)
        
        transparency_layout = QVBoxLayout()
        transparency_label = QLabel("透明度")
        transparency_layout.addWidget(transparency_label)
        
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(30, 100)
        self.transparency_slider.setValue(int(parent.transparency * 100))
        self.transparency_slider.setFixedHeight(50)
        self.transparency_slider.valueChanged.connect(parent.on_transparency_changed)
        transparency_layout.addWidget(self.transparency_slider)
        main_layout.addLayout(transparency_layout)
        
        playlist_label = QLabel("播放列表")
        main_layout.addWidget(playlist_label)
        
        self.playlist = QListWidget()
        self.playlist.setFixedHeight(200)
        self.playlist.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.playlist.itemClicked.connect(parent.on_playlist_item_clicked)
        main_layout.addWidget(self.playlist)
        
        playlist_btn_layout = QHBoxLayout()
        playlist_btn_layout.setSpacing(10)
        
        self.add_btn = QPushButton("➕ 添加音乐")
        self.add_btn.setFixedHeight(40)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 217, 255, 0.3);
                border: 2px solid rgba(0, 217, 255, 0.5);
                border-radius: 8px;
                font-family: "Microsoft YaHei";
                font-size: 13px;
                color: #00d9ff;
            }
            QPushButton:hover {
                background: rgba(0, 217, 255, 0.5);
            }
        """)
        self.add_btn.clicked.connect(parent.add_music_to_playlist)
        playlist_btn_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("🗑️ 移除")
        self.remove_btn.setFixedHeight(40)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 100, 100, 0.3);
                border: 2px solid rgba(255, 100, 100, 0.5);
                border-radius: 8px;
                font-family: "Microsoft YaHei";
                font-size: 13px;
                color: #ff6464;
            }
            QPushButton:hover {
                background: rgba(255, 100, 100, 0.5);
            }
        """)
        self.remove_btn.clicked.connect(parent.remove_from_playlist)
        playlist_btn_layout.addWidget(self.remove_btn)
        
        main_layout.addLayout(playlist_btn_layout)
        
        volume_label = QLabel("音乐音量")
        volume_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 15px;")
        main_layout.addWidget(volume_label)
        
        self.bg_volume_slider = QSlider(Qt.Horizontal)
        self.bg_volume_slider.setRange(0, 100)
        self.bg_volume_slider.setValue(int(parent.bg_player.get_volume() * 100))
        self.bg_volume_slider.setFixedHeight(50)
        self.bg_volume_slider.valueChanged.connect(parent.on_bg_volume_changed)
        main_layout.addWidget(self.bg_volume_slider)
        
        play_layout = QHBoxLayout()
        play_layout.setSpacing(15)
        self.bg_play_btn = QPushButton("▶ 播放")
        self.bg_play_btn.setFixedHeight(45)
        self.bg_play_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 100, 0.3);
                border: 2px solid rgba(0, 255, 100, 0.5);
                border-radius: 8px;
                font-family: "Microsoft YaHei";
                font-size: 14px;
                color: #00ff64;
            }
        """)
        self.bg_play_btn.clicked.connect(parent.toggle_bg_play)
        play_layout.addWidget(self.bg_play_btn)
        
        self.bg_stop_btn = QPushButton("■ 停止")
        self.bg_stop_btn.setFixedHeight(45)
        self.bg_stop_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 100, 100, 0.3);
                border: 2px solid rgba(255, 100, 100, 0.5);
                border-radius: 8px;
                font-family: "Microsoft YaHei";
                font-size: 14px;
                color: #ff6464;
            }
        """)
        self.bg_stop_btn.clicked.connect(parent.stop_bg_music)
        play_layout.addWidget(self.bg_stop_btn)
        main_layout.addLayout(play_layout)
        
        self.close_btn = QPushButton("关闭")
        self.close_btn.setFixedHeight(45)
        self.close_btn.clicked.connect(self.close)
        self.update_close_button_style(self.close_btn)
        main_layout.addWidget(self.close_btn)
    
    def apply_initial_styles(self):
        self.update_label_styles()
        self.update_combo_style(self.theme_combo)
        self.update_playlist_style()
        self.update_button_styles()
    
    def update_all_styles(self):
        self.update_dialog_style()
        self.update_label_styles()
        self.update_combo_style(self.theme_combo)
        self.update_playlist_style()
        self.update_button_styles()
        self.update_close_button_style(self.close_btn)
    
    def update_label_styles(self):
        labels = self.findChildren(QLabel)
        for label in labels:
            if label.text() == "⚙️ 设置":
                if self.parent and self.parent.theme == 'dark':
                    label.setStyleSheet("color: #00d9ff;")
                else:
                    label.setStyleSheet("color: #059669;")
            else:
                if self.parent and self.parent.theme == 'dark':
                    label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 15px;")
                else:
                    label.setStyleSheet("color: rgba(31, 41, 55, 0.95); font-family: 'Microsoft YaHei'; font-size: 15px;")
    
    def update_combo_style(self, combo):
        if self.parent and self.parent.theme == 'dark':
            combo.setStyleSheet("""
                QComboBox {
                    background: rgba(26, 26, 46, 0.95);
                    border: 2px solid rgba(0, 217, 255, 0.5);
                    border-radius: 6px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    padding: 6px;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 25px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid rgba(0, 217, 255, 0.8);
                    margin-right: 8px;
                }
                QComboBox QAbstractItemView {
                    background: rgba(26, 26, 46, 0.98);
                    border: 2px solid rgba(0, 217, 255, 0.5);
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    selection-background-color: rgba(123, 44, 191, 0.5);
                    padding: 3px;
                }
            """)
        else:
            combo.setStyleSheet("""
                QComboBox {
                    background: rgba(243, 244, 246, 0.95);
                    border: 2px solid rgba(16, 185, 129, 0.4);
                    border-radius: 6px;
                    color: #1f2937;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    padding: 6px;
                    min-height: 20px;
                }
                QComboBox::drop-down {
                    border: none;
                    width: 25px;
                }
                QComboBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 6px solid rgba(16, 185, 129, 0.8);
                    margin-right: 8px;
                }
                QComboBox QAbstractItemView {
                    background: rgba(243, 244, 246, 0.98);
                    border: 2px solid rgba(16, 185, 129, 0.4);
                    color: #1f2937;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    selection-background-color: rgba(34, 197, 94, 0.3);
                    padding: 3px;
                }
            """)
    
    def update_playlist_style(self):
        if self.parent and self.parent.theme == 'dark':
            self.playlist.setStyleSheet("""
                QListWidget {
                    background: rgba(26, 26, 46, 0.95);
                    border: 2px solid rgba(0, 217, 255, 0.3);
                    border-radius: 8px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    padding: 5px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }
                QListWidget::item:selected {
                    background: rgba(123, 44, 191, 0.4);
                    color: #00d9ff;
                }
                QListWidget::item:hover {
                    background: rgba(123, 44, 191, 0.2);
                }
                QListWidget::verticalScrollBar {
                    width: 10px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 5px;
                }
                QListWidget::verticalScrollBar::handle {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border-radius: 5px;
                    min-height: 20px;
                }
                QListWidget::verticalScrollBar::handle:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #9b4cdf, stop:1 #20e9ff);
                }
                QListWidget::verticalScrollBar::add-page, QListWidget::verticalScrollBar::sub-page {
                    background: rgba(255, 255, 255, 0.05);
                }
            """)
        else:
            self.playlist.setStyleSheet("""
                QListWidget {
                    background: rgba(243, 244, 246, 0.95);
                    border: 2px solid rgba(16, 185, 129, 0.3);
                    border-radius: 8px;
                    color: #1f2937;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    padding: 5px;
                }
                QListWidget::item {
                    padding: 8px;
                    border-bottom: 1px solid rgba(31, 41, 55, 0.08);
                }
                QListWidget::item:selected {
                    background: rgba(34, 197, 94, 0.35);
                    color: #059669;
                }
                QListWidget::item:hover {
                    background: rgba(34, 197, 94, 0.2);
                }
                QListWidget::verticalScrollBar {
                    width: 10px;
                    background: rgba(31, 41, 55, 0.08);
                    border-radius: 5px;
                }
                QListWidget::verticalScrollBar::handle {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 5px;
                    min-height: 20px;
                }
                QListWidget::verticalScrollBar::handle:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #059669, stop:1 #0891b2);
                }
                QListWidget::verticalScrollBar::add-page, QListWidget::verticalScrollBar::sub-page {
                    background: rgba(31, 41, 55, 0.03);
                }
            """)
    
    def update_button_styles(self):
        if self.parent and self.parent.theme == 'dark':
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 217, 255, 0.3);
                    border: 2px solid rgba(0, 217, 255, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    color: #00d9ff;
                }
                QPushButton:hover {
                    background: rgba(0, 217, 255, 0.5);
                }
            """)
            self.remove_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 100, 100, 0.3);
                    border: 2px solid rgba(255, 100, 100, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    color: #ff6464;
                }
                QPushButton:hover {
                    background: rgba(255, 100, 100, 0.5);
                }
            """)
            self.bg_play_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 255, 100, 0.3);
                    border: 2px solid rgba(0, 255, 100, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    color: #00ff64;
                }
            """)
            self.bg_stop_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 100, 100, 0.3);
                    border: 2px solid rgba(255, 100, 100, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    color: #ff6464;
                }
            """)
        else:
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(16, 185, 129, 0.15);
                    border: 2px solid rgba(16, 185, 129, 0.4);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    color: #059669;
                }
                QPushButton:hover {
                    background: rgba(16, 185, 129, 0.3);
                }
            """)
            self.remove_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 68, 68, 0.2);
                    border: 2px solid rgba(239, 68, 68, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 13px;
                    color: #ef4444;
                }
                QPushButton:hover {
                    background: rgba(239, 68, 68, 0.4);
                }
            """)
            self.bg_play_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(34, 197, 94, 0.2);
                    border: 2px solid rgba(34, 197, 94, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    color: #22c55e;
                }
            """)
            self.bg_stop_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(239, 68, 68, 0.2);
                    border: 2px solid rgba(239, 68, 68, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    color: #ef4444;
                }
            """)
    
    def update_dialog_style(self):
        if self.parent and self.parent.theme == 'dark':
            self.setStyleSheet("""
                QDialog {
                    background: rgba(26, 26, 46, 0.98);
                    border: 2px solid rgba(0, 217, 255, 0.5);
                    border-radius: 15px;
                }
                QSlider::groove:horizontal {
                    height: 10px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 5px;
                    margin: 5px 0;
                }
                QSlider::handle:horizontal {
                    width: 28px;
                    height: 28px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border-radius: 14px;
                    margin: -9px 0;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border-radius: 5px;
                    margin: 5px 0;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background: rgba(243, 244, 246, 0.98);
                    border: 2px solid rgba(16, 185, 129, 0.4);
                    border-radius: 15px;
                }
                QSlider::groove:horizontal {
                    height: 10px;
                    background: rgba(31, 41, 55, 0.1);
                    border-radius: 5px;
                    margin: 5px 0;
                }
                QSlider::handle:horizontal {
                    width: 28px;
                    height: 28px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 14px;
                    margin: -9px 0;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 5px;
                    margin: 5px 0;
                }
            """)
    
    def update_close_button_style(self, btn):
        if self.parent and self.parent.theme == 'dark':
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border: none;
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 15px;
                    color: white;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border: none;
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 15px;
                    color: white;
                }
            """)

class AudioPlayer(QThread):
    tick = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.bpm = 120
        self.volume = 0.7
        self.beat_count = 0
        self.beats_per_measure = 4
        self.click_type = 'electronic'
        self.accent_type = 'strong'
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.current_click_data = None
        self.current_accent_data = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_beat)
        
        self.generate_all_sounds()
    
    def generate_all_sounds(self):
        self.click_sounds = {}
        click_types = ['electronic', 'woodblock', 'beep']
        frequencies = {
            'electronic': (880, 660),
            'woodblock': (600, 400),
            'beep': (1000, 800)
        }
        
        for click_type in click_types:
            freq_accent, freq_normal = frequencies[click_type]
            accent_data = self.generate_click_data(freq_accent, 0.15, click_type, True)
            normal_data = self.generate_click_data(freq_normal, 0.08, click_type, False)
            self.click_sounds[click_type] = (accent_data, normal_data)
    
    def generate_click_data(self, frequency, duration, click_type='electronic', is_accent=False):
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), dtype=np.float32)
        
        if click_type == 'electronic':
            envelope = np.exp(-t * 15)
            wave_data = np.sin(2 * np.pi * frequency * t) * envelope
        elif click_type == 'woodblock':
            envelope = np.exp(-t * 8)
            wave_data = np.sin(2 * np.pi * frequency * t) * envelope * (1 + 0.3 * np.sin(2 * np.pi * frequency * 3 * t))
        elif click_type == 'metallic':
            envelope = np.exp(-t * 20)
            wave_data = np.sin(2 * np.pi * frequency * t) * envelope + \
                        0.5 * np.sin(2 * np.pi * frequency * 2 * t) * envelope
        elif click_type == 'beep':
            envelope = np.where(t < 0.02, 1, np.exp(-(t - 0.02) * 50))
            wave_data = np.sin(2 * np.pi * frequency * t) * envelope
        elif click_type == 'drum':
            noise = np.random.normal(0, 1, len(t))
            envelope = np.exp(-t * 20)
            wave_data = (noise * envelope * 0.5 + np.sin(2 * np.pi * 100 * t) * envelope * 0.5)
        elif click_type == 'tick':
            envelope = np.exp(-t * 30)
            wave_data = (np.sin(2 * np.pi * frequency * 2 * t) * envelope + 
                        np.sin(2 * np.pi * frequency * t) * envelope * 0.5)
        elif click_type == 'click':
            envelope = np.exp(-t * 25)
            wave_data = np.sin(2 * np.pi * frequency * 1.5 * t) * envelope
        else:
            envelope = np.exp(-t * 10)
            wave_data = np.sin(2 * np.pi * frequency * t) * envelope
        
        if is_accent:
            wave_data = wave_data * 1.3
        
        wave_data = wave_data * self.volume
        return (wave_data * 32767).astype(np.int16).tobytes()
    
    def set_bpm(self, bpm):
        self.bpm = bpm
        if self.is_playing:
            interval = int(60000 / bpm)
            self.timer.setInterval(interval)
    
    def set_volume(self, volume):
        self.volume = volume
        self.generate_all_sounds()
    
    def set_beats_per_measure(self, beats):
        self.beats_per_measure = beats
        if self.beat_count >= beats:
            self.beat_count = 0
    
    def set_click_type(self, click_type):
        self.click_type = click_type
    
    def init_stream(self):
        if self.stream is None or not self.stream.is_active():
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True
            )
    
    def play_beat(self):
        try:
            self.init_stream()
            
            accent_data, normal_data = self.click_sounds[self.click_type]
            
            if self.beat_count == 0:
                self.stream.write(accent_data)
            else:
                self.stream.write(normal_data)
            
            self.tick.emit(self.beat_count)
            self.beat_count = (self.beat_count + 1) % self.beats_per_measure
        except Exception as e:
            print(f"播放错误: {e}")
            if self.stream:
                try:
                    self.stream.close()
                except:
                    pass
            self.stream = None
    
    def start_playing(self):
        self.is_playing = True
        self.beat_count = 0
        interval = int(60000 / self.bpm)
        self.timer.setInterval(interval)
        self.init_stream()
        self.timer.start()
    
    def stop_playing(self):
        self.is_playing = False
        self.timer.stop()
        if self.stream:
            try:
                self.stream.stop_stream()
            except:
                pass
    
    def quit(self):
        self.timer.stop()
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
        self.audio.terminate()
        super().quit()

class BackgroundMusicPlayer:
    def __init__(self):
        pygame.mixer.init(frequency=44100)
        self.is_playing = False
        self.volume = 0.3
        self.playlist = []
        self.current_index = -1
    
    def add_to_playlist(self, file_paths):
        for file_path in file_paths:
            if os.path.exists(file_path):
                self.playlist.append(file_path)
        return len(file_paths) > 0
    
    def remove_from_playlist(self, index):
        if 0 <= index < len(self.playlist):
            removed = self.playlist.pop(index)
            if self.current_index == index:
                self.current_index = -1
                self.stop()
            elif self.current_index > index:
                self.current_index -= 1
            return removed
        return None
    
    def clear_playlist(self):
        self.playlist.clear()
        self.current_index = -1
        self.stop()
    
    def get_current_track(self):
        if 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None
    
    def play_next(self):
        if len(self.playlist) > 0:
            if self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                self.current_index = 0
            return self.play_index(self.current_index)
        return False
    
    def play_index(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            try:
                pygame.mixer.music.load(self.playlist[index])
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)
                self.is_playing = True
                return True
            except Exception as e:
                print(f"播放失败: {e}")
                return False
        return False
    
    def play(self):
        if len(self.playlist) > 0:
            if self.current_index < 0:
                self.current_index = 0
            return self.play_index(self.current_index)
        return False
    
    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def unpause(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
    
    def get_volume(self):
        return self.volume
    
    def quit(self):
        pygame.mixer.quit()

class MetronomeWindow(QMainWindow):
    music_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("节拍器")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.transparency = 0.9
        self.dragging = False
        self.drag_pos = QPoint()
        self.max_beat_indicators = 6
        self.settings_dialog = None
        self.last_music_dir = self.load_last_music_dir()
        self.theme = 'dark'
        
        self.audio_player = AudioPlayer()
        self.audio_player.tick.connect(self.update_beat_indicator)
        
        self.bg_player = BackgroundMusicPlayer()
        
        self.init_ui()
        self.update_window_size()
    
    def init_ui(self):
        central_widget = QWidget()
        self.update_widget_style(central_widget)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 12, 15, 12)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(36, 36)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 100, 100, 0.3);
                border-radius: 50%;
                font-family: "Microsoft YaHei";
                font-size: 16px;
                color: white;
            }
            QPushButton:hover {
                background: rgba(255, 100, 100, 0.6);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(36, 36)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(123, 44, 191, 0.3);
                border-radius: 50%;
                font-family: "Microsoft YaHei";
                font-size: 18px;
                color: white;
            }
            QPushButton:hover {
                background: rgba(123, 44, 191, 0.6);
            }
        """)
        settings_btn.clicked.connect(self.show_settings)
        
        title_label = QLabel("🎵 节拍器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Microsoft YaHei', 15, QFont.Bold))
        title_label.setStyleSheet("color: #00d9ff;")
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(settings_btn)
        header_layout.addWidget(close_btn)
        main_layout.addLayout(header_layout)
        
        self.music_label = QLabel("♪ 未播放音乐")
        self.music_label.setAlignment(Qt.AlignCenter)
        self.music_label.setFont(QFont('Microsoft YaHei', 12))
        self.music_label.setStyleSheet("color: rgba(0, 217, 255, 0.8);")
        self.music_label.setFixedHeight(40)
        main_layout.addWidget(self.music_label)
        
        self.bpm_display = QLabel("120")
        self.bpm_display.setAlignment(Qt.AlignCenter)
        self.bpm_display.setFont(QFont('Microsoft YaHei', 56, QFont.Bold))
        self.bpm_display.setStyleSheet("color: white;")
        main_layout.addWidget(self.bpm_display)
        
        self.beat_indicators = []
        self.preset_buttons = []
        self.beat_layout = QHBoxLayout()
        self.beat_layout.setSpacing(8)
        self.beat_layout.setAlignment(Qt.AlignCenter)
        for i in range(self.max_beat_indicators):
            indicator = QLabel()
            indicator.setFixedSize(9, 6)
            indicator.setStyleSheet("background: rgba(123, 44, 191, 0.5); border-radius: 3px;")
            self.beat_indicators.append(indicator)
            self.beat_layout.addWidget(indicator)
        main_layout.addLayout(self.beat_layout)
        main_layout.addSpacing(8)
        
        bpm_layout = QHBoxLayout()
        bpm_label = QLabel("BPM")
        bpm_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 16px;")
        self.bpm_slider = QSlider(Qt.Horizontal)
        self.bpm_slider.setRange(40, 240)
        self.bpm_slider.setValue(120)
        self.bpm_slider.setFixedHeight(20)
        self.bpm_slider.valueChanged.connect(self.on_bpm_changed)
        
        bpm_layout.addWidget(bpm_label)
        bpm_layout.addWidget(self.bpm_slider)
        main_layout.addLayout(bpm_layout)
        
        options_layout = QHBoxLayout()
        options_layout.setSpacing(12)
        
        beat_label = QLabel("节拍")
        beat_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 16px;")
        self.beat_count_combo = QComboBox()
        self.beat_count_combo.addItems(['2拍', '4拍'])
        self.beat_count_combo.setCurrentIndex(1)
        self.beat_count_combo.setStyleSheet("""
            QComboBox {
                background: rgba(26, 26, 46, 0.95);
                border: 2px solid rgba(0, 217, 255, 0.5);
                border-radius: 6px;
                color: white;
                font-family: "Microsoft YaHei";
                font-size: 16px;
                padding: 6px;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid rgba(0, 217, 255, 0.8);
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background: rgba(26, 26, 46, 0.98);
                border: 2px solid rgba(0, 217, 255, 0.5);
                color: white;
                font-family: "Microsoft YaHei";
                font-size: 16px;
                selection-background-color: rgba(123, 44, 191, 0.5);
                padding: 3px;
            }
        """)
        self.beat_count_combo.currentIndexChanged.connect(self.on_beat_count_changed)
        
        click_label = QLabel("节拍声")
        click_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 14px;")
        self.click_combo = QComboBox()
        self.click_combo.addItems(['电子音', '木鱼', '蜂鸣'])
        self.click_combo.setStyleSheet("""
            QComboBox {
                background: rgba(26, 26, 46, 0.95);
                border: 2px solid rgba(0, 217, 255, 0.5);
                border-radius: 6px;
                color: white;
                font-family: "Microsoft YaHei";
                font-size: 16px;
                padding: 6px;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid rgba(0, 217, 255, 0.8);
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background: rgba(26, 26, 46, 0.98);
                border: 2px solid rgba(0, 217, 255, 0.5);
                color: white;
                font-family: "Microsoft YaHei";
                font-size: 16px;
                selection-background-color: rgba(123, 44, 191, 0.5);
                padding: 3px;
            }
        """)
        self.click_combo.currentIndexChanged.connect(self.on_click_type_changed)
        
        options_layout.addWidget(beat_label)
        options_layout.addWidget(self.beat_count_combo, 1)
        options_layout.addWidget(click_label)
        options_layout.addWidget(self.click_combo, 2)
        main_layout.addLayout(options_layout)
        
        volume_layout = QHBoxLayout()
        volume_label = QLabel("音量")
        volume_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 16px;")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedHeight(28)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        main_layout.addLayout(volume_layout)
        
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(10)
        preset_layout.addStretch()
        presets = [100, 120, 140, 160, 180, 200]
        for preset in presets:
            btn = QPushButton(str(preset))
            btn.setFixedSize(52, 38)
            btn.clicked.connect(lambda checked, p=preset: self.set_preset(p))
            self.preset_buttons.append(btn)
            preset_layout.addWidget(btn)
        preset_layout.addStretch()
        main_layout.addLayout(preset_layout)
        main_layout.addSpacing(5)
        
        self.play_btn = QPushButton("▶ 开始")
        self.play_btn.setFixedHeight(52)
        self.play_btn.clicked.connect(self.toggle_play)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #7b2cbf, stop:1 #00d9ff);
                border: none;
                border-radius: 10px;
                color: white;
                font-family: "Microsoft YaHei";
                font-size: 20px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.play_btn)
    
    def show_settings(self):
        if self.settings_dialog is None:
            self.settings_dialog = SettingsDialog(self)
            self.update_playlist_display()
        # 设置主题下拉框的当前值
        theme_index = 0 if self.theme == 'dark' else 1
        self.settings_dialog.theme_combo.setCurrentIndex(theme_index)
        self.settings_dialog.apply_initial_styles()
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.activateWindow()
    
    def update_widget_style(self, widget):
        if self.theme == 'dark':
            widget.setStyleSheet("""
                QWidget {
                    background: rgba(26, 26, 46, %(transparency)s);
                    border: 2px solid rgba(0, 217, 255, 0.5);
                    border-radius: 15px;
                }
                QLabel {
                    color: white;
                    font-family: "Microsoft YaHei";
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #9b4cdf, stop:1 #20e9ff);
                }
                QSlider::groove:horizontal {
                    height: 8px;
                    background: rgba(255, 255, 255, 0.15);
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    width: 24px;
                    height: 24px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border-radius: 12px;
                    margin: -8px 0;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border-radius: 4px;
                }
            """ % {'transparency': self.transparency})
        else:
            widget.setStyleSheet("""
                QWidget {
                    background: rgba(243, 244, 246, %(transparency)s);
                    border: 2px solid rgba(34, 197, 94, 0.4);
                    border-radius: 15px;
                }
                QLabel {
                    color: #1f2937;
                    font-family: "Microsoft YaHei";
                }
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #059669, stop:1 #0891b2);
                }
                QSlider::groove:horizontal {
                    height: 8px;
                    background: rgba(31, 41, 55, 0.1);
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    width: 24px;
                    height: 24px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 12px;
                    margin: -8px 0;
                }
                QSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 4px;
                }
            """ % {'transparency': self.transparency})
    
    def update_window_size(self):
        self.setFixedSize(380, 600)
    
    def update_playlist_display(self):
        if self.settings_dialog:
            self.settings_dialog.playlist.clear()
            for file_path in self.bg_player.playlist:
                self.settings_dialog.playlist.addItem(os.path.basename(file_path))
    
    def update_music_label(self):
        current = self.bg_player.get_current_track()
        if self.theme == 'dark':
            if current:
                filename = os.path.basename(current)
                self.music_label.setText(f"♪ {filename}")
                self.music_label.setStyleSheet("color: rgba(0, 217, 255, 1.0);")
            else:
                self.music_label.setText("♪ 未播放音乐")
                self.music_label.setStyleSheet("color: rgba(0, 217, 255, 0.6);")
        else:
            if current:
                filename = os.path.basename(current)
                self.music_label.setText(f"♪ {filename}")
                self.music_label.setStyleSheet("color: rgba(16, 185, 129, 1.0);")
            else:
                self.music_label.setText("♪ 未播放音乐")
                self.music_label.setStyleSheet("color: rgba(16, 185, 129, 0.7);")
    
    def on_theme_changed(self, index):
        themes = ['dark', 'light']
        self.theme = themes[index]
        self.update_widget_style(self.centralWidget())
        self.update_other_widgets_style()
        self.update_music_label()
        # 更新设置对话框样式
        if self.settings_dialog:
            self.settings_dialog.update_all_styles()
    
    def update_other_widgets_style(self):
        # 更新标题栏按钮
        if self.theme == 'dark':
            for btn in [self.findChild(QPushButton, "✕"), self.findChild(QPushButton, "⚙️")]:
                if btn:
                    if btn.text() == "✕":
                        btn.setStyleSheet("""
                            QPushButton {
                                background: rgba(255, 100, 100, 0.3);
                                border-radius: 50%;
                                font-family: "Microsoft YaHei";
                                font-size: 16px;
                                color: white;
                            }
                            QPushButton:hover {
                                background: rgba(255, 100, 100, 0.6);
                            }
                        """)
                    else:
                        btn.setStyleSheet("""
                            QPushButton {
                                background: rgba(123, 44, 191, 0.3);
                                border-radius: 50%;
                                font-family: "Microsoft YaHei";
                                font-size: 18px;
                                color: white;
                            }
                            QPushButton:hover {
                                background: rgba(123, 44, 191, 0.6);
                            }
                        """)
        else:
            for btn in self.findChildren(QPushButton):
                if btn.text() == "✕":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: rgba(239, 68, 68, 0.15);
                            border-radius: 50%;
                            font-family: "Microsoft YaHei";
                            font-size: 16px;
                            color: #dc2626;
                        }
                        QPushButton:hover {
                            background: rgba(239, 68, 68, 0.3);
                        }
                    """)
                elif btn.text() == "⚙️":
                    btn.setStyleSheet("""
                        QPushButton {
                            background: rgba(16, 185, 129, 0.15);
                            border-radius: 50%;
                            font-family: "Microsoft YaHei";
                            font-size: 18px;
                            color: #059669;
                        }
                        QPushButton:hover {
                            background: rgba(16, 185, 129, 0.3);
                        }
                    """)
        
        # 更新文字颜色（浅色主题用深色文字）
        if self.theme == 'dark':
            self.bpm_display.setStyleSheet("color: white;")
            for label in self.findChildren(QLabel):
                if label.text() not in ["✕", "⚙️"]:
                    if "♪" in label.text():
                        label.setStyleSheet("color: rgba(0, 217, 255, 1.0);")
                    elif label.text() in ["BPM", "节拍", "节拍声", "音量"]:
                        label.setStyleSheet(f"color: rgba(255, 255, 255, 0.9); font-family: 'Microsoft YaHei'; font-size: 16px;")
        else:
            self.bpm_display.setStyleSheet("color: #1f2937;")
            for label in self.findChildren(QLabel):
                if label.text() not in ["✕", "⚙️"]:
                    if "♪" in label.text():
                        label.setStyleSheet("color: rgba(16, 185, 129, 1.0);")
                    elif label.text() in ["BPM", "节拍", "节拍声", "音量"]:
                        label.setStyleSheet(f"color: #1f2937; font-family: 'Microsoft YaHei'; font-size: 16px;")
        
        # 更新节拍指示器
        for indicator in self.beat_indicators:
            if self.theme == 'dark':
                indicator.setStyleSheet("background: rgba(123, 44, 191, 0.5); border-radius: 3px;")
            else:
                indicator.setStyleSheet("background: rgba(34, 197, 94, 0.5); border-radius: 3px;")
        
        # 更新预设按钮
        for btn in self.preset_buttons:
            if self.theme == 'dark':
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(0, 217, 255, 0.2);
                        border: 1px solid rgba(0, 217, 255, 0.5);
                        border-radius: 7px;
                        color: #00d9ff;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background: rgba(0, 217, 255, 0.4);
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(16, 185, 129, 0.15);
                        border: 1px solid rgba(16, 185, 129, 0.5);
                        border-radius: 7px;
                        color: #059669;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background: rgba(16, 185, 129, 0.3);
                    }
                """)
        
        # 更新下拉框
        for combo in self.findChildren(QComboBox):
            if self.theme == 'dark':
                combo.setStyleSheet("""
                    QComboBox {
                        background: rgba(26, 26, 46, 0.95);
                        border: 2px solid rgba(0, 217, 255, 0.5);
                        border-radius: 6px;
                        color: white;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        padding: 6px;
                        min-height: 20px;
                    }
                    QComboBox::drop-down {
                        border: none;
                        width: 25px;
                    }
                    QComboBox::down-arrow {
                        image: none;
                        border-left: 4px solid transparent;
                        border-right: 4px solid transparent;
                        border-top: 6px solid rgba(0, 217, 255, 0.8);
                        margin-right: 8px;
                    }
                    QComboBox QAbstractItemView {
                        background: rgba(26, 26, 46, 0.98);
                        border: 2px solid rgba(0, 217, 255, 0.5);
                        color: white;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        selection-background-color: rgba(123, 44, 191, 0.5);
                        padding: 3px;
                    }
                """)
            else:
                combo.setStyleSheet("""
                    QComboBox {
                        background: rgba(243, 244, 246, 0.95);
                        border: 2px solid rgba(16, 185, 129, 0.4);
                        border-radius: 6px;
                        color: #1f2937;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        padding: 6px;
                        min-height: 20px;
                    }
                    QComboBox::drop-down {
                        border: none;
                        width: 25px;
                    }
                    QComboBox::down-arrow {
                        image: none;
                        border-left: 4px solid transparent;
                        border-right: 4px solid transparent;
                        border-top: 6px solid rgba(16, 185, 129, 0.8);
                        margin-right: 8px;
                    }
                    QComboBox QAbstractItemView {
                        background: rgba(243, 244, 246, 0.98);
                        border: 2px solid rgba(16, 185, 129, 0.4);
                        color: #1f2937;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        selection-background-color: rgba(34, 197, 94, 0.3);
                        padding: 3px;
                    }
                """)
    
    def on_bpm_changed(self, value):
        self.bpm_display.setText(str(value))
        self.audio_player.set_bpm(value)
    
    def on_volume_changed(self, value):
        self.audio_player.set_volume(value / 100)
    
    def on_beat_count_changed(self, index):
        beat_counts = [2, 4]
        self.audio_player.set_beats_per_measure(beat_counts[index])
        self.update_beat_indicators_visibility(beat_counts[index])
    
    def on_click_type_changed(self, index):
        types = ['electronic', 'woodblock', 'beep']
        self.audio_player.set_click_type(types[index])
    
    def on_transparency_changed(self, value):
        self.transparency = value / 100
        self.update_widget_style(self.centralWidget())
        if self.settings_dialog:
            self.settings_dialog.transparency_slider.blockSignals(True)
            self.settings_dialog.transparency_slider.setValue(int(value * 100))
            self.settings_dialog.transparency_slider.blockSignals(False)
    
    def on_bg_volume_changed(self, value):
        self.bg_player.set_volume(value / 100)
    
    def update_beat_indicators_visibility(self, active_count):
        for i, indicator in enumerate(self.beat_indicators):
            indicator.setVisible(i < active_count)
    
    def set_preset(self, bpm):
        self.bpm_slider.setValue(bpm)
    
    def toggle_play(self):
        if self.audio_player.is_playing:
            self.audio_player.stop_playing()
            self.play_btn.setText("▶ 开始")
            self.play_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #7b2cbf, stop:1 #00d9ff);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 20px;
                    font-weight: bold;
                }
            """)
            for indicator in self.beat_indicators:
                indicator.setStyleSheet("background: rgba(123, 44, 191, 0.5); border-radius: 3px;")
        else:
            self.audio_player.start_playing()
            self.play_btn.setText("⏸ 暂停")
            self.play_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #ff6b6b, stop:1 #ee5a24);
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-family: "Microsoft YaHei";
                    font-size: 20px;
                    font-weight: bold;
                }
            """)
    
    @pyqtSlot(int)
    def update_beat_indicator(self, beat):
        for i, indicator in enumerate(self.beat_indicators):
            if i == beat:
                if self.theme == 'dark':
                    indicator.setStyleSheet("""
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #7b2cbf, stop:1 #00d9ff);
                        border-radius: 3px;
                        box-shadow: 0 0 10px rgba(0, 217, 255, 0.9);
                    """)
                else:
                    indicator.setStyleSheet("""
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #3b82f6, stop:1 #06b6d4);
                        border-radius: 3px;
                        box-shadow: 0 0 10px rgba(59, 130, 246, 0.9);
                    """)
            else:
                if self.theme == 'dark':
                    indicator.setStyleSheet("background: rgba(123, 44, 191, 0.5); border-radius: 3px;")
                else:
                    indicator.setStyleSheet("background: rgba(59, 130, 246, 0.5); border-radius: 3px;")
    
    def load_last_music_dir(self):
        import os
        config_dir = os.path.join(os.path.expanduser("~"), ".metronome")
        config_file = os.path.join(config_dir, "config.txt")
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                path = f.read().strip()
                if os.path.isdir(path):
                    return path
        return ""
    
    def save_last_music_dir(self, directory):
        import os
        config_dir = os.path.join(os.path.expanduser("~"), ".metronome")
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "config.txt")
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(directory)
    
    def add_music_to_playlist(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择音乐文件", self.last_music_dir, 
            "音频文件 (*.mp3 *.wav *.ogg *.flac *.m4a *.wma)"
        )
        if file_paths:
            self.bg_player.add_to_playlist(file_paths)
            self.update_playlist_display()
            if file_paths:
                self.last_music_dir = os.path.dirname(file_paths[0])
                self.save_last_music_dir(self.last_music_dir)
    
    def remove_from_playlist(self):
        if self.settings_dialog:
            current_row = self.settings_dialog.playlist.currentRow()
            if current_row >= 0:
                self.bg_player.remove_from_playlist(current_row)
                self.update_playlist_display()
                self.update_music_label()
    
    def on_playlist_item_clicked(self, item):
        if self.settings_dialog:
            index = self.settings_dialog.playlist.row(item)
            if self.bg_player.play_index(index):
                self.update_music_label()
                self.settings_dialog.bg_play_btn.setText("⏸ 暂停")
                self.settings_dialog.bg_play_btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(255, 100, 100, 0.3);
                        border: 2px solid rgba(255, 100, 100, 0.5);
                        border-radius: 8px;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        color: #ff6464;
                    }
                """)
    
    def toggle_bg_play(self):
        if self.bg_player.is_playing:
            self.bg_player.pause()
            if self.settings_dialog:
                self.settings_dialog.bg_play_btn.setText("▶ 播放")
                self.settings_dialog.bg_play_btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(0, 255, 100, 0.3);
                        border: 2px solid rgba(0, 255, 100, 0.5);
                        border-radius: 8px;
                        font-family: "Microsoft YaHei";
                        font-size: 14px;
                        color: #00ff64;
                    }
                """)
        else:
            if self.bg_player.play():
                self.update_music_label()
                if self.settings_dialog:
                    self.settings_dialog.bg_play_btn.setText("⏸ 暂停")
                    self.settings_dialog.bg_play_btn.setStyleSheet("""
                        QPushButton {
                            background: rgba(255, 100, 100, 0.3);
                            border: 2px solid rgba(255, 100, 100, 0.5);
                            border-radius: 8px;
                            font-family: "Microsoft YaHei";
                            font-size: 14px;
                            color: #ff6464;
                        }
                    """)
    
    def stop_bg_music(self):
        self.bg_player.stop()
        self.update_music_label()
        if self.settings_dialog:
            self.settings_dialog.bg_play_btn.setText("▶ 播放")
            self.settings_dialog.bg_play_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 255, 100, 0.3);
                    border: 2px solid rgba(0, 255, 100, 0.5);
                    border-radius: 8px;
                    font-family: "Microsoft YaHei";
                    font-size: 14px;
                    color: #00ff64;
                }
            """)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
    
    def closeEvent(self, event):
        self.audio_player.stop_playing()
        self.audio_player.quit()
        self.bg_player.quit()
        if self.settings_dialog:
            self.settings_dialog.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 26, 46))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)
    
    window = MetronomeWindow()
    window.show()
    
    sys.exit(app.exec_())