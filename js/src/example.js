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


// Custom View. Renders the widget model.
var P55CanvasView = widgets.DOMWidgetView.extend({
    render: function() {
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});


module.exports = {
    P55CanvasModel : P55CanvasModel,
    P55CanvasView : P55CanvasView
};
