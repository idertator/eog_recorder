from collections import defaultdict
from os.path import exists, join

from eoglib.io import load_eog, load_openbci, save_eog
from eoglib.models import Channel
from PySide6 import QtGui, QtWidgets

from saccrec import settings

_SD_NAMES = {
    'RECORDS',
    'OPENBCI'
}


class SDCardImport(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SDCardImport, self).__init__(parent)

        self._studies = []

        self.setWindowTitle(_('Import OpenBCI SD Signals'))
        self.setFixedSize(640, 480)

        self._input_folder_button = QtWidgets.QPushButton(_('Input Folder'))
        self._input_folder_button.setIcon(QtGui.QIcon(':/common/folder-open.svg'))
        self._input_folder_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._input_folder_button.pressed.connect(self._on_input_folder_button_clicked)

        self._input_path_label = QtWidgets.QLabel('')

        self._add_studies_button = QtWidgets.QPushButton()
        self._add_studies_button.setIcon(QtGui.QIcon(':/common/plus-square.svg'))
        self._add_studies_button.setFixedSize(24, 24)
        self._add_studies_button.pressed.connect(self._on_add_studies_button_clicked)

        self._del_studies_button = QtWidgets.QPushButton()
        self._del_studies_button.setIcon(QtGui.QIcon(':/common/minus-square.svg'))
        self._del_studies_button.setFixedSize(24, 24)
        self._del_studies_button.setEnabled(False)
        self._del_studies_button.pressed.connect(self._on_del_studies_button_clicked)

        self._studies_list = QtWidgets.QListWidget()
        self._studies_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._studies_list.itemSelectionChanged.connect(self._on_selection_changed)

        self._progress_bar = QtWidgets.QProgressBar()

        self._import_button = QtWidgets.QPushButton(_('Import'))
        self._import_button.setIcon(QtGui.QIcon(':/common/file-import.svg'))
        self._import_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._import_button.pressed.connect(self._on_import_button_clicked)

        # Laying out the components

        self._top_layout = QtWidgets.QHBoxLayout()
        self._top_layout.addWidget(self._input_folder_button)
        self._top_layout.addWidget(self._input_path_label)
        self._top_layout.addWidget(self._add_studies_button)
        self._top_layout.addWidget(self._del_studies_button)

        self._bottom_layout = QtWidgets.QHBoxLayout()
        self._bottom_layout.addWidget(self._progress_bar)
        self._bottom_layout.addWidget(self._import_button)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._top_layout)
        self._layout.addWidget(self._studies_list)
        self._layout.addLayout(self._bottom_layout)

        self.setLayout(self._layout)

    def open(self, studies: list[str] = []):
        if studies:
            for path in studies:
                if path not in self._studies:
                    self._studies.append(path)
            self._studies.sort()

        current_input_path = self._default_input_path
        self._input_path_label.setText(current_input_path)
        self._import_button.setEnabled(self._import_enabled)
        self._progress_bar.reset()

        super(SDCardImport, self).open()

    @property
    def _default_input_path(self) -> str:
        path = None
        with open('/proc/mounts', 'rt') as f:
            for line in f:
                if 'vfat' in line:
                    current_path = line.split()[1]
                    if current_path.split('/')[-1] in _SD_NAMES:
                        path = current_path
                        break

        if path is not None:
            return path

        return settings.gui.sd_path

    @property
    def _input_path(self) -> str:
        return self._input_path_label.text()

    @property
    def _import_enabled(self) -> bool:
        return len(self._studies) > 0 and exists(self._input_path)

    def _refresh_list(self):
        self._studies_list.clear()
        for study in self._studies:
            self._studies_list.addItem(study)

    def _on_input_folder_button_clicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            _('Select SD Data Location'),
            self._default_input_path
        )

        if path is not None:
            self._input_path_label.setText(path)
            settings.gui.sd_path = path

        self._import_button.setEnabled(self._import_enabled)

    def _on_add_studies_button_clicked(self):
        filenames, file_filter = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            _('Select studies to set channels data'),
            settings.gui.records_path,
            _('EOG Studies (*.eog)')
        )
        if filenames:
            for path in filenames:
                if path not in self._studies:
                    self._studies.append(path)

            self._studies.sort()
            self._refresh_list()

        self._import_button.setEnabled(self._import_enabled)

    def _on_del_studies_button_clicked(self):
        itemset = {
            item.text()
            for item in self._studies_list.selectedItems()
        }
        self._studies = [
            study
            for study in self._studies
            if study not in itemset
        ]
        self._refresh_list()
        self._import_button.setEnabled(self._import_enabled)

    def _on_import_button_clicked(self):
        msg = _('Importing %p%')
        self._progress_bar.setRange(0, len(self._studies))
        self._progress_bar.setFormat(msg)

        errors = defaultdict(list)
        input_path = self._input_path

        for index, study_path in enumerate(self._studies):
            study = load_eog(study_path)

            filenames = study.parameters.get('filenames', None)
            if filenames is not None:
                have_errors = False
                for filename in filenames:
                    if not exists(join(input_path, filename)):
                        errors[study_path].append(filename)
                        have_errors = True

                if not have_errors:
                    for filename, test in zip(filenames, study):
                        horizontal, vertical, stimulus = load_openbci(join(self._input_path, filename))
                        test[Channel.Horizontal] = horizontal
                        test[Channel.Vertical] = vertical
                        test[Channel.Stimulus] = stimulus

                    save_eog(study_path, study)

            self._progress_bar.setValue(index + 1)

        if errors:
            failed = len(errors)
            self._progress_bar.setFormat(_('Imported {success} studies, {failed} failed').format(
                success=len(self._studies) - failed,
                failed=failed
            ))
            error_message = _('The following studies present missing files:\n\n')
            error_list = []
            for path, study_errors in errors.items():
                error_list.append(
                    path + '\n' + '\n'.join((
                        _(' - {filename} missing!'.format(filename=filename))
                        for filename in study_errors
                    ))
                )

            QtWidgets.QMessageBox.critical(
                self,
                _('{failed} studies failed').format(failed=failed),
                error_message + '\n\n'.join(error_list)
            )
        else:
            self._progress_bar.setFormat(_('Imported {success} studies').format(
                success=len(self._studies)
            ))

    def _on_selection_changed(self):
        self._del_studies_button.setEnabled(len(self._studies_list.selectedItems()) > 0)
