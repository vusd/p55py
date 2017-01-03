from PIL import Image, ImageDraw
import time
import calendar

def empty_function(wrapper):
    pass

class Canvas():
    drawContext = None
    cur_fill = (0, 0, 0, 255)
    cur_outline = (0, 0, 0, 255)

    def __init__(self, width=320, height=320, setupfn=empty_function, drawfn=empty_function, stepfn=empty_function, renderfn=empty_function):
        self.setup_func = setupfn
        self.draw_func = drawfn
        self.step_func = stepfn
        self.render_func = renderfn
        self.width = width
        self.height = height
        self.redraw_freq = 1
        self.random_seed = int(calendar.timegm(time.gmtime()))
        self.reset()
        
    def reset(self):
        color = (0,0,0,255)
        self.step_number = 0
        self.backend_img = Image.new('RGBA', [self.width, self.height], color=color)
        self.drawContext = ImageDraw.Draw(self.backend_img)
        self.setup_func(self)

    def onecycle(self):
        self.step_func(self)
        if self.step_number % self.redraw_freq == 0:
            self.render_func(self)
        self.draw_func(self)
        self.step_number += 1
        
    def fill(self, c):
        self.cur_fill = (c, c, c, 255)

    def stroke(self, c):
        self.cur_outline = (c, c, c, 255)

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

    def image(self):
        return self.backend_img;
