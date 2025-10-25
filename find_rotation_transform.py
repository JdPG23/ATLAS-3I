"""
Encontrar la transformación de coordenadas para que coincida con la imagen de NASA
"""
import numpy as np
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)  # 30 de agosto
date_str = start_date.strftime("%Y-%m-%d")

def get_planet_position(planet_name):
    solar_system_ephemeris.set('builtin')
    sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]
    planet_pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    
    x = planet_pos.x.value - sun_pos.x.value
    y = planet_pos.y.value - sun_pos.y.value
    z = planet_pos.z.value - sun_pos.z.value
    
    return x, y, z

def describe_quadrant(x, y):
    """Describir en qué cuadrante está (visto desde arriba)"""
    if x > 0 and y > 0:
        return "Arriba-Derecha (NE)"
    elif x < 0 and y > 0:
        return "Arriba-Izquierda (NW)"
    elif x < 0 and y < 0:
        return "Abajo-Izquierda (SW)"
    else:
        return "Abajo-Derecha (SE)"

print("="*80)
print("ENCONTRAR TRANSFORMACIÓN DE COORDENADAS")
print("="*80)
print(f"Fecha: {start_date.strftime('%d de agosto de 2025')}")
print("\nEn la imagen de NASA:")
print("  - Earth: Derecha (Este)")
print("  - Jupiter: Arriba (Norte)")
print("  - Mars: Abajo-Izquierda")
print("  - Venus: Arriba-Derecha (cerca del centro)")

# Obtener posiciones originales
planets = {
    'earth': get_planet_position('earth'),
    'mars': get_planet_position('mars'),
    'jupiter': get_planet_position('jupiter'),
    'venus': get_planet_position('venus')
}

print("\n" + "="*80)
print("COORDENADAS ORIGINALES (de astropy):")
print("="*80)
for name, (x, y, z) in planets.items():
    print(f"{name.capitalize():<10} ({x:7.3f}, {y:7.3f}, {z:7.3f}) → {describe_quadrant(x, y)}")

# Probar diferentes transformaciones
transformations = {
    "Sin cambio (X, Y, Z)": lambda x, y, z: (x, y, z),
    "Rotar 180° en Z (-X, -Y, Z)": lambda x, y, z: (-x, -y, z),
    "Rotar 90° en Z (-Y, X, Z)": lambda x, y, z: (-y, x, z),
    "Rotar 270° en Z (Y, -X, Z)": lambda x, y, z: (y, -x, z),
    "Invertir X (-X, Y, Z)": lambda x, y, z: (-x, y, z),
    "Invertir Y (X, -Y, Z)": lambda x, y, z: (x, -y, z),
    "Invertir X e Y (-X, -Y, Z)": lambda x, y, z: (-x, -y, z),
    "Intercambiar XY (Y, X, Z)": lambda x, y, z: (y, x, z),
    "Intercambiar XY + invertir (Y, -X, Z)": lambda x, y, z: (y, -x, z),
    "Intercambiar XY + invertir (-Y, X, Z)": lambda x, y, z: (-y, x, z),
}

best_match = None
best_score = 0

for transform_name, transform_func in transformations.items():
    print(f"\n{'='*80}")
    print(f"TRANSFORMACIÓN: {transform_name}")
    print("="*80)
    
    score = 0
    results = {}
    
    for name, (x, y, z) in planets.items():
        x_new, y_new, z_new = transform_func(x, y, z)
        quadrant = describe_quadrant(x_new, y_new)
        results[name] = (x_new, y_new, quadrant)
        print(f"{name.capitalize():<10} ({x_new:7.3f}, {y_new:7.3f}) → {quadrant}")
        
        # Puntuar según imagen de NASA
        if name == 'earth' and x_new > 0 and abs(y_new) < 0.8:  # Earth debe estar a la derecha
            score += 3
        if name == 'jupiter' and y_new > 3 and x_new < 1:  # Jupiter debe estar arriba
            score += 3
        if name == 'mars' and x_new < 0 and y_new < 0:  # Mars debe estar abajo-izquierda
            score += 3
        if name == 'venus' and x_new > 0 and y_new > 0:  # Venus arriba-derecha
            score += 1
    
    print(f"\nPuntuación: {score}/10")
    
    if score > best_score:
        best_score = score
        best_match = transform_name

print("\n" + "="*80)
print("MEJOR TRANSFORMACIÓN ENCONTRADA:")
print("="*80)
print(f"{best_match} (Puntuación: {best_score}/10)")
print("\nAplica esta transformación a todas las coordenadas planetarias")
print("en la función animate() de tu código.")
print("="*80)

