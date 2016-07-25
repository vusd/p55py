import ipywidgets as widgets
from traitlets import Unicode

@widgets.register('p55py.P55CanvasWidget')
class P55CanvasWidget(widgets.DOMWidget):
    """"""
    _view_name = Unicode('P55CanvasView').tag(sync=True)
    _model_name = Unicode('P55CanvasModel').tag(sync=True)
    _view_module = Unicode('p55py').tag(sync=True)
    _model_module = Unicode('p55py').tag(sync=True)
    value = Unicode('Hello P55!').tag(sync=True)
