from .qt_annotation_controls_base import QtAnnotationControlsBase


class QtShapeAnnotationControls(QtAnnotationControlsBase):
    """Qt widget for control the annotation properties
    when annotating with shapes (polygons).

    Parameters
    ----------
    viewer : napari.viewer.Viewer
        The parent napari viewer
    """

    def __init__(self, viewer):
        super().__init__(viewer=viewer)

    def _layer_filter(self, layer):
        """Function that returns true if the layer should be included in the
        combobox of layers to be annotated and false if not.

        The criterion is that the layer is a shapes layer.

        Parameters
        ----------
        layer
            The napari layer to test if it should be included
            in the layer list combobox

        Returns
        -------
        include_layer : bool
            True if the provided layer should be included in the layer combobox
        """
        if layer._type_string == "shapes":
            include_layer = True
        else:
            include_layer = False

        return include_layer
