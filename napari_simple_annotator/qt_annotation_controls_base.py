from qtpy.QtCore import Qt
from qtpy.QtWidgets import QVBoxLayout, QWidget


class QtAnnotationControlsBase(QWidget):
    """A QWidget base class for controlling the annotation properties.

    This is implemented as a QtShapesAnnotationsControls class.

    Parameters
    ----------
    viewer : napari.viewer.Viewer
        The parent napari viewer
    """

    def __init__(self, viewer):
        super().__init__()

        # save the viewer
        self.viewer = viewer

        self.selected_layer = None

        # create the combobox for selecting the layer to make the
        # annotations on the subclass should implement this method
        layer_combobox = self._create_layer_combo_box()
        self.layer_combobox = layer_combobox
        self.layer_combo_box.currentIndexChanged.connect(self.on_layer_select)
        self._initialize_layer_combobox()

        # connect the viewer layer list events
        self.viewer.layers.events.inserted.connect(self.on_add_layer)
        self.viewer.layers.events.removed.connect(self.on_remove_layer)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.layer_combo_box)
        self.vbox_layout.addWidget(self.table)

        self.setLayout(self.vbox_layout)

    def _create_layer_combo_box(self):
        raise NotImplementedError

    def _initialize_layer_combobox(self):
        """Populates the combobox with all layers that contain properties"""
        raise NotImplementedError

    def on_add_layer(self, event):
        """Callback function that updates the layer list combobox
        when a layer is added to the viewer LayerList.
        """
        layer_name = event.value.name
        layer = self.viewer.layers[layer_name]
        if hasattr(layer, "properties"):
            self.layer_combo_box.addItem(layer_name)

    def on_remove_layer(self, event):
        """Callback function that updates the layer list combobox
        when a layer is removed from the viewer LayerList.
        """
        layer_name = event.value.name

        index = self.layer_combo_box.findText(layer_name, Qt.MatchExactly)
        # findText returns -1 if the item isn't in the ComboBox
        # if it is in the ComboBox, remove it
        if index != -1:
            self.layer_combo_box.removeItem(index)

            # get the new layer selection
            index = self.layer_combo_box.currentIndex()
            layer_name = self.layer_combo_box.itemText(index)
            if layer_name != self.selected_layer:
                self.selected_layer = layer_name

    def _connect_layer_events(self, layer_name: str):
        """Connect the selected layer's properties events to
        table the update function.

        Parameters
        ----------
        layer_name : str
            The name of the layer to connect the update_table
            method to.
        """
        layer = self.viewer.layers[layer_name]
        layer.events.properties.connect(self.update_table)

    def _disconnect_layer_events(self, layer_name: str):
        """Connect the selected layer's properties events to
        table the update function.

        Parameters
        ----------
        layer_name : str
            The name of the layer to disconnect the update_table
            from
        """
        layer = self.viewer.layers[layer_name]
        layer.events.properties.disconnect(self.update_table)
