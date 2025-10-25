"""
Verificar posiciones de planetas el 30 de agosto de 2025 (inicio de la animación)
"""
import numpy as np
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

AU_TO_KM = 149597870.7

# Parámetros del cometa
e = 6.3
q = 1.38
i = 30.0
Omega = 30.0
omega = 210.0
perihelion_date = datetime(2025, 10, 29)
a = q / (1 - e)

# Fecha inicial: 30 de agosto de 2025 (60 días antes del perihelio)
start_date = perihelion_date - timedelta(days=60)
print(f"Fecha calculada: {start_date}")  # Debería ser 30 de agosto

def hyperbolic_orbit_3d(a, e, i, Omega, omega, theta):
    i_rad = np.radians(i)
    Omega_rad = np.radians(Omega)
    omega_rad = np.radians(omega)
    
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    
    x_orb = r * np.cos(theta)
    y_orb = r * np.sin(theta)
    z_orb = 0
    
    x1 = x_orb * np.cos(omega_rad) - y_orb * np.sin(omega_rad)
    y1 = x_orb * np.sin(omega_rad) + y_orb * np.cos(omega_rad)
    z1 = z_orb
    
    x2 = x1
    y2 = y1 * np.cos(i_rad) - z1 * np.sin(i_rad)
    z2 = y1 * np.sin(i_rad) + z1 * np.cos(i_rad)
    
    x = x2 * np.cos(Omega_rad) - y2 * np.sin(Omega_rad)
    y = x2 * np.sin(Omega_rad) + y2 * np.cos(Omega_rad)
    z = z2
    
    return x, y, z

def calculate_comet_position(days_offset):
    GM_sun = 4 * np.pi**2 / 365.25**2
    n = np.sqrt(GM_sun / abs(a)**3)
    M = n * days_offset
    
    H = M / e if M > 0 else M * e
    for _ in range(100):
        f = e * np.sinh(H) - H - M
        df = e * np.cosh(H) - 1
        if abs(df) < 1e-10:
            break
        H_new = H - f / df
        if abs(H_new - H) < 1e-10:
            H = H_new
            break
        H = H_new
    
    theta = 2 * np.arctan(np.sqrt((e - 1) / (e + 1)) * np.tanh(H / 2))
    x, y, z = hyperbolic_orbit_3d(a, e, i, Omega, omega, theta)
    
    return x, y, z

def get_planet_position(planet_name, date_str):
    solar_system_ephemeris.set('builtin')
    sun_pos = get_body_barycentric_posvel('sun', Time(date_str))[0]
    planet_pos = get_body_barycentric_posvel(planet_name, Time(date_str))[0]
    
    x = planet_pos.x.value - sun_pos.x.value
    y = planet_pos.y.value - sun_pos.y.value
    z = planet_pos.z.value - sun_pos.z.value
    
    r = np.sqrt(x**2 + y**2 + z**2)
    angle = np.degrees(np.arctan2(y, x))
    if angle < 0:
        angle += 360
    
    return x, y, z, r, angle

print("="*80)
print(f"POSICIONES PLANETARIAS: {start_date.strftime('%d de %B de %Y')}")
print("="*80)

date_str = start_date.strftime("%Y-%m-%d")

# Calcular posición del cometa
comet_x, comet_y, comet_z = calculate_comet_position(-60)
comet_r = np.sqrt(comet_x**2 + comet_y**2 + comet_z**2)
comet_angle = np.degrees(np.arctan2(comet_y, comet_x))
if comet_angle < 0:
    comet_angle += 360

print(f"\nCOMETA (3I/ATLAS):")
print(f"  Posición: ({comet_x:7.3f}, {comet_y:7.3f}, {comet_z:7.3f}) AU")
print(f"  Distancia del Sol: {comet_r:.3f} AU")
print(f"  Ángulo: {comet_angle:.1f}° (desde +X)")

print("\nPLANETAS:")
print("-" * 80)
print(f"{'Planeta':<12} {'X (AU)':>9} {'Y (AU)':>9} {'Z (AU)':>9} {'Dist':>9} {'Ángulo':>9}")
print("-" * 80)

planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']
for planet in planets:
    x, y, z, r, angle = get_planet_position(planet, date_str)
    print(f"{planet.capitalize():<12} {x:9.3f} {y:9.3f} {z:9.3f} {r:9.3f} {angle:9.1f}°")

print("="*80)
print("\nDESCRIPCIÓN DE LA GEOMETRÍA (vista desde arriba, +Y = arriba):")
print("-" * 80)

# Describir posiciones en términos de cuadrantes
def describe_position(angle):
    if 0 <= angle < 45 or 315 <= angle < 360:
        return "Derecha (Este)"
    elif 45 <= angle < 135:
        return "Arriba (Norte)"
    elif 135 <= angle < 225:
        return "Izquierda (Oeste)"
    else:
        return "Abajo (Sur)"

print(f"Cometa:   {describe_position(comet_angle)} ({comet_angle:.1f}°)")
for planet in planets:
    x, y, z, r, angle = get_planet_position(planet, date_str)
    print(f"{planet.capitalize():<10} {describe_position(angle)} ({angle:.1f}°)")

print("\n" + "="*80)
print("COMPARAR CON LA IMAGEN DE NASA:")
print("="*80)
print("En la imagen de NASA (30 de agosto):")
print("  - Jupiter: arriba (Norte)")
print("  - Earth: derecha (Este)")
print("  - Mars: cerca del cruce con el cometa")
print("  - Venus: cerca del Sol, centro")
print("  - Mercury: cerca del Sol, centro")
print("  - Cometa: cruza desde arriba-izquierda hacia abajo-derecha")
print("="*80)

