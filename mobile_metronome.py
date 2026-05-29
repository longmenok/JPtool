from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
import os

class MetronomeApp(App):
    title = '节拍器'
    bpm = NumericProperty(120)
    beat_count = NumericProperty(4)
    volume = NumericProperty(0.7)
    is_playing = BooleanProperty(False)
    current_beat = NumericProperty(0)
    current_track = StringProperty('')
    theme = StringProperty('dark')
    
    def build(self):
        self.sound_files = {
            'tick': 'sounds/tick.wav',
            'tock': 'sounds/tock.wav',
            'click': 'sounds/click.wav'
        }
        self.current_sound = 'tick'
        self.tick_sound = None
        self.clock_event = None
        self.playlist = []
        self.current_track_index = -1
        
        return MainLayout()

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        
        self.app = App.get_running_app()
        self.setup_ui()
        self.update_theme()
        
    def setup_ui(self):
        self.add_widget(TopBar())
        
        self.bpm_display = Label(
            text='120',
            font_size='72sp',
            bold=True
        )
        self.add_widget(self.bpm_display)
        
        self.beat_indicators = BeatIndicator()
        self.add_widget(self.beat_indicators)
        
        self.add_widget(BPMSlider())
        
        self.add_widget(BeatSelector())
        
        self.add_widget(VolumeSlider())
        
        self.add_widget(PresetButtons())
        
        self.control_button = Button(
            text='▶ 开始',
            font_size='24sp',
            size_hint_y=None,
            height=70,
            on_press=self.toggle_play
        )
        self.add_widget(self.control_button)
        
        self.music_label = Label(
            text='♪ 未播放音乐',
            font_size='18sp',
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.music_label)
        
        self.settings_button = Button(
            text='⚙️ 设置',
            font_size='20sp',
            size_hint_y=None,
            height=60,
            on_press=self.show_settings
        )
        self.add_widget(self.settings_button)
        
    def toggle_play(self, instance):
        app = App.get_running_app()
        if app.is_playing:
            self.stop_metronome()
        else:
            self.start_metronome()
    
    def start_metronome(self):
        app = App.get_running_app()
        app.is_playing = True
        self.control_button.text = '❚❚ 暂停'
        interval = 60.0 / app.bpm
        app.current_beat = 0
        app.bind(bpm=self.on_bpm_change)
        self.clock_event = Clock.schedule_interval(self.tick, interval)
        
    def stop_metronome(self):
        app = App.get_running_app()
        app.is_playing = False
        self.control_button.text = '▶ 开始'
        if self.clock_event:
            self.clock_event.cancel()
            self.clock_event = None
        app.unbind(bpm=self.on_bpm_change)
        
    def on_bpm_change(self, instance, value):
        if app.is_playing:
            self.stop_metronome()
            self.start_metronome()
        
    def tick(self, dt):
        app = App.get_running_app()
        app.current_beat = (app.current_beat % app.beat_count) + 1
        self.beat_indicators.update_indicator(app.current_beat)
        
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load(f'sounds/{app.current_sound}.wav')
        if sound:
            sound.volume = app.volume
            sound.play()
    
    def update_theme(self):
        app = App.get_running_app()
        if app.theme == 'dark':
            self.canvas.before.clear()
            with self.canvas.before:
                Color(26/255, 26/255, 46/255, 1)
                Rectangle(pos=self.pos, size=self.size)
            text_color = (255/255, 255/255, 255/255, 1)
            accent_color = (0/255, 217/255, 255/255, 1)
        else:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(243/255, 244/255, 246/255, 1)
                Rectangle(pos=self.pos, size=self.size)
            text_color = (31/255, 41/255, 55/255, 1)
            accent_color = (16/255, 185/255, 129/255, 1)
        
        self.bpm_display.color = text_color
        self.control_button.color = (1, 1, 1, 1)
        self.control_button.background_color = accent_color
        self.settings_button.color = accent_color
        
    def show_settings(self, instance):
        popup = SettingsPopup()
        popup.open()

class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super(TopBar, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.padding = 10
        self.spacing = 10
        
        self.add_widget(Label(text='🎵 节拍器', font_size='22sp', bold=True))
        
        close_btn = Button(text='✕', font_size='20sp', size_hint_x=None, width=50)
        close_btn.bind(on_press=self.close_app)
        self.add_widget(close_btn)
        
    def close_app(self, instance):
        App.get_running_app().stop()

class BeatIndicator(BoxLayout):
    def __init__(self, **kwargs):
        super(BeatIndicator, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 40
        self.spacing = 10
        self.padding = 20
        self.indicators = []
        
        for i in range(4):
            indicator = Label(text='●', font_size='24sp')
            indicator.color = (123/255, 44/255, 191/255, 0.5)
            self.indicators.append(indicator)
            self.add_widget(indicator)
        
        App.get_running_app().bind(beat_count=self.on_beat_count_change)
        
    def update_indicator(self, beat):
        app = App.get_running_app()
        for i, indicator in enumerate(self.indicators):
            if i < app.beat_count:
                indicator.opacity = 1
                if i + 1 == beat:
                    indicator.color = (0/255, 217/255, 255/255, 1)
                else:
                    indicator.color = (123/255, 44/255, 191/255, 0.6)
            else:
                indicator.opacity = 0
    
    def on_beat_count_change(self, instance, value):
        self.update_indicator(0)

class BPMSlider(BoxLayout):
    def __init__(self, **kwargs):
        super(BPMSlider, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 10
        
        self.add_widget(Label(text='BPM', font_size='18sp'))
        
        self.slider = Slider(
            min=40,
            max=240,
            value=120,
            value_track=True
        )
        self.slider.bind(value=self.on_slider_change)
        self.add_widget(self.slider)
        
        self.value_label = Label(text='120', font_size='18sp')
        self.add_widget(self.value_label)
        
        App.get_running_app().bind(bpm=self.on_bpm_change)
        
    def on_slider_change(self, instance, value):
        App.get_running_app().bpm = int(value)
        
    def on_bpm_change(self, instance, value):
        self.value_label.text = str(value)
        self.slider.value = value

class BeatSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(BeatSelector, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.spacing = 10
        
        self.add_widget(Label(text='节拍', font_size='18sp'))
        
        self.spinner = Spinner(
            text='4拍',
            values=['2拍', '4拍'],
            font_size='18sp',
            size_hint_x=0.5
        )
        self.spinner.bind(text=self.on_spinner_change)
        self.add_widget(self.spinner)
        
    def on_spinner_change(self, instance, value):
        App.get_running_app().beat_count = int(value[0])

class VolumeSlider(BoxLayout):
    def __init__(self, **kwargs):
        super(VolumeSlider, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 10
        
        self.add_widget(Label(text='音量', font_size='18sp'))
        
        self.slider = Slider(
            min=0,
            max=1,
            value=0.7,
            value_track=True
        )
        self.slider.bind(value=self.on_slider_change)
        self.add_widget(self.slider)
        
        self.value_label = Label(text='70%', font_size='18sp')
        self.add_widget(self.value_label)
        
    def on_slider_change(self, instance, value):
        App.get_running_app().volume = value
        self.value_label.text = f'{int(value * 100)}%'

class PresetButtons(GridLayout):
    def __init__(self, **kwargs):
        super(PresetButtons, self).__init__(**kwargs)
        self.cols = 6
        self.size_hint_y = None
        self.height = 50
        self.spacing = 5
        
        presets = [100, 120, 140, 160, 180, 200]
        for preset in presets:
            btn = Button(
                text=str(preset),
                font_size='16sp',
                on_press=self.on_preset_click
            )
            self.add_widget(btn)
            
    def on_preset_click(self, instance):
        App.get_running_app().bpm = int(instance.text)

class SettingsPopup(Popup):
    def __init__(self, **kwargs):
        super(SettingsPopup, self).__init__(**kwargs)
        self.title = '设置'
        self.size_hint = (0.9, 0.8)
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        theme_layout = BoxLayout(orientation='horizontal', spacing=10)
        theme_layout.add_widget(Label(text='主题', font_size='18sp'))
        self.theme_spinner = Spinner(
            text='暗色' if App.get_running_app().theme == 'dark' else '浅色',
            values=['暗色', '浅色'],
            font_size='18sp'
        )
        self.theme_spinner.bind(text=self.on_theme_change)
        theme_layout.add_widget(self.theme_spinner)
        content.add_widget(theme_layout)
        
        sound_layout = BoxLayout(orientation='horizontal', spacing=10)
        sound_layout.add_widget(Label(text='节拍声', font_size='18sp'))
        self.sound_spinner = Spinner(
            text='tick',
            values=['tick', 'tock', 'click'],
            font_size='18sp'
        )
        self.sound_spinner.bind(text=self.on_sound_change)
        sound_layout.add_widget(self.sound_spinner)
        content.add_widget(sound_layout)
        
        music_layout = BoxLayout(orientation='vertical', spacing=10)
        music_layout.add_widget(Label(text='播放列表', font_size='18sp'))
        
        self.playlist_view = ScrollView(size_hint_y=0.5)
        self.playlist_list = Label(text='暂无音乐', font_size='16sp')
        self.playlist_view.add_widget(self.playlist_list)
        music_layout.add_widget(self.playlist_view)
        
        button_layout = BoxLayout(spacing=10)
        add_btn = Button(text='添加音乐', font_size='16sp', on_press=self.show_file_chooser)
        button_layout.add_widget(add_btn)
        remove_btn = Button(text='删除选中', font_size='16sp')
        button_layout.add_widget(remove_btn)
        music_layout.add_widget(button_layout)
        content.add_widget(music_layout)
        
        close_btn = Button(text='关闭', font_size='18sp', on_press=self.dismiss)
        content.add_widget(close_btn)
        
        self.content = content
        
    def on_theme_change(self, instance, value):
        app = App.get_running_app()
        app.theme = 'dark' if value == '暗色' else 'light'
        root = app.root
        root.update_theme()
        
    def on_sound_change(self, instance, value):
        App.get_running_app().current_sound = value
        
    def show_file_chooser(self, instance):
        file_chooser = FileChooserListView(filters=['*.mp3', '*.wav', '*.ogg'])
        popup = Popup(title='选择音乐文件', content=file_chooser, size_hint=(0.9, 0.8))
        
        def select_file(instance):
            if file_chooser.selection:
                app = App.get_running_app()
                app.playlist.extend(file_chooser.selection)
                self.update_playlist_display()
            popup.dismiss()
            
        file_chooser.bind(on_submit=select_file)
        popup.open()
        
    def update_playlist_display(self):
        app = App.get_running_app()
        if app.playlist:
            self.playlist_list.text = '\n'.join([os.path.basename(f) for f in app.playlist])
        else:
            self.playlist_list.text = '暂无音乐'

if __name__ == '__main__':
    MetronomeApp().run()