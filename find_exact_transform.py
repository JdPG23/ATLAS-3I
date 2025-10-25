"""
Probar todas las transformaciones posibles para encontrar la correcta
"""
import numpy as np

# Posiciones originales (30 de agosto, azim=0°)
planets = {
    'Earth': (0.926, -0.369),
    'Mars': (-1.259, -0.883),
    'Jupiter': (-0.775, 4.688),
    'Venus': (0.158, 0.645)
}

# OBJETIVO (según imagen de NASA):
# Earth: DERECHA (x > 0.5, |y| pequeño)
# Jupiter: ARRIBA (y > 3)
# Mars: ABAJO-IZQUIERDA (x < 0, y < 0)
# Venus: ARRIBA-DERECHA (x > 0, y > 0)

transformations = {
    "Sin cambio": lambda x, y: (x, y),
    "Rotar 90° (-y, x)": lambda x, y: (-y, x),
    "Rotar 180° (-x, -y)": lambda x, y: (-x, -y),
    "Rotar 270° (y, -x)": lambda x, y: (y, -x),
    "Invertir X (-x, y)": lambda x, y: (-x, y),
    "Invertir Y (x, -y)": lambda x, y: (x, -y),
    "Intercambiar (y, x)": lambda x, y: (y, x),
    "Intercambiar+InvX (-y, x)": lambda x, y: (-y, x),
    "Intercambiar+InvY (y, -x)": lambda x, y: (y, -x),
    "Intercambiar+Ambos (-y, -x)": lambda x, y: (-y, -x),
}

print("="*80)
print("BUSCANDO TRANSFORMACIÓN CORRECTA")
print("="*80)
print("\nOBJETIVO (imagen NASA):")
print("  Earth:   DERECHA (x > 0.5)")
print("  Jupiter: ARRIBA (y > 3)")
print("  Mars:    ABAJO-IZQUIERDA (x < 0, y < 0)")
print("  Venus:   ARRIBA-DERECHA (x > 0, y > 0)")

best_score = 0
best_transform = None

for name, transform in transformations.items():
    print(f"\n{'='*80}")
    print(f"Probando: {name}")
    print("="*80)
    
    score = 0
    results = {}
    
    for planet, (x_orig, y_orig) in planets.items():
        x_new, y_new = transform(x_orig, y_orig)
        results[planet] = (x_new, y_new)
        
        # Determinar posición
        h = "Der" if x_new > 0 else "Izq"
        v = "Arr" if y_new > 0 else "Aba"
        pos = f"{v}-{h}"
        
        print(f"  {planet:<10} ({x_new:7.3f}, {y_new:7.3f}) → {pos}", end="")
        
        # Evaluar
        checks = []
        if planet == 'Earth':
            if x_new > 0.5 and abs(y_new) < 1:
                checks.append("✓ Derecha")
                score += 3
        elif planet == 'Jupiter':
            if y_new > 3:
                checks.append("✓ Arriba")
                score += 3
        elif planet == 'Mars':
            if x_new < 0 and y_new < 0:
                checks.append("✓ Abajo-Izq")
                score += 3
        elif planet == 'Venus':
            if x_new > 0 and y_new > 0:
                checks.append("✓ Arr-Der")
                score += 1
        
        if checks:
            print(f"  {' '.join(checks)}")
        else:
            print()
    
    print(f"Puntuación: {score}/10")
    
    if score > best_score:
        best_score = score
        best_transform = name

print("\n" + "="*80)
print("MEJOR TRANSFORMACIÓN:")
print("="*80)
print(f"{best_transform} (Puntuación: {best_score}/10)")

if best_transform:
    print("\nAPLICAR EN EL CÓDIGO:")
    transform_func = transformations[best_transform]
    print(f"Transformación: {best_transform}")
    
    # Generar código Python
    if best_transform == "Sin cambio":
        print("  # No se necesita transformación")
    elif "Rotar 90°" in best_transform or "Intercambiar+InvX" in best_transform:
        print("  planet_x_new = -planet_y_original")
        print("  planet_y_new = planet_x_original")
    elif "Rotar 270°" in best_transform or "Intercambiar+InvY" in best_transform:
        print("  planet_x_new = planet_y_original")
        print("  planet_y_new = -planet_x_original")
    elif "Rotar 180°" in best_transform:
        print("  planet_x_new = -planet_x_original")
        print("  planet_y_new = -planet_y_original")
    elif "Invertir X" in best_transform:
        print("  planet_x_new = -planet_x_original")
        print("  planet_y_new = planet_y_original")
    elif "Invertir Y" in best_transform:
        print("  planet_x_new = planet_x_original")
        print("  planet_y_new = -planet_y_original")
    elif "Intercambiar (y, x)" == best_transform:
        print("  planet_x_new = planet_y_original")
        print("  planet_y_new = planet_x_original")
    elif "Intercambiar+Ambos" in best_transform:
        print("  planet_x_new = -planet_y_original")
        print("  planet_y_new = -planet_x_original")

print("="*80)

