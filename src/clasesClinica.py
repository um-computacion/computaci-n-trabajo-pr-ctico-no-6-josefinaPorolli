from datetime import datetime # Se importa datetime para manejar fechas y horas

class Paciente: 
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: str):
        self._dni = dni
        self._nombre = nombre
        self._fecha_nacimiento = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self._dni
    
    def __str__(self):
        return f'Paciente: {self._nombre}\n DNI: {self._dni}\n Fecha de Nacimiento: {self._fecha_nacimiento}'
    
class Medico: 
    def __init__(self, matricula: str, nombre: str, especialidad: str):
        self._matricula = matricula
        self._nombre = nombre
        self._especialidad = especialidad

    def obtener_matricula(self) -> str:
        return self._matricula
    
    def __str__(self):
        return f'MÉDICO\nMatrícula del médico: {self._matricula}\n Nombre: {self._nombre}\n Especialidad: {self._especialidad}'
    
class Turno:
    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime):
        self._paciente = paciente
        self._medico = medico
        self._fecha_hora = fecha_hora
    
    def obtener_fecha_hora(self) -> datetime:
        return self._fecha_hora
    
    def __str__(self):
        return f'Turno:\n Paciente: {self._paciente}\n Médico: {self._medico}\n Fecha y Hora: {self._fecha_hora.strftime("%d/%m/%Y %H:%M")}'
    
class Receta:
    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str], fecha:datetime):
        self._paciente = paciente
        self._medico = medico
        self._medicamentos = medicamentos
        self._fecha = fecha
    
    def __str__(self):
        medicamentos_str = ', '.join(self._medicamentos) # Convierte la lista de medicamentos a una cadena de medicamentos separados por comas
        if not medicamentos_str:
            medicamentos_str = 'Ninguno' # en caso de que la lista de medicamentos esté vacía
        return (f'Receta:\n Paciente: {self._paciente}\n Médico: {self._medico}\n '
                f'Medicamentos: {medicamentos_str}\n Fecha: {self._fecha.strftime("%d/%m/%Y")}')
    
class HistoriaClinica:
    def __init__(self, paciente: Paciente, turnos: list[Turno], recetas: list[Receta]):
        self._paciente = paciente
        self._turnos = turnos
        self._recetas = recetas

    def agregar_turno(self, turno: Turno):
        self._turnos.append(turno)
    
    def agregar_receta(self, receta: Receta):
        self._recetas.append(receta)
    
    def obtener_turnos(self) -> list[Turno]:
        return self._turnos
    
    def obtener_recetas(self) -> list[Receta]:
        return self._recetas
    
    def __str__(self):
        turnos_str = '\n'.join(str(turno) for turno in self._turnos) if self._turnos else 'Ninguno'
        recetas_str = '\n'.join(str(receta) for receta in self._recetas) if self._recetas else 'Ninguna' # mismo caso que en la clase Receta
        return (f'Historia Clínica de {self._paciente}\n'
                f'Turnos:\n{turnos_str}\n'
                f'Recetas:\n{recetas_str}')
    
class Clinica:
    def __init__(self, pacientes: dict[str, Paciente], medicos: dict[str, Medico], turnos: list[Turno], historias_clinicas: dict[str, HistoriaClinica]):
        self._pacientes = pacientes
        self._medicos = medicos
        self._turnos = turnos
        self._historias_clinicas = historias_clinicas

    def agregar_paciente(self, paciente: Paciente):
        if paciente.obtener_dni() not in self._pacientes: #verifica si el paciente ya existe para no repetir claves (DNI)
            self._pacientes[paciente.obtener_dni()] = paciente
        else:
            raise ValueError(f'El paciente con DNI {paciente.obtener_dni()} ya existe.')
    
    def agregar_medico(self, medico: Medico):
        if medico.obtener_matricula() not in self._medicos: # verifica si el médico ya existe para no repetir claves (Matrícula)
            self._medicos[medico.obtener_matricula()] = medico
        else:
            raise ValueError(f'El médico con matrícula {medico.obtener_matricula()} ya existe.')
        
    def agendar_turno(self, dni:str, matricula:str, fecha_hora: datetime):
        
        paciente = self._pacientes[dni]
        medico = self._medicos[matricula]
        turno = Turno(paciente, medico, fecha_hora)
        self._turnos.append(turno) 
        
        if dni not in self._historias_clinicas:
            self._historias_clinicas[dni] = HistoriaClinica(paciente, [], [])
        
        self._historias_clinicas[dni].agregar_turno(turno)

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str], fecha: datetime):
        if dni not in self._pacientes:
            raise ValueError(f'El paciente con DNI {dni} no existe.')
        if matricula not in self._medicos:
            raise ValueError(f'El médico con matrícula {matricula} no existe.')
        paciente = self._pacientes[dni]
        medico = self._medicos[matricula]
        fecha = datetime.now() # Se obtiene la fecha y hora actual para agregar a la receta
        receta = Receta(paciente, medico, medicamentos, fecha)
        self._historias_clinicas[dni].agregar_receta(receta)
        return receta
