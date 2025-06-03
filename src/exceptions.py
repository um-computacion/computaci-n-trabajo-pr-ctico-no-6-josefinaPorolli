class PacienteNoExisteError(Exception):
    def __init__(self, dni: str):
        super().__init__(f'El paciente con DNI {dni} no existe.')


class MedicoNoExisteError(Exception):
    def __init__(self, matricula: str):
        super().__init__(f'El médico con matrícula {matricula} no existe.')


class TurnoEnElPasadoError(Exception):
    def __init__(self):
        super().__init__('La fecha y hora del turno no puede ser en el pasado.')


class TurnoDuplicadoError(Exception):
    def __init__(self, fecha_hora):
        super().__init__(f'El médico ya tiene un turno asignado en ese horario ({fecha_hora}).')

class RecetaInvalidaError(Exception):
    def __init__(self):
        super().__init__(f'Receta inválida')
