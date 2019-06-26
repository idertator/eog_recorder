import os

from saccrec.core.Patient import Patient

class Test:

    def __init__(self):
        self._patient = None
        self._stimulation_angle = 30 # angulo
        self._mean_duration = 3000 # milisegundos
        self._variation = 1000 # milisegundos
        self._test_duration = 60000 # un minuto
        self._output_path = os.getcwd()+'/LastTest.test'

    def save(self):
        # TODO: Esto se debe ejecutar cuando se finalize el QWizard
        pass

    @property
    def patient(self):
        return self._patient

    @property
    def stimulation_angle(self):
        return self._stimulation_angle
    
    @property
    def mean_duration(self):
        return self._mean_duration

    @property
    def variation(self):
        return self._variation

    @property
    def test_duration(self):
        return self._test_duration

    @property
    def output_file_path(self):
        return self._output_path

    # SETTERS

    @patient.setter
    def patient(self, patient : Patient):
        self._patient = patient
    
    @stimulation_angle.setter
    def stimulation_angle(self, angle : int):
        self._stimulation_angle = angle
    
    @mean_duration.setter
    def mean_duration(self, duration : int):
        self._mean_duration = duration

    @variation.setter
    def variation(self, duration : int):
        self._variation = duration

    @test_duration.setter
    def test_duration(self, duration: int):
        self._test_duration = duration

    @output_file_path.setter
    def output_file_path(self, path : str):
        self._output_path = path