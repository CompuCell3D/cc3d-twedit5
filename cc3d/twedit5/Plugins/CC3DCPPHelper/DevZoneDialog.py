cc3d_core_conda_utils_installed = True

try:
    from cc3d.core.utils import find_conda, find_current_conda_env
    from cc3d.core.developer_zone.developer_zone_config import (
        configure_developer_zone,
        get_conda_specs,
        get_windows_cmake_generator_options
    )
except ImportError:
    cc3d_core_conda_utils_installed = False

FALLBACK_WINDOWS_CMAKE_GENERATORS = (
    {
        'label': 'Visual Studio 2019 x64 (default)',
        'generator': 'Visual Studio 16 2019',
    },
    {
        'label': 'NMake Makefiles',
        'generator': 'NMake Makefiles',
    },
    {
        'label': 'Visual Studio 2015 x64',
        'generator': 'Visual Studio 14 2015',
    },
    {
        'label': 'Visual Studio 2026 x64',
        'generator': 'Visual Studio 18 2026',
    },
)

from multiprocessing.pool import ThreadPool
from cc3d.twedit5.twedit.utils.global_imports import *
from pathlib import Path
import re
from . import ui_dev_zone
import shutil

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
        self.configure_windows_cmake_generator_controls()
        self.dev_zone_status_TE.setText('To configure Developer Zone for compilation please select CC3D GIT '
                                        'and build directories and click "Configure" ')

    def configure_windows_cmake_generator_controls(self):
        is_windows = sys.platform.startswith('win')
        self.win_cmake_generator_label.setVisible(is_windows)
        self.win_cmake_generator_CB.setVisible(is_windows)
        if not is_windows:
            return

        self.win_cmake_generator_CB.clear()
        try:
            generator_options = get_windows_cmake_generator_options()
        except NameError:
            generator_options = FALLBACK_WINDOWS_CMAKE_GENERATORS

        for generator_specs in generator_options:
            self.win_cmake_generator_CB.addItem(generator_specs['label'], generator_specs['generator'])

    def selected_windows_cmake_generator(self):
        return {
            'label': self.win_cmake_generator_CB.currentText(),
            'generator': self.win_cmake_generator_CB.itemData(self.win_cmake_generator_CB.currentIndex())
        }

    @pyqtSlot()
    def on_cc3d_git_browse_PB_clicked(self):
        cc3d_git_dir = QFileDialog.getExistingDirectory(parent=self, caption="CC3D GIT Dir")
        if cc3d_git_dir:
            self.cc3d_git_dir_LE.setText(cc3d_git_dir)
            self.build_dir_LE.setText(cc3d_git_dir + '_dev_zone_build')

    @pyqtSlot()
    def on_build_dir_browse_PB_clicked(self):
        build_dir = QFileDialog.getExistingDirectory(parent=self, caption="Build Directory (compiler work dir)")
        if build_dir:
            self.build_dir_LE.setText(build_dir)

    @pyqtSlot()  # signature of the signal emitted by the button
    def on_configurePB_clicked(self):

        cc3d_git_dir = Path(self.cc3d_git_dir_LE.text())
        build_dir = Path(self.build_dir_LE.text())
        win_cmake_generator = self.selected_windows_cmake_generator()

        if not self.prep_build_dir(build_dir=build_dir):
            return

        if not all((cc3d_git_dir, build_dir)):
            self.dev_zone_status_TE.setText(
                "Both CC3D_GIT and build directory (compiler working dir) must be set"
            )
        else:
            if cc3d_git_dir.exists() and build_dir.exists():

                self.dev_zone_status_TE.setText('Please Wait While I Configure Developer Zone For Compilation')
                try:

                    self.worker = Worker(
                        cc3d_git_dir=cc3d_git_dir, build_dir=build_dir,
                        win_cmake_generator=win_cmake_generator
                    )
                    self.worker.started_config.connect(self.update_status)
                    self.worker.completed.connect(self.update_status)
                    self.worker.start()


                except FileExistsError as e:
                    self.dev_zone_status_TE.setText(f'{e}')
                    return
            else:
                self.dev_zone_status_TE.setText(
                    "Both CC3D_GIT and build directory (compiler working dir) must be set and "
                    "point to existing directories"
                )

    def prep_build_dir(self, build_dir: Path) -> bool:
        """
        checks if build dir is empty . Then lets user decide if the content should be removed or
        whether the used should select different directory
        :param build_dir:
        :return:
        """
        build_dir.mkdir(exist_ok=True, parents=True)
        build_dir_content = os.listdir(build_dir)
        if len(build_dir_content):
            ret = QMessageBox.question(self.__ui, 'Directory not empty',
                                       f'The build directory you selected '
                                       f'<br> <i>{build_dir}</i> <br>'
                                       f'is not empty.<br>Should I remove the content of this directory?',
                                       QMessageBox.Yes | QMessageBox.No
                                       )
            if ret == QMessageBox.No:
                self.update_status(msg='Please select an <b>empty</b> build directory')
                return False
            try:
                shutil.rmtree(build_dir)
            except OSError as e:
                self.update_status(
                    msg=f'Could not remove build directory <br><i>{build_dir}</i><br><br>'
                        f'{e}<br><br>'
                        f'Please close any programs using this directory, or select a different '
                        f'empty build directory.'
                )
                return False
            build_dir.mkdir(exist_ok=True, parents=True)
        return True

    def update_status(self, msg: str = ''):
        self.dev_zone_status_TE.setText(msg)


class Worker(QThread, QObject):
    # started = pyqtSignal()
    started_config = pyqtSignal(str)
    completed = pyqtSignal(str)

    def __init__(self, cc3d_git_dir, build_dir, win_cmake_generator=None):
        super().__init__()
        self.cc3d_git_dir = cc3d_git_dir
        self.build_dir = build_dir
        self.win_cmake_generator = win_cmake_generator

    def run(self):
        """Long-running task."""
        self.started_config.emit('Developer Zone Configuration Started - Please wait...')
        conda_specs = None
        try:
            conda_specs = get_conda_specs()
            output = configure_developer_zone(
                self.cc3d_git_dir, self.build_dir,
                win_cmake_generator=self.win_cmake_generator['generator'],
                conda_specs=conda_specs
            )
        except (RuntimeError, FileExistsError, Exception) as e:
            output = f'{e}'
            self.completed.emit(output)
            return

        errors, missing_lines = self.process_cmake_config_output(output=output)
        msg = self.build_post_config_message(errors=errors, missing_lines=missing_lines, output=output,
                                             build_dir=self.build_dir, win_cmake_generator=self.win_cmake_generator,
                                             conda_specs=conda_specs)

        self.completed.emit(msg)
        # output = self.how_to_compile_msg(build_dir=self.build_dir) + \
        #          '\n\nCmake Configuration Details' \
        #          '\n==========================\n\n' \
        #          + output
        #
        # self.completed.emit(output)

    def conda_activation_msg(self, conda_specs: dict = None) -> str:
        if not conda_specs:
            return 'Activate the conda environment used for Developer Zone configuration.'

        conda_exec = conda_specs.get('conda_exec')
        conda_env_name = conda_specs.get('conda_env_name')
        if sys.platform.startswith('win') and conda_exec:
            activate_script = Path(conda_exec).parent.joinpath('activate.bat')
            return f'call "{activate_script}"<br>conda activate {conda_env_name}'

        return f'conda activate {conda_env_name}'

    def how_to_compile_msg(self, build_dir: str, win_cmake_generator: dict = None, conda_specs: dict = None) -> str:

        if sys.platform.startswith('win'):
            conda_activation_msg = self.conda_activation_msg(conda_specs=conda_specs)
            generator_name = win_cmake_generator['generator'] if win_cmake_generator else None
            generator_label = win_cmake_generator['label'] if win_cmake_generator else 'Visual Studio'
            if generator_name == 'NMake Makefiles':
                build_cmd = f'nmake<br>' \
                            f'nmake install'
                msg = f'<br><br>Open a terminal and activate the same conda environment used for configuration:' \
                      f'<br><br>{conda_activation_msg}<br><br>' \
                      f'cd {build_dir}<br>' \
                      f'{build_cmd}'
            else:
                msg = f'<br><br>Open the generated project in {generator_label} and build the ' \
                      f'<b>INSTALL</b> target using the <b>Release</b> configuration.' \
                      f'<br><br>As a backup, open a terminal and activate the same conda environment ' \
                      f'used for configuration:<br><br>' \
                      f'{conda_activation_msg}<br><br>' \
                      f'cd {build_dir}<br>' \
                      f'cmake --build . --config RelWithDebInfo --target install'
        elif sys.platform.startswith('darwin'):
            conda_activation_msg = self.conda_activation_msg(conda_specs=conda_specs)
            msg = f'<br><br>Open a terminal and activate the same conda environment ' \
                  f'used for configuration:<br><br>' \
                  f'{conda_activation_msg}<br><br>' \
                  f'cd {build_dir}<br>' \
                  f'make<br>' \
                  f'make install<br>' \
                  f'<br>The macOS SDK must be installed before compilation. ' \
                  f'This is a one-time setup task: install SDK 10.10 for x86 processors ' \
                  f'to /opt/MacOSX10.10.sdk, or SDK 11.3 for arm64 processors ' \
                  f'(M1, M2, etc.) to /opt/MacOSX11.3.sdk. ' \
                  f'You can get MacOSX10.10.sdk or MacOSX11.3.sdk from ' \
                  f'https://github.com/phracker/MacOSX-SDKs.<br>' \
                  f'<br>If compilation still picks up the wrong conda environment, ' \
                  f'use this fallback before activating the compile environment:<br>' \
                  f'conda deactivate base<br>'
        else:
            msg = f'<br><br>Now open a terminal and do the following:<br><br>' \
                  f'cd {build_dir}<br>' \
                  f'make<br>' \
                  f'make install'


        return msg

    def process_cmake_config_output(self, output):
        """
        parses output of cmake config and checks if errors have occurred.
        :param output:
        :return:
        """
        split_output = output.split('\n')
        errors = False
        missing_lines = []
        for line in split_output:
            if line.find('errors occurred') > -1:
                errors = True
            if line.lower().find('missing') > -1:
                missing_lines.append(line)

        return errors, missing_lines

    def build_post_config_message(
            self, errors, missing_lines, output, build_dir, win_cmake_generator=None, conda_specs=None
    ):
        msg = ''
        compile_msg = self.how_to_compile_msg(
            build_dir=build_dir, win_cmake_generator=win_cmake_generator, conda_specs=conda_specs
        )

        if errors:
            msg += '<b>Errors have occurred during Cmake configuration</b>.<br> ' \
                   'Please see the output of cmake config below and fix the issues<br>'
            msg += '<br><br><b><u>Cmake Configuration Details:</u></b><br><br>' + output.replace('\n', '<br>')
            return msg
        elif len(missing_lines):
            msg += f'<b>Missing libraries/headers detected during Cmake configuration</b>.<br> ' \
                   f'THe compilation may or may not work depending on which package is missing:<br><br>' \
                   f'{"<br>".join(missing_lines)}<br><br>' \
                   f'You may also try running <b>CompuCell3D/conda-shell.sh</b> ' \
                   f'in the terminal before launching Twedit<br>' \
                   f'<br><b>Steps to compile:</b><br>{compile_msg}' \
                   '<br><br>Please see the output of cmake config below <br>'
            msg += '<br><br><b><u>Cmake Configuration Details:</u></b><br><br>' + output.replace('\n', '<br>')
        else:
            msg = f'<br><b>Steps to compile:</b><br>{compile_msg}' \
                  f'<br><br><b><u>Cmake Configuration Details:</u></b><br><br>' + output.replace('\n', '<br>')

        return msg
