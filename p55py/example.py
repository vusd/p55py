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
    image_src = Unicode(u"thumbnail.png").tag(sync=True)
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
from io import BytesIO
# import cStringIO
import base64

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

        outputBuffer = BytesIO()
        backend_img.save(outputBuffer, format='PNG')
        bgBase64Data = outputBuffer.getvalue()
        p55_widget.image_src = 'data:image/png;base64,' + base64.b64encode(bgBase64Data).decode()

        # buffer = cStringIO.StringIO()
        # backend_img.save(buffer, format="PNG")
        # img_str = base64.b64encode(buffer.getvalue())

        # byte_io = BytesIO()
        # backend_img.save(byte_io, 'PNG')
        # byte_io.seek(0)
        # p55_widget.image_src = u"final.png"
        # cheat_value = "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"
        # p55_widget.image_src = u"data:image/gif;base64,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"
        # p55_widget.image_src = u"data:image/png;base64," + str(base64.b64encode(byte_io.getvalue()))
        # p55_widget.image_src = u"data:image/png;base64," + img_str
        p55_widget.image_buffer = backend_img.tobytes()
        # bonus
        # byte_io = BytesIO()
        # image.save(byte_io, 'PNG')        
        # byte_io.seek(0)
        # p55_widget.image_src = u"final.png"
        # p55_widget.image_src = "data:image/png;base64," + base64.b64encode(img_buffer.getvalue())
        # print(p55_widget.image_src)

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
