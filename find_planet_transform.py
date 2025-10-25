"""
Encontrar la transformación que hace que los planetas se vean
como si la cámara estuviera en azimut 270°, pero manteniendo la cámara en azimut 0°
"""
import numpy as np

# Posiciones originales de los planetas (30 de agosto)
planets_original = {
    'Earth': (0.926, -0.369),
    'Mars': (-1.259, -0.883),
    'Jupiter': (-0.775, 4.688),
    'Venus': (0.158, 0.645)
}

def describe_position(x, y):
    """Describir posición vista desde arriba"""
    h_pos = "Derecha" if x > 0 else "Izquierda"
    v_pos = "Arriba" if y > 0 else "Abajo"
    return f"{v_pos}-{h_pos}"

print("="*80)
print("POSICIONES ORIGINALES (con cámara azim=0°):")
print("="*80)
for name, (x, y) in planets_original.items():
    print(f"{name:<10} ({x:7.3f}, {y:7.3f}) → {describe_position(x, y)}")

print("\n" + "="*80)
print("OBJETIVO (como se ve con cámara azim=270°):")
print("="*80)
print("Earth:   Derecha")
print("Jupiter: Arriba")
print("Mars:    Abajo-Izquierda")
print("Venus:   Arriba-Derecha")

# Si la cámara rota 270° antihorario, los objetos aparecen rotados 270° horario = -270° = +90°
# Para simular esto sin mover la cámara, rotamos los objetos -270° = +90° alrededor del eje Z

# Rotación +90° alrededor de Z: (x,y) → (-y, x)
print("\n" + "="*80)
print("TRANSFORMACIÓN: Rotar +90° en Z  →  (x_new, y_new) = (-y, x)")
print("="*80)

for name, (x, y) in planets_original.items():
    x_new = -y
    y_new = x
    print(f"{name:<10} ({x:7.3f}, {y:7.3f}) → ({x_new:7.3f}, {y_new:7.3f}) → {describe_position(x_new, y_new)}")

# Verificar si coincide con objetivo
print("\n" + "="*80)
print("VERIFICACIÓN:")
print("="*80)
x_e, y_e = -(-0.369), 0.926
x_j, y_j = -(4.688), -0.775
x_m, y_m = -(-0.883), -1.259
x_v, y_v = -(0.645), 0.158

checks = [
    ("Earth derecha?", x_e > 0),
    ("Jupiter arriba?", y_j > 0),  # Esto fallará
    ("Mars abajo-izquierda?", x_m < 0 and y_m < 0)
]

# Hmm, parece que +90° no es correcto. Probemos -90°
print("\n" + "="*80)
print("TRANSFORMACIÓN: Rotar -90° en Z  →  (x_new, y_new) = (y, -x)")
print("="*80)

all_good = True
for name, (x, y) in planets_original.items():
    x_new = y
    y_new = -x
    result = describe_position(x_new, y_new)
    print(f"{name:<10} ({x:7.3f}, {y:7.3f}) → ({x_new:7.3f}, {y_new:7.3f}) → {result}")
    
    # Verificar
    if name == 'Earth' and x_new > 0 and abs(y_new) < 1:
        print("  ✓ Earth está a la derecha")
    elif name == 'Jupiter' and y_new > 0:
        print("  ✓ Jupiter está arriba")
    elif name == 'Mars' and x_new < 0 and y_new < 0:
        print("  ✓ Mars está abajo-izquierda")

print("\n" + "="*80)
print("FÓRMULA FINAL PARA APLICAR EN EL CÓDIGO:")
print("="*80)
print("En la función animate(), después de obtener la posición del planeta:")
print("  planet_x_original, planet_y_original, planet_z = ...")
print("  # Aplicar transformación para que coincida con vista de NASA")
print("  planet_x = planet_y_original")
print("  planet_y = -planet_x_original")
print("  planet_z = planet_z  # Sin cambio")
print("="*80)

