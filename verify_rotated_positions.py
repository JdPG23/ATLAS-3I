"""
Verificar posiciones planetarias DESPUÉS de aplicar rotación de 270°
"""
import numpy as np
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)  # 30 de agosto
date_str = start_date.strftime("%Y-%m-%d")

solar_system_ephemeris.set('builtin')
sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]

print("="*80)
print(f"VERIFICANDO POSICIONES ROTADAS - {start_date.strftime('%d de agosto de %Y')}")
print("="*80)

for planet_name in ['mercury', 'venus', 'earth', 'mars', 'jupiter']:
    pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    
    # Posición original
    x_orig = pos.x.value - sun_pos.x.value
    y_orig = pos.y.value - sun_pos.y.value
    
    # Aplicar rotación 270°
    angle_rad = np.radians(270)
    x_new = x_orig * np.cos(angle_rad) - y_orig * np.sin(angle_rad)
    y_new = x_orig * np.sin(angle_rad) + y_orig * np.cos(angle_rad)
    
    # Determinar posición
    h = "Derecha" if x_new > 0 else "Izquierda"
    v = "Arriba" if y_new > 0 else "Abajo"
    
    print(f"{planet_name.upper():<10} Original: ({x_orig:7.3f}, {y_orig:7.3f}) → Rotado: ({x_new:7.3f}, {y_new:7.3f}) → {v}-{h}")

print("\n" + "="*80)
print("OBJETIVO según imagen NASA (30 agosto):")
print("="*80)
print("Earth:   Derecha (Este)")
print("Jupiter: Arriba (Norte)")  
print("Mars:    Abajo-Izquierda")
print("="*80)

# Probar diferentes ángulos
print("\nPROBANDO DIFERENTES ÁNGULOS DE ROTACIÓN:")
print("="*80)

for angle in [0, 90, 180, 270]:
    print(f"\nRotación {angle}°:")
    print("-" * 80)
    
    angle_rad = np.radians(angle)
    
    for planet_name in ['earth', 'mars', 'jupiter']:
        pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
        x_orig = pos.x.value - sun_pos.x.value
        y_orig = pos.y.value - sun_pos.y.value
        
        x_new = x_orig * np.cos(angle_rad) - y_orig * np.sin(angle_rad)
        y_new = x_orig * np.sin(angle_rad) + y_orig * np.cos(angle_rad)
        
        h = "Der" if x_new > 0 else "Izq"
        v = "Arr" if y_new > 0 else "Aba"
        
        print(f"  {planet_name.capitalize():<10} ({x_new:6.2f}, {y_new:6.2f}) → {v}-{h}")

