"""
Calcular los ángulos de rotación necesarios para que cada planeta
coincida con la imagen de NASA
"""
import numpy as np
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)  # 30 de agosto
date_str = start_date.strftime("%Y-%m-%d")

# Posiciones OBJETIVO según imagen de NASA (30 de agosto)
# Estimadas visualmente de la imagen
target_positions = {
    'earth': {'angle': 338, 'desc': 'Derecha (Este)'},
    'mars': {'angle': 215, 'desc': 'Abajo-Izquierda'},
    'jupiter': {'angle': 99, 'desc': 'Arriba (Norte)'},
    'venus': {'angle': 76, 'desc': 'Arriba-Derecha'},
    'mercury': {'angle': 93, 'desc': 'Arriba (Norte)'},
    'saturn': {'angle': 359, 'desc': 'Derecha'}
}

solar_system_ephemeris.set('builtin')
sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]

print("="*80)
print(f"CALCULANDO OFFSETS ANGULARES - {start_date.strftime('%d de agosto de %Y')}")
print("="*80)
print("\nObjetivo: Rotar cada planeta en su órbita para coincidir con NASA\n")

offsets = {}

for planet_name in ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']:
    # Posición actual del planeta
    pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    x = pos.x.value - sun_pos.x.value
    y = pos.y.value - sun_pos.y.value
    
    # Ángulo actual
    current_angle = np.degrees(np.arctan2(y, x))
    if current_angle < 0:
        current_angle += 360
    
    # Ángulo objetivo
    target_angle = target_positions[planet_name]['angle']
    target_desc = target_positions[planet_name]['desc']
    
    # Calcular offset necesario
    offset = target_angle - current_angle
    
    # Normalizar a rango [-180, 180]
    if offset > 180:
        offset -= 360
    elif offset < -180:
        offset += 360
    
    offsets[planet_name] = offset
    
    print(f"{planet_name.upper()}")
    print(f"  Posición actual:   {current_angle:6.1f}°")
    print(f"  Posición objetivo: {target_angle:6.1f}° ({target_desc})")
    print(f"  Offset necesario:  {offset:6.1f}°")
    print()

print("="*80)
print("OFFSETS PARA COPIAR EN EL CÓDIGO:")
print("="*80)
print("planet_angle_offsets = {")
for planet_name, offset in offsets.items():
    print(f"    '{planet_name}': {offset:.1f},")
print("}")
print("="*80)

# Verificar
print("\nVERIFICACIÓN:")
print("="*80)
for planet_name in ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']:
    pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    x_orig = pos.x.value - sun_pos.x.value
    y_orig = pos.y.value - sun_pos.y.value
    
    # Aplicar rotación
    angle_offset = np.radians(offsets[planet_name])
    x_new = x_orig * np.cos(angle_offset) - y_orig * np.sin(angle_offset)
    y_new = x_orig * np.sin(angle_offset) + y_orig * np.cos(angle_offset)
    
    new_angle = np.degrees(np.arctan2(y_new, x_new))
    if new_angle < 0:
        new_angle += 360
    
    target_angle = target_positions[planet_name]['angle']
    error = abs(new_angle - target_angle)
    
    print(f"{planet_name.capitalize():<10} Nuevo ángulo: {new_angle:6.1f}° (objetivo: {target_angle:6.1f}°, error: {error:.1f}°)")

print("="*80)

