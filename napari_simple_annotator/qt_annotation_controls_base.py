from magicgui.widgets import CheckBox, ComboBox, Container, Label
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
        # annotations on subclasses should implement this method
        self.layer_combo_box = self._initialize_layer_combobox()

        # create the combobox for selecting the property value
        self.property_name_combobox = self._initialize_property_name_combobox()

        self.combobox_container = Container(
            widgets=[self.layer_combo_box, self.property_name_combobox]
        )
        self.combobox_container.max_height = 80

        self.property_name_container = Container(
            widgets=[
                Label(value="Select properties"),
                CheckBox(name="hi name"),
                CheckBox(name="hello name"),
            ]
        )
        # self.property_name_container.max_height = 120
        print(self.property_name_container.margins)
        print(self.property_name_container.options)

        # connect the viewer layer list events
        self.viewer.layers.events.inserted.connect(self.on_add_layer)
        self.viewer.layers.events.removed.connect(self.on_remove_layer)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.combobox_container.native)
        self.vbox_layout.addWidget(self.property_name_container.native)

        # initialize the combobox for selecting the layer to make the
        # annotations on the subclass should implement this method
        self.layer_combo_box.changed.connect(self.on_layer_select)

        self.setLayout(self.vbox_layout)

    def _initialize_layer_combobox(self):
        """Populates the combobox with all layers that contain properties

        note that this requires the self._layer_filter() method to be
        implemented on the subclass

        """
        all_layers = self.viewer.layers
        names = [lr.name for lr in all_layers if self._layer_filter(lr)]
        layer_combo_box = ComboBox(label="layer:", choices=names)
        return layer_combo_box

    def _initialize_property_name_combobox(self):
        current_layer = self.layer_combo_box.value
        if current_layer is not None:
            choices = self.viewer.layers[current_layer].properties.keys()
        prop_name_combobox = ComboBox(label="property name:", choices=choices)

        return prop_name_combobox

    def _layer_filter(self, layer):
        """Function that returns true if the layer should be included in the
        combobox of layers to be annotated and false if not.

        Parameters
        ----------
        layer
            The napari layer to test if it should be included in
            the layer list combobox

        Returns
        -------
        include_layer : bool
            True if the provided layer should be included in the layer combobox
        """
        raise NotImplementedError

    def on_add_layer(self, event):
        """Callback function that updates the layer list combobox
        when a layer is added to the viewer LayerList.
        """
        layer_name = event.value.name
        layer = self.viewer.layers[layer_name]
        if self._layer_filter(layer):
            current_choices = list(self.layer_combo_box.choices)
            current_choices.append(layer_name)
            self.layer_combo_box.choices = current_choices

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

    def on_layer_select(self, index: int):
        """Callback function that updates the properties when a
        new layer is selected in the combobox.
        """
        # get the layer
        layer_name = self.layer_combo_box.value
        self._update_property_names(layer_name)

    def _update_property_names(self, layer_name):
        layer = self.viewer.layers[layer_name]
        property_names = list(layer.properties.keys())
        self.property_name_combobox.choices = property_names

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
