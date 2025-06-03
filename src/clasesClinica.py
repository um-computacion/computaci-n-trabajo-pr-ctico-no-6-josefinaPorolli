from datetime import datetime # Se importa datetime para manejar fechas y horas
from exceptions import * # Se importan las excepciones

class Paciente: 
    # CONSTRUCTOR
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        self.__dni__ = dni
        self.__nombre__ = nombre
        self.__fecha_nacimiento__ = fecha_nacimiento

    # getters
    def obtener_dni(self) -> str:
        return self.__dni__
    
    # representación
    def __str__(self):
        return f'Paciente: {self.__nombre__}\n DNI: {self.__dni__}\n Fecha de Nacimiento: {self.__fecha_nacimiento__}'
    
class Especialidad:
    # CONSTRUCTOR
    def __init__(self, nombre:str, dias: list[str]):
        self.__nombre__ = nombre
        self.__dias__ = dias
    
    # getters
    def obtener_especialidad(self) -> str:
        return self.__nombre__
    
     # validación
    def verificar_dia(self, dia: str) -> bool: # devuelve true si la especialidad está disponible en el día indicado
        return dia in self.__dias__
    
    # representación
    def __str__(self):
        dias_str = ', '.join(self.__dias__)
        return f'Especialidad: {self.__nombre__}\n Días disponibles: {dias_str}'
    
class Medico: 
    # CONSTRUCTOR
    def __init__(self, matricula: str, nombre: str, especialidad: str):
        self.__matricula__ = matricula
        self.__nombre__ = nombre
        self.__especialidad__ = especialidad

    # getters
    def obtener_matricula(self) -> str:
        return self.__matricula__
    
    # representación
    def __str__(self):
        return f'MÉDICO\nMatrícula del médico: {self.__matricula__}\n Nombre: {self.__nombre__}\n Especialidad: {self.__especialidad__}'
    
class Turno:
    # CONSTRUCTOR
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime):
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
    
    # getters
    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora__
    
    # representación
    def __str__(self):
        return f'Turno:\n Paciente: {self.__paciente__}\n Médico: {self.__medico__}\n Fecha y Hora: {self.__fecha_hora__.strftime("%d/%m/%Y %H:%M")}'
    
class Receta:
    # CONSTRUCTOR
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str], fecha:datetime):
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = fecha
    
    # representación
    def __str__(self):
        medicamentos_str = ', '.join(self._medicamentos) # Convierte la lista de medicamentos a una cadena de medicamentos separados por comas
        if not medicamentos_str:
            medicamentos_str = 'Ninguno' # en caso de que la lista de medicamentos esté vacía
        return (f'Receta:\n Paciente: {self.__paciente__}\n Médico: {self.__medico__}\n '
                f'Medicamentos: {medicamentos_str}\n Fecha: {self.__fecha__.strftime("%d/%m/%Y")}')
    
class HistoriaClinica:
    # CONSTRUCTOR
    def __init__(self, paciente: Paciente, turnos: list[Turno], recetas: list[Receta]):
        self.__paciente__ = paciente
        self.__turnos__ = turnos
        self.__recetas__ = recetas

    # setters
    def agregar_turno(self, turno: Turno):
        self.__turnos__.append(turno)
    
    def agregar_receta(self, receta: Receta):
        self.__recetas__.append(receta)
    
    # getters
    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos__
    
    def obtener_recetas(self) -> list[Receta]:
        return self.__recetas__
    
    # representación
    def __str__(self):
        turnos_str = '\n'.join(str(turno) for turno in self.__turnos__) if self.__turnos__ else 'Ninguno'
        recetas_str = '\n'.join(str(receta) for receta in self.__recetas__) if self.__recetas__ else 'Ninguna' # mismo caso que en la clase Receta
        return (f'Historia Clínica de {self.__paciente__}\n'
                f'Turnos:\n{turnos_str}\n'
                f'Recetas:\n{recetas_str}')
    
class Clinica:
    # CONSTRUCTOR
    def __init__(self, pacientes: dict[str, Paciente], medicos: dict[str, Medico], turnos: list[Turno], historias_clinicas: dict[str, HistoriaClinica]):
        self.__pacientes__ = pacientes
        self.__medicos__ = medicos
        self.__turnos__ = turnos
        self.__historias_clinicas__ = historias_clinicas

    # Registro de datos
    def agregar_paciente(self, paciente: Paciente):
        if paciente.obtener_dni() not in self.__pacientes__: #verifica si el paciente ya existe para no repetir claves (DNI)
            self.__pacientes__[paciente.obtener_dni()] = paciente
        else:
            raise ValueError(f'El paciente con DNI {paciente.obtener_dni()} ya existe.')
    
    def agregar_medico(self, medico: Medico):
        if medico.obtener_matricula() not in self.__medicos__: # verifica si el médico ya existe para no repetir claves (Matrícula)
            self.__medicos__[medico.obtener_matricula()] = medico
        else:
            raise ValueError(f'El médico con matrícula {medico.obtener_matricula()} ya existe.')
        
    def agendar_turno(self, dni:str, matricula:str, fecha_hora: datetime):
        
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        turno = Turno(paciente, medico, fecha_hora)
        self.__turnos__.append(turno) 
        
        if dni not in self.__historias_clinicas__:
            self.__historias_clinicas__[dni] = HistoriaClinica(paciente, [], [])
        
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str], fecha: datetime):
        if dni not in self.__pacientes__:
            raise ValueError(f'El paciente con DNI {dni} no existe.')
        if matricula not in self.__medicos__:
            raise ValueError(f'El médico con matrícula {matricula} no existe.')
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        fecha = datetime.now() # Se obtiene la fecha y hora actual para agregar a la receta
        receta = Receta(paciente, medico, medicamentos, fecha)
        self.__historias_clinicas__[dni].agregar_receta(receta)
        return receta
    
    # Acceso a información
    def obtener_pacientes(self) -> list[Paciente]:
        return self.__pacientes__
    
    def obtener_medicos(self) -> list[Medico]:
        return self.__medicos__
    
    def obtener_medico_por_matricula(self, matricula:str) -> Medico:
        if matricula in self.__medicos__: # Vertifica si el médico existe
            return self.__medicos__[matricula]
        else:
            raise MedicoNoExisteError(matricula) # Si no existe, lanza una excepción
        
    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos__
    
    def obtener_historia_clinica_por_dni(self, dni: str) -> HistoriaClinica:
        if dni in self.__historias_clinicas__: # Verifica si el paciente existe
            return self.__historias_clinicas__[dni]
        else:
            raise PacienteNoExisteError(dni) # Si no existe, lanza una excepción
        
    # Validaciones y utilidades
    def validar_existencia_paciente(self, dni: str) -> bool: # verifica si el paciente está registrado
        if dni in self.__pacientes__:
            return True
        else:
            raise PacienteNoExisteError(dni) # Podría solo tirar false, pero queda más bonita mi excepción je
        
    def validar_existencia_medico(self, matricula: str) -> bool: # verifica si el médico está registrado
        if matricula in self.__medicos__:
            return True
        else:
            raise MedicoNoExisteError(matricula)
        
    def validar_turno_no_duplicado(self, fecha_hora: datetime) -> bool: # verifica si un turno es válido y no está duplicado
        for turno in self.__turnos__:
            if turno.obtener_fecha_hora() == fecha_hora:
                raise TurnoDuplicadoError(fecha_hora)
            else:
                return True
            
    def obtener_dia_semana_en_espanol(self, fecha: datetime) -> str: # traduce un objeto datetime a un día de la semana en español
        dias_semana = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo'
        }
        return dias_semana[fecha.weekday()]
    
    def obtener_especialidad_disponible(self, medico:Medico, dia_semana:str) -> str: # obtiene la especialidad disponible para un médico en un día específico
        especialidad = medico.obtener_especialidad()
        if especialidad.verificar_dia(dia_semana):
            return especialidad.obtener_especialidad()
        else:
            raise ValueError(f'La especialidad {especialidad.obtener_especialidad()} no está disponible el {dia_semana}.')
        
    def validar_especialidad_en_dia(self, medico: Medico, dia_semana: str) -> bool: # verifica que el médico atienda esa especialidad en ese día
        especialidad = medico.obtener_especialidad()
        if especialidad.verificar_dia(dia_semana):
            return True
        else:
            raise ValueError(f'El médico {medico.obtener_matricula()} no tiene turnos disponibles para la especialidad {especialidad.obtener_especialidad()} el {dia_semana}.')
        
    