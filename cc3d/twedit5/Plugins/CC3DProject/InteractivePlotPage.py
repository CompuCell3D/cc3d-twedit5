import math

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QInputDialog, QLabel, QTableWidgetItem, QWizardPage

from cc3d.twedit5.Plugins.CC3DProject.ui_interactiveplotpage import Ui_interactivePlotPage

try:
    import pyqtgraph as pg
except ImportError:
    pg = None


DEFAULT_X_AXIS_TITLE = "MonteCarlo Step (MCS)"
DEFAULT_X_VALUE = "mcs"
OTHER_SERIES_LABEL = "Other..."
CELL_TYPE_SERIES_PREFIX = "Cell count: "
DEFAULT_COLORS = ["red", "green", "blue", "magenta", "cyan", "yellow", "white"]


class InteractivePlotPage(QWizardPage):
    """Wizard page that collects PyQtGraph plot window configuration."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_interactivePlotPage()
        self.ui.setupUi(self)
        self.cell_types = []
        self.plots = []
        self.current_plot_index = -1
        self._loading_plot = False
        self._custom_series_names = []

        self._setup_preview()
        self._connect_signals()
        self.ui.xValueLE.setText(DEFAULT_X_VALUE)
        self.set_cell_types(["Medium"])
        self.add_plot()

    def _setup_preview(self):
        if pg is None:
            self.preview_widget = QLabel("PyQtGraph is not available in this environment.")
            self.preview_widget.setAlignment(Qt.AlignCenter)
        else:
            self.preview_widget = pg.PlotWidget()
            self.preview_widget.showGrid(x=True, y=True)
            self.preview_widget.setBackground(QColor(245, 245, 245))
        self.ui.previewLayout.addWidget(self.preview_widget)

    def _connect_signals(self):
        self.ui.addPlotPB.clicked.connect(self.on_add_plot_clicked)
        self.ui.removePlotPB.clicked.connect(self.on_remove_plot_clicked)
        self.ui.addSeriesPB.clicked.connect(self.on_add_series_clicked)
        self.ui.removeSeriesPB.clicked.connect(self.on_remove_series_clicked)
        self.ui.plotListWidget.currentRowChanged.connect(self.on_plot_selection_changed)
        self.ui.titleLE.textChanged.connect(self.on_plot_field_changed)
        self.ui.xAxisTitleLE.textChanged.connect(self.on_plot_field_changed)
        self.ui.yAxisTitleLE.textChanged.connect(self.on_plot_field_changed)
        self.ui.xLogScaleCB.toggled.connect(self.on_plot_field_changed)
        self.ui.yLogScaleCB.toggled.connect(self.on_plot_field_changed)
        self.ui.showLegendCB.toggled.connect(self.on_plot_field_changed)

    def set_cell_types(self, cell_types):
        self.cell_types = list(cell_types)
        current_text = self.ui.yValueCB.currentText()
        self.ui.yValueCB.blockSignals(True)
        self.ui.yValueCB.clear()
        for cell_type in self.cell_types:
            self.ui.yValueCB.addItem(CELL_TYPE_SERIES_PREFIX + cell_type, {"type": "cell_type", "name": cell_type})
        for custom_name in self._custom_series_names:
            self.ui.yValueCB.addItem(custom_name, {"type": "custom", "name": custom_name})
        self.ui.yValueCB.addItem(OTHER_SERIES_LABEL, {"type": "other"})
        index = self.ui.yValueCB.findText(current_text)
        if index >= 0:
            self.ui.yValueCB.setCurrentIndex(index)
        self.ui.yValueCB.blockSignals(False)

    def add_plot(self):
        plot_number = len(self.plots) + 1
        plot = {
            "title": f"Plot {plot_number}",
            "x_axis_title": DEFAULT_X_AXIS_TITLE,
            "y_axis_title": "",
            "x_scale": "linear",
            "y_scale": "linear",
            "legend": True,
            "series": []
        }
        self.plots.append(plot)
        self.ui.plotListWidget.addItem(plot["title"])
        self.ui.plotListWidget.setCurrentRow(len(self.plots) - 1)

    def _current_plot(self):
        if 0 <= self.current_plot_index < len(self.plots):
            return self.plots[self.current_plot_index]
        return None

    def _load_plot(self, index):
        self._loading_plot = True
        plot = self._current_plot()
        enabled = plot is not None
        self.ui.plotParamsGB.setEnabled(enabled)
        self.ui.seriesGB.setEnabled(enabled)
        if plot is None:
            self._loading_plot = False
            return

        self.ui.titleLE.setText(plot["title"])
        self.ui.xAxisTitleLE.setText(plot["x_axis_title"])
        self.ui.yAxisTitleLE.setText(plot["y_axis_title"])
        self.ui.xLogScaleCB.setChecked(plot["x_scale"] == "log")
        self.ui.yLogScaleCB.setChecked(plot["y_scale"] == "log")
        self.ui.showLegendCB.setChecked(plot["legend"])
        self._fill_series_table(plot["series"])
        self._loading_plot = False
        self._update_preview()

    def _save_current_plot(self):
        plot = self._current_plot()
        if plot is None:
            return
        title = self.ui.titleLE.text().strip() or f"Plot {self.current_plot_index + 1}"
        plot["title"] = title
        plot["x_axis_title"] = self.ui.xAxisTitleLE.text().strip() or DEFAULT_X_AXIS_TITLE
        plot["y_axis_title"] = self.ui.yAxisTitleLE.text().strip()
        plot["x_scale"] = "log" if self.ui.xLogScaleCB.isChecked() else "linear"
        plot["y_scale"] = "log" if self.ui.yLogScaleCB.isChecked() else "linear"
        plot["legend"] = self.ui.showLegendCB.isChecked()
        plot["series"] = self._series_from_table()
        item = self.ui.plotListWidget.item(self.current_plot_index)
        if item is not None:
            item.setText(title)

    def _fill_series_table(self, series):
        self.ui.seriesTable.setRowCount(0)
        for entry in series:
            self._append_series_row(entry)

    def _append_series_row(self, entry):
        row = self.ui.seriesTable.rowCount()
        self.ui.seriesTable.insertRow(row)
        values = [entry["name"], entry["x"], entry["y"]]
        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.ui.seriesTable.setItem(row, column, item)

    def _series_from_table(self):
        series = []
        for row in range(self.ui.seriesTable.rowCount()):
            name = self.ui.seriesTable.item(row, 0).text()
            x_value = self.ui.seriesTable.item(row, 1).text()
            y_value = self.ui.seriesTable.item(row, 2).text()
            source_type = "cell_type" if y_value in self.cell_types else "custom"
            series.append({"name": name, "x": x_value, "y": y_value, "source_type": source_type})
        return series

    def _update_preview(self):
        if pg is None:
            return
        self.preview_widget.clear()
        plot = self._current_plot()
        if plot is None:
            return
        self.preview_widget.setTitle(plot["title"])
        self.preview_widget.setLabel("bottom", plot["x_axis_title"])
        self.preview_widget.setLabel("left", plot["y_axis_title"])
        self.preview_widget.setLogMode(x=plot["x_scale"] == "log", y=plot["y_scale"] == "log")
        x_values = list(range(1, 11)) if plot["x_scale"] == "log" else list(range(0, 10))
        for index, entry in enumerate(plot["series"] or [{"name": "series"}]):
            y_values = [max(1, i + index + 1) if plot["y_scale"] == "log" else math.sin(i / 2.0) + index
                        for i in x_values]
            pen = pg.mkPen(DEFAULT_COLORS[index % len(DEFAULT_COLORS)], width=2)
            self.preview_widget.plot(x_values, y_values, pen=pen, name=entry["name"])

    @pyqtSlot()
    def on_add_plot_clicked(self):
        self._save_current_plot()
        self.add_plot()

    @pyqtSlot()
    def on_remove_plot_clicked(self):
        row = self.ui.plotListWidget.currentRow()
        if row < 0 or len(self.plots) <= 1:
            return
        self.plots.pop(row)
        self.ui.plotListWidget.takeItem(row)
        self.ui.plotListWidget.setCurrentRow(min(row, len(self.plots) - 1))

    @pyqtSlot(int)
    def on_plot_selection_changed(self, row):
        if self._loading_plot:
            return
        self._save_current_plot()
        self.current_plot_index = row
        self._load_plot(row)

    @pyqtSlot()
    def on_plot_field_changed(self):
        if self._loading_plot:
            return
        self._save_current_plot()
        self._update_preview()

    @pyqtSlot()
    def on_add_series_clicked(self):
        plot = self._current_plot()
        if plot is None:
            return
        data = self.ui.yValueCB.currentData()
        if data is None:
            return
        if data.get("type") == "other":
            name, accepted = QInputDialog.getText(self, "User Defined Data Series", "Y data series name:")
            name = name.strip()
            if not accepted or not name:
                return
            if name not in self._custom_series_names:
                self._custom_series_names.append(name)
                insert_index = max(0, self.ui.yValueCB.count() - 1)
                self.ui.yValueCB.insertItem(insert_index, name, {"type": "custom", "name": name})
            y_value = name
            source_type = "custom"
        else:
            y_value = data["name"]
            source_type = data["type"]
        x_value = self.ui.xValueLE.text().strip() or DEFAULT_X_VALUE
        name = y_value if source_type == "custom" else f"{y_value} count"
        entry = {"name": name, "x": x_value, "y": y_value, "source_type": source_type}
        plot["series"].append(entry)
        self._append_series_row(entry)
        self._update_preview()

    @pyqtSlot()
    def on_remove_series_clicked(self):
        row = self.ui.seriesTable.currentRow()
        if row < 0:
            return
        self.ui.seriesTable.removeRow(row)
        self._save_current_plot()
        self._update_preview()

    def get_plot_data(self):
        self._save_current_plot()
        return [
            {
                "title": plot["title"],
                "x_axis_title": plot["x_axis_title"],
                "y_axis_title": plot["y_axis_title"],
                "x_scale": plot["x_scale"],
                "y_scale": plot["y_scale"],
                "legend": plot["legend"],
                "series": list(plot["series"])
            }
            for plot in self.plots
            if plot["series"]
        ]
