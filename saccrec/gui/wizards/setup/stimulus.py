from PyQt5 import QtWidgets

from saccrec import settings
from saccrec.gui.stimulus import StimulusWidget, TestStimulusWidget, InitialStimulusWidget, FinalStimulusWidget


_TEST_HTML = '''<p>{name} {of_str} <b>{angle}&#176;</b> {with_str} <b>{saccades_count}</b> {saccades_str}.
{duration_str} <b>{fixation_duration} {seconds_str}</b> {variability_str} <b>{fixation_variability}%</b>.</p>'''


class StimulusWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent):
        super(StimulusWizardPage, self).__init__(parent)

        self.setTitle(_('Configuración del estímulo'))

        scroll_area = QtWidgets.QScrollArea()
        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_layout = QtWidgets.QVBoxLayout()

        layout = QtWidgets.QVBoxLayout()
        self.test_widget_list = list()
        test_layout = QtWidgets.QVBoxLayout()

        self.initial_calibration_test = InitialStimulusWidget(
            settings.tests.initial_calibration,
            self.test_widget_list,
            test_layout
        )
        scroll_area_layout.addWidget(self.initial_calibration_test)

        test_list = settings.tests.tests['tests']
        cont = 0
        for test in test_list:
            stimulus_widget = TestStimulusWidget(self.test_widget_list, test_layout, cont, test)
            test_layout.addWidget(stimulus_widget)
            self.test_widget_list.append(stimulus_widget)
            cont += 1

        scroll_area_layout.addLayout(test_layout)

        self.final_calibration_test = FinalStimulusWidget(
            settings.tests.final_calibration
        )
        scroll_area_layout.addWidget(self.final_calibration_test)

        scroll_area.setWidgetResizable(True)
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    @property
    def html(self) -> str:
        text = '<h4>{title}</h4>'.format(
            title=_('Estímulos')
        )
        text += self._test_to_html(self.initial_calibration_test)
        for test in self.test_widget_list:
            text += self._test_to_html(test)
        text += self._test_to_html(self.final_calibration_test)
        return text

    @staticmethod
    def _test_to_html(test: StimulusWidget) -> str:
        name = test.test_name
        if type(test) is TestStimulusWidget:
            name = _('Prueba sacádica')

        return _TEST_HTML.format(
            name=name,
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
        json = {
            'initial_calibration': self.initial_calibration_test.json,
            'final_calibration': self.final_calibration_test.json,
        }
        test_list = list()
        for test in self.test_widget_list:
            test_list.append(test.json)
        json.setdefault('tests', test_list)
        return json

    @property
    def max_angle(self) -> float:
        return float(max(max(test.angle for test in self.test_widget_list), self.initial_calibration_test.angle,
                         self.final_calibration_test.angle))

    def save(self):
        settings.tests.tests = self.json
