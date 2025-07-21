import datetime
import random

class GeneradorBiometrico:
    def __init__(self):
        pass
    
    def generar_dato(self):
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],
            "oxigeno": random.randint(90, 100)
        }