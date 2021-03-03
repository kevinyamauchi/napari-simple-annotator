from napari_plugin_engine import napari_hook_implementation

from .qt_shape_annotation_controls import QtShapeAnnotationControls


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    kwargs = {"area": "right", "name": "ShapeAnnotator"}
    return (QtShapeAnnotationControls, kwargs)
