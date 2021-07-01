from kivy.app import App
from kivy.lang import Builder
import threading
import time

kv = '''
FloatLayout:
    ScrollView:
        pos_hint: {'left': 1, 'top': 1}
        size_hint_y: .8
        do_scroll_x: False
        Label:
            id: debugarea
            size_hint: None, None
            size: self.texture_size
    Button:
        size_hint_y: .1
        text: 'start'
        on_release:
            app.do_print()
            self.text = 'stop' if app.is_printing else 'start'
'''

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_printing = False
        self.print_thread = None
        self.root_widget = Builder.load_string(kv)

    def build(self):
        return self.root_widget

    def printer(self):
        i = 0
        while self.is_printing:
            self.root_widget.ids['debugarea'].text += f'Hello {i}' + '\n'
            i += 1
            time.sleep(1)

    def do_print(self):
        if not self.is_printing:
            self.is_printing = True
            self.print_thread = threading.Thread(target=self.printer)
            self.print_thread.start()
        else:
            self.is_printing = False
            self.print_thread.join()
            self.print_thread = None

MainApp().run()
