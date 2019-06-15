from PyQt5.QtWidgets import QDialog


class SubjectDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(SubjectDialog, self).__init__(*args, **kwargs)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Subject')
