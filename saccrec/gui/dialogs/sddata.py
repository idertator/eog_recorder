from PySide6 import QtWidgets, QtGui


class SDCardImport(QtWidgets.QDialog):

    def __init__(self, studies: list[str], parent=None):
        super(SDCardImport, self).__init__(parent)

        self.setWindowTitle(_('Import OpenBCI SD Signals'))
        self.setFixedSize(640, 480)

        self._input_folder_button = QtWidgets.QPushButton(_('Input Folder'))
        self._input_folder_button.setIcon(QtGui.QIcon(':/common/folder-open.svg'))
        self._input_folder_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self._input_path_label = QtWidgets.QLabel('')

        self._add_study_button = QtWidgets.QPushButton()
        self._add_study_button.setIcon(QtGui.QIcon(':/common/plus-square.svg'))
        self._add_study_button.setFixedSize(24, 24)

        self._del_study_button = QtWidgets.QPushButton()
        self._del_study_button.setIcon(QtGui.QIcon(':/common/minus-square.svg'))
        self._del_study_button.setFixedSize(24, 24)

        self._studies_list = QtWidgets.QListWidget()

        self._progress_bar = QtWidgets.QProgressBar()
        self._import_button = QtWidgets.QPushButton(_('Import'))
        self._import_button.setIcon(QtGui.QIcon(':/common/file-import.svg'))

        # Laying out the components

        self._top_layout = QtWidgets.QHBoxLayout()
        self._top_layout.addWidget(self._input_folder_button)
        self._top_layout.addWidget(self._input_path_label)
        self._top_layout.addWidget(self._add_study_button)
        self._top_layout.addWidget(self._del_study_button)

        self._bottom_layout = QtWidgets.QHBoxLayout()
        self._bottom_layout.addWidget(self._progress_bar)
        self._bottom_layout.addWidget(self._import_button)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._top_layout)
        self._layout.addWidget(self._studies_list)
        self._layout.addLayout(self._bottom_layout)

        self.setLayout(self._layout)

