var widgets = require('jupyter-js-widgets');
var _ = require('underscore');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including `_model_name`, `_view_name`, `_model_module`
// and `_view_module` when different from the base class.
//
// When serialiazing entire widget state for embedding, only values different from the
// defaults will be specified.
var P55CanvasModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
        _model_name : 'P55CanvasModel',
        _view_name : 'P55CanvasView',
        _model_module : 'p55py',
        _view_module : 'p55py',
        value : 'Hello P55'
    })
});

//TODO: think about whether this goes here
var p55_mouse_x = 0;
var p55_mouse_y = 0;
var p55_mouse_is_down = false;

var callback_on_mouse_down = function(evt) {
    p55_mouse_is_down = true;
};

var callback_on_mouse_up = function(evt) {
    p55_mouse_is_down = false;
};

function track_mouse_pos(evt) {
    p55_mouse_x = evt.clientX;
    p55_mouse_y = evt.clientY;
}

// Custom View. Renders the widget model.
var P55CanvasView = widgets.DOMWidgetView.extend({
    render: function() {
        var that = this;
        var canvas_width = this.model.get('canvas_width');
        var canvas_height = this.model.get('canvas_height');
        var canvas_str = '<canvas width="' + canvas_width + '" height="' + canvas_height + '"></canvas>'
        this.$canvas = $(canvas_str);
        this.$el.append(this.$canvas);
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
        this.$canvas[0].addEventListener('mousemove', track_mouse_pos, false);
        this.$canvas[0].addEventListener('mousedown', callback_on_mouse_down, false);
        this.$canvas[0].addEventListener('mouseup', callback_on_mouse_up, false);
    },

    value_changed: function() {
        // anytime the value is changed we do a full sync
        var canvas_width = this.model.get('canvas_width');
        var canvas_height = this.model.get('canvas_height');
        this.$canvas[0].width = canvas_width
        this.$canvas[0].height = canvas_height
        var ctx = this.$canvas[0].getContext("2d");
        var buffer = this.model.get('image_buffer').buffer
        var arr = new Uint8ClampedArray(buffer);
        var imdata = new ImageData(arr, canvas_width, canvas_height);
        ctx.putImageData(imdata, 0, 0)
        var rect = this.$canvas[0].getBoundingClientRect();
        var local_x = Math.floor( p55_mouse_x - rect.left );
        var local_y = Math.floor( p55_mouse_y - rect.top );
        this.handle_mouse(local_x, local_y, p55_mouse_is_down);
    },

    handle_mouse: function(x, y, is_down) {
        this.model.set('mouseX', x);
        this.model.set('mouseY', y);
        this.model.set('mousePressed', is_down);
        this.touch();
    }
});

module.exports = {
    P55CanvasModel : P55CanvasModel,
    P55CanvasView : P55CanvasView
};
