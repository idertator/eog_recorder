from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtWidgets import QVBoxLayout


_HTML = '''
<!DOCTYPE HTML>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style>
            h1 {
                text-align: center;
            }
        </style>        
    </head>
    <body>
        <h1>Proyecto DIATAX</h1>

        <ol>
            <li>Gonzalo Joya Caparrós (UMA), <strong>Coordinador General</strong></li>
            <li>Rodolfo García (UTM), <strong>Coordinador UTM</strong></li>
            <li>Roberto Becerra (UMA), <strong>Desarrollador Principal</strong></li>
            <li>Wilmer Cedeño (UTM), <strong>Desarrollador</strong></li>
            <li>Mauro Ferrín (UTM), <strong>Desarrollador</strong></li>
            <li>Rodolfo Becerra (UHO), <strong>Desarrollador</strong></li>            
            <li>Luis Velázquez Rodríguez (CIRAH), <strong>Asesor Principal</strong></li>
            <li>Roberto Rodríguez Labrada (CIRAH), <strong>Asesor</strong></li>
        </ol>

        <br>

        <p>Proyecto resultado de la colaboración entre la Universidad de Málaga (España),
        el Instituto Tecnológico de Manabí (Ecuador) y el Centro de Investigación y 
        Rehabilitación de las Ataxias Hereditarias (Cuba)<p/>
    </body>
</html>
'''


class AboutDialog(QDialog):
    
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.setWindowTitle('Acerca de DIATAX ...')
        self.setFixedWidth(640)
        self.setFixedHeight(400)

        main_layout = QVBoxLayout()

        credits_text = QTextEdit()
        credits_text.setHtml(_HTML)
        credits_text.setReadOnly(True)
        credits_text.setTextInteractionFlags(Qt.NoTextInteraction)

        main_layout.addWidget(credits_text)

        self.setLayout(main_layout)
