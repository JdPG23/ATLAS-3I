"""
Generar solo el primer frame para verificar posiciones planetarias
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)  # 30 de agosto
date_str = start_date.strftime("%Y-%m-%d")

# Crear figura
fig = plt.figure(figsize=(14, 10), facecolor='#000000')
ax = fig.add_subplot(111, projection='3d', facecolor='#000011')

# Obtener posiciones planetarias
solar_system_ephemeris.set('builtin')
sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]

planet_colors = {'mercury': 'gray', 'venus': 'orange', 'earth': 'blue',
                'mars': 'red', 'jupiter': 'brown', 'saturn': 'goldenrod'}
planet_sizes = {'mercury': 40, 'venus': 60, 'earth': 70, 'mars': 50, 
                'jupiter': 140, 'saturn': 120}

print("="*80)
print(f"PRIMER FRAME - {start_date.strftime('%d de agosto de 2025')}")
print("="*80)

for planet_name in ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']:
    pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    
    # Heliocéntrico
    x = pos.x.value - sun_pos.x.value
    y = pos.y.value - sun_pos.y.value
    z = pos.z.value - sun_pos.z.value
    
    print(f"{planet_name.capitalize():<10} X:{x:7.3f}  Y:{y:7.3f}  Z:{z:7.3f}")
    
    # Plot planeta
    ax.scatter([x], [y], [z], 
              color=planet_colors[planet_name], 
              s=planet_sizes[planet_name], 
              alpha=1.0, 
              edgecolors='white', 
              linewidths=2,
              label=planet_name.capitalize())
    
    # Label
    ax.text(x, y, z + 0.2, planet_name.capitalize(), 
           color='white', fontsize=10, ha='center', va='bottom', weight='bold')

# Plot Sol
ax.scatter([0], [0], [0], color='yellow', s=300, alpha=1.0, label='Sun')
ax.text(0, 0, 0.2, 'Sun', color='white', fontsize=12, ha='center', va='bottom', weight='bold')

# Configurar ejes
ax.set_xlabel('X (AU)', fontsize=12, color='white')
ax.set_ylabel('Y (AU)', fontsize=12, color='white')
ax.set_zlabel('Z (AU)', fontsize=12, color='white')
ax.tick_params(colors='white')

# Vista top-down como NASA
ax.view_init(elev=90, azim=0)  # Vista desde arriba
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_zlim(-3, 3)

# Agregar texto de referencia
ax.text2D(0.5, 0.98, f'{start_date.strftime("%B %d, %Y")} - Vista Top-Down (como NASA)', 
         transform=ax.transAxes, fontsize=14, weight='bold', ha='center', va='top',
         color='white', bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8))

ax.text2D(0.02, 0.02, 
         'Orientación:\n+X = Derecha\n+Y = Arriba\n+Z = Fuera de pantalla', 
         transform=ax.transAxes, fontsize=10, ha='left', va='bottom',
         color='white', family='monospace',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.8))

plt.savefig('test_first_frame.png', dpi=150, facecolor='#000000', edgecolor='none')
print("\n✓ Imagen guardada: test_first_frame.png")
print("="*80)
print("Compara esta imagen con la de NASA.")
print("Si los planetas están en posiciones incorrectas, el problema es el azimut de la cámara.")
print("="*80)
plt.close()

