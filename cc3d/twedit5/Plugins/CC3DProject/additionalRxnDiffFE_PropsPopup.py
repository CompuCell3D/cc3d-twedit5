import sys
from PyQt5.QtWidgets import (
    QApplication, QWizard, QWizardPage, QVBoxLayout, QPushButton,
    QDialog, QBoxLayout, QGroupBox, QLineEdit, QDialogButtonBox, QLabel
)


# Popup form listing additional parameters used in Reaction Diffusion FE solver
class RxnDiffusionPropsPopupForm(QDialog):
    def __init__(self,  tab_idx: int = 0, parent=None):  # tab_idx for chemical field currently not used.
        super().__init__(parent)
        self.setWindowTitle("Additional Reaction Diffusion FE properties")

        # Layout and form
        self.main_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.reaction_diff_descr_label = QLabel("Additional term can be an expression involving field name and CellType. See "
                                           "muParser and CC3D documentation for valid mathematical expressions.")
        self.reaction_diff_descr_label.setWordWrap(True)
        self.main_layout.addWidget(self.reaction_diff_descr_label)

        self.additional_eq_term_label = QLabel("Additional reaction term:")
        self.main_layout.addWidget(self.additional_eq_term_label)
        self.additional_eq_term_lineEdit = QLineEdit()
        self.additional_eq_term_lineEdit.setPlaceholderText("1 * chemField + CellType")
        self.main_layout.addWidget(self.additional_eq_term_lineEdit)

        self.extra_set_group = QGroupBox()
        self.extra_set_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.mcs_descr_label = QLabel(
            "To run solver for large diffusion constants you typically call the solver multiple times "
            "- to specify additional calls to the solver in each MCS:")
        self.mcs_descr_label.setWordWrap(True)
        self.extra_set_layout.addWidget(self.mcs_descr_label)

        self.extra_times_mcs_group = QGroupBox("")
        self.extra_times_mcs_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.extra_mcs_label = QLabel("Extra times per MCS:")
        self.extra_times_mcs_layout.addWidget(self.extra_mcs_label)
        self.extra_mcs_lineEdit = QLineEdit("0")
        self.extra_times_mcs_layout.addWidget(self.extra_mcs_lineEdit)
        self.extra_times_mcs_group.setLayout(self.extra_times_mcs_layout)
        self.extra_set_layout.addWidget(self.extra_times_mcs_group)

        self.extra_deltaX_group = QGroupBox("")
        self.extra_deltaX_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.extra_deltaX_label = QLabel("Delta X:")
        self.extra_deltaX_layout.addWidget(self.extra_deltaX_label)
        self.extra_deltaX_lineEdit = QLineEdit("1.0")
        self.extra_deltaX_layout.addWidget(self.extra_deltaX_lineEdit)
        self.extra_deltaX_group.setLayout(self.extra_deltaX_layout)
        self.extra_set_layout.addWidget(self.extra_deltaX_group)

        self.extra_deltaT_group = QGroupBox("")
        self.extra_deltaT_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.extra_deltaT_label = QLabel("Delta T:")
        self.extra_deltaT_layout.addWidget(self.extra_deltaT_label)
        self.extra_deltaT_lineEdit = QLineEdit("1.0")
        self.extra_deltaT_layout.addWidget(self.extra_deltaT_lineEdit)
        self.extra_deltaT_group.setLayout(self.extra_deltaT_layout)
        self.extra_set_layout.addWidget(self.extra_deltaT_group)

        self.extra_set_group.setLayout(self.extra_set_layout)
        self.main_layout.addWidget(self.extra_set_group)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.main_layout.addWidget(buttons)
        self.setLayout(self.main_layout)

    def get_data(self) -> dict[str, str]:
        data: dict[str, str] = {}
        data["AdditionalTerm"] = self.additional_eq_term_lineEdit.text()
        data["ExtraTimesPerMCS"] = self.extra_mcs_lineEdit.text()
        data["DeltaX"] = self.extra_deltaX_lineEdit.text()
        data["DeltaT"] = self.extra_deltaT_lineEdit.text()
        return data

    def set_data(self, data: dict[str, str]):
        for key in data:
            if key == "AdditionalTerm":
                self.additional_eq_term_lineEdit.setText(data[key])
            elif key == "ExtraTimesPerMCS":
                self.extra_mcs_lineEdit.setText(data[key])
            elif key == "DeltaX":
                self.extra_deltaX_lineEdit.setText(data[key])
            elif key == "DeltaT":
                self.extra_deltaT_lineEdit.setText(data[key])

