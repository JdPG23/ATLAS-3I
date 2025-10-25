"""
Comparar trayectorias del cometa con parámetros originales vs nuevos
"""
import numpy as np
from datetime import datetime, timedelta

perihelion_date = datetime(2025, 10, 29)
start_date = perihelion_date - timedelta(days=60)  # 30 de agosto

# Parámetros fijos
e = 6.3
q = 1.38
a = q / (1 - e)

# PARÁMETROS ORIGINALES (de tu código inicial)
i_orig = 175.0
Omega_orig = 180.0
omega_orig = 150.0

# PARÁMETROS NUEVOS (que puse yo)
i_new = 30.0
Omega_new = 30.0
omega_new = 210.0

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

def calculate_comet_position(days_offset, i, Omega, omega):
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
    
    return x, y, z, theta

print("="*80)
print("COMPARACIÓN DE TRAYECTORIAS DEL COMETA")
print("="*80)

print(f"\nFecha: {start_date.strftime('%d de %B de %Y')} (30 de agosto)")
print("\n" + "-"*80)

# Posición con parámetros ORIGINALES
x_orig, y_orig, z_orig, theta_orig = calculate_comet_position(-60, i_orig, Omega_orig, omega_orig)
r_orig = np.sqrt(x_orig**2 + y_orig**2 + z_orig**2)
angle_orig = np.degrees(np.arctan2(y_orig, x_orig))
if angle_orig < 0:
    angle_orig += 360

print("\nPARÁMETROS ORIGINALES (i=175°, Ω=180°, ω=150°):")
print(f"  Posición: ({x_orig:7.3f}, {y_orig:7.3f}, {z_orig:7.3f}) AU")
print(f"  Distancia: {r_orig:.3f} AU")
print(f"  Ángulo: {angle_orig:.1f}°")

# Posición con parámetros NUEVOS
x_new, y_new, z_new, theta_new = calculate_comet_position(-60, i_new, Omega_new, omega_new)
r_new = np.sqrt(x_new**2 + y_new**2 + z_new**2)
angle_new = np.degrees(np.arctan2(y_new, x_new))
if angle_new < 0:
    angle_new += 360

print("\nPARÁMETROS NUEVOS (i=30°, Ω=30°, ω=210°):")
print(f"  Posición: ({x_new:7.3f}, {y_new:7.3f}, {z_new:7.3f}) AU")
print(f"  Distancia: {r_new:.3f} AU")
print(f"  Ángulo: {angle_new:.1f}°")

print("\n" + "="*80)
print("ANÁLISIS DE LA IMAGEN DE NASA:")
print("="*80)
print("\nEn la imagen de NASA (30 de agosto), el cometa:")
print("  - Viene desde arriba-izquierda")
print("  - Cruza hacia abajo-derecha")
print("  - Pasa cerca de Mars (que está en 215°)")
print("  - La línea verde es muy inclinada")
print("\n¿Cuál geometría coincide mejor?")
print(f"\nOriginal: Cometa en {angle_orig:.1f}° (Ángulo cerca de Mars: 215°)")
print(f"Nueva:    Cometa en {angle_new:.1f}° (Ángulo cerca de Mars: 215°)")

print("\n" + "="*80)
print("RECOMENDACIÓN:")
print("="*80)
if abs(angle_orig - 215) < abs(angle_new - 215):
    print("Los parámetros ORIGINALES parecen estar más cerca de Mars.")
    print("Sugiero REVERTIR a los parámetros originales.")
else:
    print("Los parámetros NUEVOS están más cerca de Mars.")
    print("Sugiero MANTENER los parámetros nuevos.")
print("="*80)

