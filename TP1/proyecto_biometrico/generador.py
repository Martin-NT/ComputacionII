import datetime
import random

def generar_dato():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "frecuencia": random.randint(60, 180),
        "presion": [random.randint(110, 180), random.randint(70, 110)],
        "oxigeno": random.randint(90, 100)
    }
