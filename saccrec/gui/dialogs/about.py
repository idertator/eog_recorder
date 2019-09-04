from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTextBrowser
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget

_HTML = '''
<!DOCTYPE HTML>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <style>
            ul {
                list-style: none;
            }
            li {
                text-align: center;
            }
            .project {
                text-align: center;
                margin-top: 2em;
            }
        </style>        
    </head>
    <body>
        <ul>
            <li>Gonzalo Joya Caparrós (UMA), <strong>Coordinador General</strong></li>
            <li>Rodolfo García (UTM), <strong>Coordinador UTM</strong></li>
            <li>Roberto Becerra (UMA), <strong>Desarrollador Principal</strong></li>
            <li>Wilmer Cedeño (UTM), <strong>Desarrollador</strong></li>
            <li>Mauro Ferrín (UTM), <strong>Desarrollador</strong></li>
            <li>Rodolfo Becerra (UHO), <strong>Desarrollador</strong></li>            
            <li>Luis Velázquez Rodríguez (CIRAH), <strong>Asesor Principal</strong></li>
            <li>Roberto Rodríguez Labrada (CIRAH), <strong>Asesor</strong></li>
        </ul>

        <p class="project">Proyecto resultado de la colaboración entre la Universidad de Málaga (España),
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

        logo_svg = QSvgWidget(':diatax.svg')
        logo_svg.setFixedSize(183, 81)
        
        logo_layout = QHBoxLayout()    
        logo_layout.addStretch()    
        logo_layout.addWidget(logo_svg)
        logo_layout.addStretch()

        main_layout.addLayout(logo_layout)

        credits_text = QTextBrowser()
        credits_text.setHtml(_HTML)
        credits_text.setReadOnly(True)
        credits_text.setTextInteractionFlags(Qt.NoTextInteraction)
        credits_text.setStyleSheet("background: rgba(0, 0, 0, 0%)")

        main_layout.addWidget(credits_text)

        self.setLayout(main_layout)
