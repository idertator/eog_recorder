from PyQt5 import QtWidgets

from saccrec import settings
from saccrec.core import workspace
from saccrec.core.study import Stimulus


_TEST_HTML = '''<p>{name} {of_str} <b>{angle}&#176;</b> {with_str} <b>{saccades_count}</b> {saccades_str}.
{duration_str} <b>{fixation_duration} {seconds_str}</b> {variability_str} <b>{fixation_variability}%</b>.</p>'''


class StimulusWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(StimulusWizardPage, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setTitle(_('Configuración del estímulo'))

        self._protocol = workspace.protocol
        self._protocol.setParent(self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._protocol)

        self.setLayout(layout)

    @property
    def html(self) -> str:
        text = '<h4>{title}</h4>'.format(
            title=_('Estímulos')
        )
        for test in self._protocol:
            text += self._test_to_html(test)
        return text

    @staticmethod
    def _test_to_html(test: Stimulus) -> str:
        return _TEST_HTML.format(
            name=test.name,
            of_str=_('a'),
            angle=test.angle,
            with_str=_('con'),
            saccades_count=test.saccades_count,
            saccades_str=_('sácadas'),
            duration_str=_('La duración media de las fijaciones es de'),
            fixation_duration=test.fixation_duration,
            seconds_str=_('segundos'),
            variability_str=_('con una variabilidad del'),
            fixation_variability=test.fixation_variability
        )

    @property
    def json(self) -> dict:
        return self._protocol.json
