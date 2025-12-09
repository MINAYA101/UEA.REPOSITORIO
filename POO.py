"""
Programa para calcular el promedio semanal del clima usando Programación Orientada a Objetos
Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import sys


def safe_input(prompt: str):
    """Entrada segura que captura EOFError/KeyboardInterrupt y muestra mensajes claros.

    Si la entrada no está disponible (por ejemplo cuando se ejecuta en un entorno
    no interactivo o en la Debug Console de VS Code), imprimimos una instrucción
    útil y salimos con código 1 para evitar que el programa quede esperando.
    """
    try:
        return input(prompt)
    except EOFError:
        print("\n[ERROR] Entrada no disponible. Ejecuta el script en un terminal interactivo (p. ej. PowerShell) usando:\n    python POO.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Ejecución interrumpida por el usuario.")
        sys.exit(1)


# Clase base que representa un día del clima
class DiaClima:
    """
    Clase que representa la información climática de un día.
    
    Atributos:
        _temperatura (float): Temperatura del día (encapsulado)
        _dia_semana (str): Nombre del día de la semana
    """
    
    # Diccionario de días de la semana
    DIAS_SEMANA = {
        1: "Lunes",
        2: "Martes", 
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
        7: "Domingo"
    }
    
    def __init__(self, numero_dia, temperatura=None):
        """
        Constructor de la clase DiaClima.
        
        Args:
            numero_dia (int): Número del día (1-7)
            temperatura (float, optional): Temperatura del día
        """
        self._temperatura = temperatura
        self._numero_dia = numero_dia
        self._dia_semana = self.DIAS_SEMANA.get(numero_dia, f"Día {numero_dia}")
    
    # Getter y Setter para temperatura (encapsulamiento)
    @property
    def temperatura(self):
        """Getter para la temperatura del día."""
        return self._temperatura
    
    @temperatura.setter
    def temperatura(self, valor):
        """
        Setter para la temperatura del día con validación.
        
        Args:
            valor (float): Nueva temperatura
        
        Raises:
            ValueError: Si la temperatura no es un número válido
        """
        try:
            self._temperatura = float(valor)
        except (ValueError, TypeError):
            raise ValueError("La temperatura debe ser un número válido")
    
    @property
    def dia_semana(self):
        """Getter para el nombre del día de la semana."""
        return self._dia_semana
    
    @property
    def numero_dia(self):
        """Getter para el número del día."""
        return self._numero_dia
    
    def mostrar_info(self):
        """
        Método para mostrar la información del día.
        
        Returns:
            str: Información formateada del día
        """
        if self._temperatura is not None:
            return f"{self._dia_semana}: {self._temperatura}°C"
        return f"{self._dia_semana}: Temperatura no registrada"
    
    def __str__(self):
        """Representación en string del objeto."""
        return self.mostrar_info()

# Clase que representa una semana completa de clima (herencia no aplica aquí,
# pero podríamos extenderla para meses o años)
class SemanaClima:
    """
    Clase que gestiona una semana completa de datos climáticos.
    
    Atributos:
        _dias (list): Lista de objetos DiaClima
    """
    
    def __init__(self):
        """Constructor de la clase SemanaClima."""
        self._dias = []
    
    def agregar_dia(self, dia_clima):
        """
        Agrega un día climático a la semana.
        
        Args:
            dia_clima (DiaClima): Objeto DiaClima a agregar
        
        Raises:
            TypeError: Si el parámetro no es un objeto DiaClima
        """
        if not isinstance(dia_clima, DiaClima):
            raise TypeError("Solo se pueden agregar objetos de tipo DiaClima")
        self._dias.append(dia_clima)
    
    def ingresar_temperaturas_manual(self):
        """
        Método para ingresar temperaturas manualmente por consola.
        """
        print("\n" + "="*50)
        print("INGRESO DE TEMPERATURAS SEMANALES (POO)")
        print("="*50)
        
        for numero_dia in range(1, 8):
            while True:
                try:
                    temp_input = safe_input(f"Ingrese la temperatura para el {DiaClima.DIAS_SEMANA[numero_dia]}: ")
                    dia = DiaClima(numero_dia)
                    dia.temperatura = temp_input  # Usa el setter con validación
                    self.agregar_dia(dia)
                    break
                except ValueError as e:
                    print(f"Error: {e}. Intente nuevamente.")
    
    def calcular_promedio(self):
        """
        Calcula el promedio semanal de temperaturas.
        
        Returns:
            float: Promedio semanal, o 0.0 si no hay datos
        
        Raises:
            ValueError: Si no hay días con temperatura registrada
        """
        if not self._dias:
            return 0.0
        
        # Filtra días sin temperatura registrada
        dias_con_temp = [dia for dia in self._dias if dia.temperatura is not None]
        
        if not dias_con_temp:
            raise ValueError("No hay temperaturas registradas para calcular el promedio")
        
        suma = sum(dia.temperatura for dia in dias_con_temp)
        promedio = suma / len(dias_con_temp)
        return round(promedio, 2)
    
    def clasificar_clima(self, promedio):
        """
        Clasifica el clima según el promedio de temperatura (polimorfismo potencial).
        
        Args:
            promedio (float): Promedio semanal de temperatura
        
        Returns:
            str: Clasificación del clima
        """
        if promedio < 10:
            return "Muy frío"
        elif promedio < 20:
            return "Frío"
        elif promedio < 25:
            return "Templado"
        elif promedio < 30:
            return "Cálido"
        else:
            return "Muy cálido"
    
    def mostrar_resumen(self):
        """
        Muestra un resumen completo de la semana climática.
        """
        if not self._dias:
            print("No hay datos climáticos registrados.")
            return
        
        print("\n" + "="*50)
        print("RESUMEN SEMANAL DEL CLIMA (POO)")
        print("="*50)
        
        # Mostrar información de cada día
        for dia in self._dias:
            print(f"  {dia.mostrar_info()}")
        
        # Calcular y mostrar promedio
        try:
            promedio = self.calcular_promedio()
            clasificacion = self.clasificar_clima(promedio)
            
            print("\n" + "-"*30)
            print(f"PROMEDIO SEMANAL: {promedio}°C")
            print(f"CLASIFICACIÓN: {clasificacion}")
            print("-"*30)
        except ValueError as e:
            print(f"\nAdvertencia: {e}")

# Clase principal que maneja la interfaz del usuario
class GestorClima:
    """
    Clase principal que gestiona la aplicación de clima.
    
    Esta clase coordina todas las operaciones y sirve como interfaz
    principal del programa.
    """
    
    def __init__(self):
        """Constructor del GestorClima."""
        self.semana_actual = None
    
    def ejecutar(self):
        """
        Método principal que ejecuta la aplicación.
        """
        print("PROGRAMA PARA CALCULAR EL PROMEDIO SEMANAL DEL CLIMA")
        print("(Programación Orientada a Objetos)")
        
        while True:
            self.mostrar_menu()
            opcion = safe_input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.ingresar_nueva_semana()
            elif opcion == "2":
                self.mostrar_resumen_actual()
            elif opcion == "3":
                print("\n¡Gracias por usar el programa!")
                break
            else:
                print("\nOpción no válida. Intente nuevamente.")
    
    def mostrar_menu(self):
        """Muestra el menú principal de la aplicación."""
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL")
        print("="*50)
        print("1. Ingresar datos de una nueva semana")
        print("2. Mostrar resumen de la semana actual")
        print("3. Salir")
    
    def ingresar_nueva_semana(self):
        """Proceso para ingresar datos de una nueva semana."""
        self.semana_actual = SemanaClima()
        self.semana_actual.ingresar_temperaturas_manual()
        self.semana_actual.mostrar_resumen()
    
    def mostrar_resumen_actual(self):
        """Muestra el resumen de la semana actual."""
        if self.semana_actual:
            self.semana_actual.mostrar_resumen()
        else:
            print("\nNo hay datos de semana actual. Ingrese una nueva semana primero.")

# Punto de entrada del programa
if __name__ == "__main__":
    # Crear instancia del gestor y ejecutar la aplicación
    app = GestorClima()
    app.ejecutar()