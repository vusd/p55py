import ipywidgets as widgets
from traitlets import Unicode, CInt, CBytes, CBool
#TODO: this is not really necessary here, cleanup
import numpy as np

#TODO: move to separate file
#### p55 drawing convenience methods
class P55DrawContext():
    drawContext = None
    cur_fill = (0, 0, 0, 255)
    cur_outline = (0, 0, 0, 255)

    def fill(self, c):
        self.cur_fill = (c, c, c, 255)

    def ellipse(self, x1, y1, rx, ry):
        if self.drawContext is None:
            return
        hrx = int(rx / 2)
        hry = int(ry / 2)
        self.drawContext.ellipse((x1-hrx, y1-hry, x1+hrx, y1+hry), self.cur_fill, self.cur_outline)

    def rectangle(self, x1, y1, x2, y2):
        if self.drawContext is None:
            return
        self.drawContext.rectangle([x1, y1, x2, y2], self.cur_fill, self.cur_outline)

    def line(self, x1, y1, x2, y2):
        if self.drawContext is None:
            return
        self.drawContext.line((x1, y1, x2, y2), self.cur_fill)

@widgets.register('p55py.P55CanvasWidget')
class P55CanvasWidget(widgets.DOMWidget, P55DrawContext):
    """"""
    _view_name = Unicode('P55CanvasView').tag(sync=True)
    _model_name = Unicode('P55CanvasModel').tag(sync=True)
    _view_module = Unicode('p55py').tag(sync=True)
    _model_module = Unicode('p55py').tag(sync=True)

    value = CInt().tag(sync=True)
    canvas_width = CInt(320).tag(sync=True)
    canvas_height = CInt(320).tag(sync=True)
    temp_array = np.zeros([320,320,4], dtype='uint8') + 128
    image_buffer = CBytes(temp_array.tobytes()).tag(sync=True)
    mouseX = CInt().tag(sync=True)
    mouseY = CInt().tag(sync=True)
    mousePressed = CBool().tag(sync=True)

# TODO: this goes somewhere else too
import time
import calendar
import random
import numpy as np

from PIL import Image, ImageDraw
from ipywidgets import interactive
import webcolors
import traitlets

def get_p55_play_observer(wrapper):
    def play_observer(change):
        backend_img = wrapper.backend_img
        p55_widget = wrapper.p55_widget
        value = change['new']
        if value == 0:
            wrapper.reset_widget();
            backend_img = wrapper.backend_img
        else:
            wrapper.step_func(p55_widget)
            if value % wrapper.redrawFreq == 0:
                wrapper.render_func(p55_widget)
            wrapper.draw_func(p55_widget)
        p55_widget.image_buffer = backend_img.tobytes()
    return play_observer

def get_label_changer(wrapper):
    def on_value_change(change):
        wrapper.step_label.value = u"{}".format(change['new'])
    return on_value_change

def empty_function(wrapper):
    pass

class P55Wrapper():
    def reset_widget(self):
        if self.incSeedOnStop:
            self.randomSeed = self.randomSeed + 1
            if self.randomSeedWidget is not None:
                self.randomSeedWidget.value = self.randomSeed
        random.seed(self.randomSeed)
        np.random.seed(self.randomSeed)
        color = (0,0,0,255)
        self.backend_img = Image.new('RGBA', [self.p55_widget.canvas_width, self.p55_widget.canvas_height], color=color)
        self.p55_widget.drawContext = ImageDraw.Draw(self.backend_img)
        self.setup_func(self.p55_widget)

    def __init__(self, width=320, height=320, setupfn=empty_function, drawfn=empty_function, stepfn=empty_function, renderfn=empty_function):
        self.setup_func = setupfn
        self.draw_func = drawfn
        self.step_func = stepfn
        self.render_func = renderfn
        self.redrawFreq = 1
        self.randomSeed = int(calendar.timegm(time.gmtime()))
        self.incSeedOnStop = True
        self.settings_pane = None
        self.randomSeedWidget = None

        self.play = widgets.Play()
        self.p55_widget = P55CanvasWidget()
        self.p55_widget.canvas_width = width
        self.p55_widget.canvas_height = height
        self.p55_widget.value = 0
        self.reset_widget();
        self.step_label = widgets.Label(u"0", description='step');

        play_observer = get_p55_play_observer(self)
        self.p55_widget.observe(play_observer, names='value')
        traitlets.link((self.play, 'value'), (self.p55_widget, 'value'))
        label_observer = get_label_changer(self)
        self.p55_widget.observe(label_observer, names='value')

        self.play_row = widgets.HBox([self.play, self.step_label])
        self.display_pane = widgets.VBox([self.p55_widget, self.play_row])
        self.widget = widgets.HBox([self.display_pane])

    def addSettingsPane(self, settings_pane, randomSeedWidget):
        self.settings_pane = settings_pane
        self.randomSeedWidget = randomSeedWidget
        self.widget = widgets.HBox([self.display_pane, settings_pane])
