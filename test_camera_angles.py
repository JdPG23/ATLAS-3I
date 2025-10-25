"""
Probar diferentes ángulos de cámara para encontrar cuál coincide con NASA
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)
date_str = start_date.strftime("%Y-%m-%d")

# Probar diferentes azimuts
azimuts_to_test = [0, 45, 90, 135, 180, 225, 270, 315]

solar_system_ephemeris.set('builtin')
sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]

planet_colors = {'earth': 'blue', 'mars': 'red', 'jupiter': 'brown', 'venus': 'orange'}
planet_sizes = {'earth': 70, 'mars': 50, 'jupiter': 140, 'venus': 60}

# Obtener posiciones
planets_pos = {}
for planet_name in ['earth', 'mars', 'jupiter', 'venus']:
    pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    x = pos.x.value - sun_pos.x.value
    y = pos.y.value - sun_pos.y.value
    z = pos.z.value - sun_pos.z.value
    planets_pos[planet_name] = (x, y, z)

print("="*80)
print("PROBANDO DIFERENTES ÁNGULOS DE CÁMARA (azimut)")
print("="*80)

# Crear figura con subplots
fig = plt.figure(figsize=(16, 12), facecolor='#000000')

for idx, azim in enumerate(azimuts_to_test):
    ax = fig.add_subplot(2, 4, idx + 1, projection='3d', facecolor='#000011')
    
    # Plot planetas
    for planet_name, (x, y, z) in planets_pos.items():
        ax.scatter([x], [y], [z], 
                  color=planet_colors[planet_name], 
                  s=planet_sizes[planet_name], 
                  alpha=1.0, edgecolors='white', linewidths=1.5)
        ax.text(x, y, z + 0.3, planet_name[0].upper(), 
               color='white', fontsize=8, ha='center', va='bottom', weight='bold')
    
    # Sol
    ax.scatter([0], [0], [0], color='yellow', s=200, alpha=1.0)
    ax.text(0, 0, 0.3, 'S', color='white', fontsize=8, ha='center', va='bottom', weight='bold')
    
    # Configurar vista
    ax.view_init(elev=90, azim=azim)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_zlim(-2, 2)
    
    # Ocultar ejes para claridad
    ax.set_axis_off()
    
    # Título
    ax.text2D(0.5, 0.95, f'azim = {azim}°', 
             transform=ax.transAxes, fontsize=12, weight='bold', 
             ha='center', va='top', color='cyan',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.8))
    
    # Leyenda de orientación
    if idx == 0:
        ax.text2D(0.05, 0.05, 'E=Earth\nM=Mars\nJ=Jupiter\nV=Venus\nS=Sun',
                 transform=ax.transAxes, fontsize=7, ha='left', va='bottom',
                 color='white', family='monospace')

plt.tight_layout()
plt.savefig('test_camera_angles.png', dpi=150, facecolor='#000000', edgecolor='none', bbox_inches='tight')
print("\n✓ Imagen guardada: test_camera_angles.png")
print("="*80)
print("Compara estos 8 ángulos con la imagen de NASA.")
print("Encuentra cuál hace que:")
print("  - Earth esté a la DERECHA")
print("  - Jupiter esté ARRIBA")
print("  - Mars esté ABAJO-IZQUIERDA")
print("\nEse será el azimut correcto para la cámara inicial.")
print("="*80)
plt.close()

