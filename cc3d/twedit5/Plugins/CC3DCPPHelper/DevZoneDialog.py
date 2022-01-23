cc3d_core_conda_utils_installed = True

try:
    from cc3d.core.utils import find_conda, find_current_conda_env
    from cc3d.core.developer_zone.developer_zone_config import configure_developer_zone
except ImportError:
    cc3d_core_conda_utils_installed = False

from cc3d.twedit5.twedit.utils.global_imports import *
from pathlib import Path
import re
from . import ui_dev_zone

MAC = "qt_mac_set_native_menubar" in dir()


class DevZoneDialog(QDialog, ui_dev_zone.Ui_DevZoneDlg):
    def __init__(self, parent=None):

        super(DevZoneDialog, self).__init__(parent)

        self.__ui = parent

        # there are issues with Drawer dialog not getting focus when being displayed on linux
        # they are also not positioned properly so, we use "regular" windows

        if sys.platform.startswith('win'):
            self.setWindowFlags(Qt.Drawer)  # dialogs without context help - only close button exists

        self.projectPath = ""
        self.setupUi(self)
        self.dev_zone_status_TE.setText('To configure Developer Zone for compilation please select CC3D GIT '
                                        'and build directories and click "Configure" ')

    @pyqtSlot()
    def on_cc3d_git_browse_PB_clicked(self):
        cc3d_git_dir = QFileDialog.getExistingDirectory(parent=self, caption="CC3D GIT Dir")
        if cc3d_git_dir:
            self.cc3d_git_dir_LE.setText(cc3d_git_dir)

    @pyqtSlot()
    def on_build_dir_browse_PB_clicked(self):
        build_dir = QFileDialog.getExistingDirectory(parent=self, caption="Build Directory (compiler work dir)")
        if build_dir:
            self.build_dir_LE.setText(build_dir)

    @pyqtSlot()  # signature of the signal emited by the button
    def on_configurePB_clicked(self):

        error_flag = False
        cc3d_git_dir = Path(self.cc3d_git_dir_LE.text())
        build_dir = Path(self.build_dir_LE.text())
        if not all ((cc3d_git_dir, build_dir)):
            self.dev_zone_status_TE.setText(
                "Both CC3D_GIT and build directory (compiler working dir) must be set"
            )
            return
        else:
            if cc3d_git_dir.exists() and build_dir.exists():

                self.dev_zone_status_TE.setText('Please Wait While I Configure Developer Zone For Compilation')
                try:
                    output = configure_developer_zone(cc3d_git_dir=cc3d_git_dir, build_dir=build_dir)
                    if sys.platform.startswith('win'):
                        msg = f'\n\n Now open a terminal and do the following:\n' \
                              f'cd {build_dir}\n' \
                              f'nmake\n' \
                              f'nmake install'
                    else:
                        msg = f'\n\n Now open a terminal and do the following:\n' \
                              f'cd {build_dir}\n' \
                              f'make\n' \
                              f'make install'


                    self.dev_zone_status_TE.setText(output + msg)
                except FileExistsError as e:
                    self.dev_zone_status_TE.setText(f'{e}')
                    return
            else:
                self.dev_zone_status_TE.setText(
                    "Both CC3D_GIT and build directory (compiler working dir) must be set and "
                    "point to existing directories"
                )

            return

        if not error_flag:
            self.accept()

