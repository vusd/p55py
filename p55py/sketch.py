from .canvas import Canvas
import ipywidgets as widgets
import io

def raw_image_to_png_bytes(im):
    b = io.BytesIO()
    im.save(b, 'png')
    return b.getvalue()    

def get_p55_play_observer(wrapper):
    def play_observer(change):
        old_value = change['old']
        new_value = change['new']
        if new_value > 0 and old_value == 0:
            wrapper.reset_widget();
        if new_value > old_value:
            wrapper.canvas.onecycle();
        wrapper.image.value = raw_image_to_png_bytes(wrapper.canvas.image())
        wrapper.step_label.value = u"{}".format(wrapper.canvas.step_number)
    return play_observer

class Sketch():
    def __init__(self, *args, **kwargs):
        self.canvas = Canvas(*args, **kwargs)
        self.image = widgets.Image(value=raw_image_to_png_bytes(self.canvas.image()),format='png',width=self.canvas.width,height=self.canvas.height)
        self.play = widgets.Play()
        self.play.max = 2**31-1
        play_observer = get_p55_play_observer(self)
        self.play.observe(play_observer, names='value')
        self.step_label = widgets.Label(u"0", description='step');

        self.play_row = widgets.HBox([self.play, self.step_label])
        self.display_pane = widgets.VBox([self.image, self.play_row])
        self.main_widget = widgets.HBox([self.display_pane])

    def reset_widget(self):
        self.canvas.reset()

    def widget(self):
        return self.main_widget