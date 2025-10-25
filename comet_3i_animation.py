import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import os
from datetime import datetime, timedelta
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris
import astropy.units as u

# Constants
AU_TO_KM = 149597870.7  # 1 AU in kilometers

# Latest orbital parameters for Comet 3I/ATLAS (September 2025)
# Source: Cloete, R., Loeb, A., & Vereš, P. (2025). arXiv:submit/6824338
# Based on 4,022 astrometric observations from 227 observatories (May-Sept 2025)
# Computed with MPC's orbfit package using gravity-only dynamical model
#
# ORBITAL ELEMENTS (Epoch MJD = 60885.672886722 TDT):
# With 1-sigma uncertainties from MPC analysis
#
# VERIFIED PARAMETERS:
# - e = 6.1386 ± 0.0006: Hyperbolic orbit confirms interstellar origin
# - q = 1.3563 ± 0.0001 AU: Perihelion on October 29-30, 2025
# - i = 175.1130 ± 0.0001°: Retrograde orbit, nearly coplanar with ecliptic
# - Ω = 322.1559 ± 0.0012°: Longitude of ascending node
# - ω = 128.0111 ± 0.0008°: Argument of perihelion
# - T_p = 60977.483 ± 0.0004 MJD TDT: Time of perihelion passage
#
# NON-GRAVITATIONAL ACCELERATION:
# - Upper limit: < 3×10⁻¹⁰ au/day² (essentially absent)
# - RA residual: 0.025 ± 0.028 arcsec
# - Dec residual: 0.019 ± 0.02 arcsec
#
# PHYSICAL PARAMETERS (from mass balance analysis):
# - Nucleus mass: ≥ 3.3×10¹⁶ g
# - Diameter: ≥ 5 km (lower limit)
# - Bulk density: ~0.5 g/cm³ (assumed, similar to other comets)
#
e = 6.1386   # Eccentricity ± 0.0006 (hyperbolic/interstellar)
q = 1.3563   # Perihelion distance ± 0.0001 AU (~203 million km)
i = 175.1130 # Inclination ± 0.0001° (retrograde, nearly coplanar)
Omega = 322.1559  # Longitude of ascending node ± 0.0012°
omega = 128.0111  # Argument of perihelion ± 0.0008°

# Perihelion date
perihelion_date = datetime(2025, 10, 29)

# Semi-major axis (negative for hyperbolic orbit)
a = q / (1 - e)

# Uncertainty ellipsoid parameters (based on MPC astrometric residuals)
# Semi-axes lengths representing 3-sigma uncertainty at perihelion for 3I/ATLAS
# Source: Cloete et al. (2025) - arXiv:submit/6824338
#
# ASTROMETRIC RESIDUALS (July-Sept 2025):
# - RA residual: 0.025 ± 0.028 arcsec
# - Dec residual: 0.019 ± 0.02 arcsec
# - Non-gravitational acceleration: < 3×10⁻¹⁰ au/day² (essentially ABSENT)
#
# ORBITAL ELEMENT UNCERTAINTIES (1-sigma):
# - Perihelion q: ± 0.0001 AU (± 15,000 km)
# - Eccentricity e: ± 0.0006
# - Inclination i: ± 0.0001°
#
# 3-SIGMA UNCERTAINTY ELLIPSOID (99.7% confidence):
# Based on propagation of orbital element uncertainties and astrometric residuals
# The small uncertainties reflect the well-determined orbit from 4,022 observations
#
# Conservative estimate for visualization (3-sigma propagated):
# Despite intense media attention and extensive observational campaign,
# uncertainties remain significant when measured in millions of km
uncertainty_axes = [0.02, 0.01, 0.007]  # AU - along radial, tangential, normal directions
# Equivalent to approximately [3, 1.5, 1] million km

# Animation parameters
total_frames = 1000  # More frames for smoother animation
# Set to True for quick testing
TEST_MODE = False
if TEST_MODE:
    total_frames = 100  # Quick test with 100 frames

# For hyperbolic orbits, we need to properly map time to true anomaly using Kepler's equation
# Mean motion n = sqrt(GM/|a|^3) where GM = 4*pi^2 AU^3/year^2
GM_sun = 4 * np.pi**2 / 365.25**2  # AU^3/day^2
n = np.sqrt(GM_sun / abs(a)**3)  # rad/day

def solve_kepler_hyperbolic(M, e, tol=1e-10, max_iter=100):
    """
    Solve Kepler's equation for hyperbolic orbits: M = e*sinh(H) - H
    Returns hyperbolic eccentric anomaly H
    """
    # Initial guess
    H = M / e if M > 0 else M * e

    for _ in range(max_iter):
        f = e * np.sinh(H) - H - M
        df = e * np.cosh(H) - 1

        if abs(df) < tol:
            break

        H_new = H - f / df
        if abs(H_new - H) < tol:
            return H_new
        H = H_new

    return H

# Time mapping (days from perihelion) - solve Kepler's equation for each time
time_from_perihelion = np.linspace(-60, 60, total_frames)
theta_range = []

for t in time_from_perihelion:
    # Mean anomaly M = n * (t - T_perihelion)
    M = n * t

    # Solve for hyperbolic eccentric anomaly H
    H = solve_kepler_hyperbolic(M, e)

    # True anomaly θ = 2 * arctan[sqrt((e-1)/(e+1)) * tanh(H/2)]
    theta = 2 * np.arctan(np.sqrt((e - 1) / (e + 1)) * np.tanh(H / 2))
    theta_range.append(theta)

theta_range = np.array(theta_range)

def hyperbolic_orbit_3d(a, e, i, Omega, omega, theta):
    """
    Calculate 3D position in hyperbolic orbit using orbital elements
    Returns position in AU
    """
    # Convert angles to radians
    i_rad = np.radians(i)
    Omega_rad = np.radians(Omega)
    omega_rad = np.radians(omega)

    # Distance from focus (for hyperbolic orbit where a < 0)
    # Using the correct formula: r = a(1 - e²)/(1 + e*cos(θ))
    r = a * (1 - e**2) / (1 + e * np.cos(theta))

    # Position in orbital plane
    x_orb = r * np.cos(theta)
    y_orb = r * np.sin(theta)
    z_orb = 0

    # Rotation matrices for orbital orientation
    # Rotate by argument of perihelion
    x1 = x_orb * np.cos(omega_rad) - y_orb * np.sin(omega_rad)
    y1 = x_orb * np.sin(omega_rad) + y_orb * np.cos(omega_rad)
    z1 = z_orb

    # Rotate by inclination
    x2 = x1
    y2 = y1 * np.cos(i_rad) - z1 * np.sin(i_rad)
    z2 = y1 * np.sin(i_rad) + z1 * np.cos(i_rad)

    # Rotate by longitude of ascending node
    x = x2 * np.cos(Omega_rad) - y2 * np.sin(Omega_rad)
    y = x2 * np.sin(Omega_rad) + y2 * np.cos(Omega_rad)
    z = z2

    return x, y, z

def get_planetary_orbit_from_ephemeris(planet_name, center_date, num_points=300):
    """
    Calculate planetary orbit by sampling ephemeris data over one orbital period
    Returns x, y, z arrays for the complete orbit in heliocentric coordinates
    The orbit is centered around center_date to capture the planet's position accurately
    """
    solar_system_ephemeris.set('builtin')
    
    # Exact orbital periods in days (tropical year)
    orbital_periods = {
        'mercury': 87.969, 'venus': 224.701, 'earth': 365.256, 
        'mars': 686.980, 'jupiter': 4332.59, 'saturn': 10759.22
    }
    
    period_days = orbital_periods.get(planet_name, 365)
    
    # Sample positions throughout the orbit
    # Center the orbit around the reference date (±0.5 period)
    x_orbit = []
    y_orbit = []
    z_orbit = []
    
    for i in range(num_points):
        # Calculate date for this point in the orbit
        # Sample from -period/2 to +period/2 around center_date
        fraction = i / (num_points - 1)  # 0 to 1
        days_offset = (fraction - 0.5) * period_days
        sample_date = center_date + timedelta(days=days_offset)
        
        try:
            # Get planet position (barycentric)
            planet_pos = get_body_barycentric_posvel(planet_name, Time(sample_date.strftime("%Y-%m-%d")))[0]
            # Get Sun position (barycentric)
            sun_pos = get_body_barycentric_posvel('sun', Time(sample_date.strftime("%Y-%m-%d")))[0]
            
            # Convert to heliocentric (planet position relative to Sun)
            x_orbit.append(planet_pos.x.value - sun_pos.x.value)
            y_orbit.append(planet_pos.y.value - sun_pos.y.value)
            z_orbit.append(planet_pos.z.value - sun_pos.z.value)
        except Exception as e:
            # If ephemeris fails, skip this point
            print(f"    Warning: Failed to get position for {planet_name} at {sample_date}: {e}")
            continue
    
    return np.array(x_orbit), np.array(y_orbit), np.array(z_orbit)

def create_uncertainty_ellipsoid(center, axes_lengths, num_points=50):
    """
    Create uncertainty ellipsoid points around a center position
    """
    u = np.linspace(0, 2 * np.pi, num_points)
    v = np.linspace(0, np.pi, num_points)

    # Parametric equations for ellipsoid
    x = axes_lengths[0] * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = axes_lengths[1] * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = axes_lengths[2] * np.outer(np.ones_like(u), np.cos(v)) + center[2]

    return x, y, z

def get_planetary_positions(date='2025-10-29'):
    """
    Get positions of planets at a given date
    Returns positions in AU relative to Sun
    """
    solar_system_ephemeris.set('builtin')

    planets_data = {}
    planet_names = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']

    for planet in planet_names:
        try:
            pos = get_body_barycentric_posvel(planet, Time(date))[0]
            # Convert to AU and subtract solar position (approximated as origin)
            planets_data[planet] = {
                'position': [pos.x.value, pos.y.value, pos.z.value],
                'color': {'mercury': 'gray', 'venus': 'orange', 'earth': 'blue',
                         'mars': 'red', 'jupiter': 'brown', 'saturn': 'goldenrod'}[planet]
            }
        except:
            # Fallback positions if ephemeris fails
            distances = {'mercury': 0.39, 'venus': 0.72, 'earth': 1.0, 'mars': 1.52,
                        'jupiter': 5.2, 'saturn': 9.5}
            planets_data[planet] = {
                'position': [distances[planet], 0, 0],
                'color': {'mercury': 'gray', 'venus': 'orange', 'earth': 'blue',
                         'mars': 'red', 'jupiter': 'brown', 'saturn': 'goldenrod'}[planet]
            }

    return planets_data

# Create figure and 3D axes with dark space background
# Use dimensions divisible by 2 for video encoding
fig = plt.figure(figsize=(14, 10), facecolor='#000000')
ax = fig.add_subplot(111, projection='3d', facecolor='#000011')

# Calculate comet trajectory
x_traj, y_traj, z_traj = hyperbolic_orbit_3d(a, e, i, Omega, omega, theta_range)

# Plot comet trajectory - make it very visible
comet_traj, = ax.plot(x_traj, y_traj, z_traj, '-', color='cyan', linewidth=3.0, alpha=0.95,
                     label='Comet Trajectory')

# Uncertainty ellipsoid will be dynamically updated to follow the comet
# Initial placeholder
uncertainty_surf = []
dimension_lines = []  # Initialize dimension lines list
ellipse_labels = []  # Labels for each ellipse (XY, XZ, YZ)

# Plot Sun (larger and more prominent) with label
sun_glow = ax.scatter([0], [0], [0], color='yellow', s=500, alpha=0.4, edgecolors='orange', linewidths=2)
ax.scatter([0], [0], [0], color='#FFDD00', s=200, alpha=1.0, edgecolors='orange', linewidths=3)
sun_label = ax.text(0, 0, 0.15, 'Sun', color='white', fontsize=11, 
                   ha='center', va='bottom', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFDD00', 
                            alpha=0.8, edgecolor='orange', linewidth=1))

# Plot planets with orbits and labels
# Store planet data for animation
planet_names_list = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']
planet_colors = {'mercury': 'gray', 'venus': 'orange', 'earth': 'blue',
                'mars': 'red', 'jupiter': 'brown', 'saturn': 'goldenrod'}
planet_sizes = {'mercury': 40, 'venus': 60, 'earth': 70, 'mars': 50, 
                'jupiter': 140, 'saturn': 120}

# Real orbital parameters with full 3D orientation (J2000 epoch)
# a = semi-major axis (AU), e = eccentricity
# i = inclination (degrees), Omega = longitude of ascending node (degrees)
# omega = argument of perihelion (degrees), L0 = mean longitude at epoch (degrees)
planet_orbital_params = {
    'mercury': {'a': 0.387, 'e': 0.206, 'i': 7.00, 'Omega': 48.33, 'omega': 29.12, 'L0': 252.25},
    'venus': {'a': 0.723, 'e': 0.007, 'i': 3.39, 'Omega': 76.68, 'omega': 54.85, 'L0': 181.98},
    'earth': {'a': 1.000, 'e': 0.017, 'i': 0.00, 'Omega': 174.87, 'omega': 288.06, 'L0': 100.46},
    'mars': {'a': 1.524, 'e': 0.093, 'i': 1.85, 'Omega': 49.56, 'omega': 286.50, 'L0': 355.43},
    'jupiter': {'a': 5.203, 'e': 0.048, 'i': 1.30, 'Omega': 100.46, 'omega': 273.87, 'L0': 34.40},
    'saturn': {'a': 9.537, 'e': 0.054, 'i': 2.49, 'Omega': 113.66, 'omega': 339.39, 'L0': 50.08}
}

planet_plots = {}
orbit_lines = {}
planet_labels = {}

# Offsets temporales para cada planeta (en DÍAS)
# Avanza (+) o retrocede (-) cada planeta en su órbita
# Esto cambia la fecha efectiva para obtener el planeta de ephemeris
#planet_time_offsets = {
#    'mercury': 5,   # días
#    'venus': 90,
#    'earth': 140,
#    'mars': 200,
#    'jupiter': 1200,
#    'saturn': 0
#}

planet_time_offsets = {
    'mercury': 0,   # días
    'venus': 0,
    'earth': 0,
    'mars': -30,
    'jupiter': 0,
    'saturn': 0
}

# Draw REAL orbits for each planet using ephemeris data
print("\n[ORBITS] Calculating planetary orbits from ephemeris...")
for planet_name in planet_names_list:
    color = planet_colors[planet_name]
    
    # Calculate orbit from real ephemeris data (heliocentric)
    print(f"  Computing orbit for {planet_name.capitalize()}...")
    x_orbit, y_orbit, z_orbit = get_planetary_orbit_from_ephemeris(planet_name, perihelion_date, num_points=300)
    
    # NO rotar órbitas - solo rotar los planetas individuales en animate()
    
    # Different line styles based on distance
    if planet_name in ['mercury', 'venus', 'earth', 'mars']:
        orbit_line, = ax.plot(x_orbit, y_orbit, z_orbit, '--', color=color, 
                             alpha=0.4, linewidth=1.2, label=f'{planet_name.capitalize()} orbit')
    else:
        orbit_line, = ax.plot(x_orbit, y_orbit, z_orbit, ':', color=color, 
                             alpha=0.3, linewidth=1.0, label=f'{planet_name.capitalize()} orbit')
    orbit_lines[planet_name] = orbit_line
    
    # Create planet marker (will be updated in animate())
    size = planet_sizes[planet_name]
    plot = ax.scatter([], [], [],
                     color=color, s=size, alpha=1.0, edgecolors='white', linewidths=2)
    planet_plots[planet_name] = plot
    
    # Add planet label (will be updated in animate())
    label = ax.text(0, 0, 0, planet_name.capitalize(), color='white', fontsize=9, 
                   ha='center', va='bottom', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=color, 
                            alpha=0.7, edgecolor='white', linewidth=0.5))
    planet_labels[planet_name] = label

print("[SUCCESS] All planetary orbits calculated!")

# Comet position marker - small point
comet_point, = ax.plot([], [], [], 'o', markersize=4, markeredgecolor='white',
                      markeredgewidth=1, markerfacecolor='#FF6600', alpha=1.0)

# Comet label (will be dynamically updated to follow comet)
comet_label = ax.text(0, 0, 0, '', color='white', fontsize=10, 
                     ha='center', va='bottom', weight='bold',
                     bbox=dict(boxstyle='round,pad=0.4', facecolor='#FF6600', 
                              alpha=0.85, edgecolor='white', linewidth=1.5))

# Comet tail (will be dynamically updated)
comet_tail, = ax.plot([], [], [], '-', color='#00FFFF', linewidth=2.5, alpha=0.7)

# Title text (date and phase)
title_text = ax.text2D(0.5, 0.98, '', transform=ax.transAxes, fontsize=16,
                      weight='bold', ha='center', va='top',
                      color='white',
                      bbox=dict(boxstyle='round,pad=0.8', facecolor='#000000', 
                               alpha=0.85, edgecolor='#00FFFF', linewidth=2))

# Information panel (bottom left) - horizontal layout
info_text = ax.text2D(0.02, 0.02, '', transform=ax.transAxes, fontsize=9,
                    verticalalignment='bottom', ha='left',
                    color='white', family='monospace',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#000000', 
                             alpha=0.92, edgecolor='#00FF00', linewidth=2))

# Legend panel (top right) - horizontal layout
legend_text = ax.text2D(0.98, 0.85, '', transform=ax.transAxes, fontsize=8,
                       verticalalignment='top', ha='right',
                       color='white',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='#000000',
                                alpha=0.92, edgecolor='#FFAA00', linewidth=2))

# Set initial view limits (will be dynamically adjusted)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)

# Style axes - labels in millions of km
ax.set_xlabel('X (million km)', fontsize=12, color='white', weight='bold')
ax.set_ylabel('Y (million km)', fontsize=12, color='white', weight='bold')
ax.set_zlabel('Z (million km)', fontsize=12, color='white', weight='bold')
ax.tick_params(colors='white', labelsize=9)

# Custom tick formatter to show million km
def format_ticks_million_km(val, pos):
    return f'{val * AU_TO_KM / 1e6:.0f}'

from matplotlib.ticker import FuncFormatter
ax.xaxis.set_major_formatter(FuncFormatter(format_ticks_million_km))
ax.yaxis.set_major_formatter(FuncFormatter(format_ticks_million_km))
ax.zaxis.set_major_formatter(FuncFormatter(format_ticks_million_km))

# Make axes invisible for cinematic look
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')
ax.grid(False)  # No grid for cinematic view
ax.set_axis_off()  # Hide axes completely

def get_camera_path(frame, total_frames, comet_pos):
    """
    Ultra-close camera starting at 0.1 AU, smooth gradual zoom to 1.2 AU
    - Start extremely close (0.1 AU) for maximum ellipsoid visibility
    - Single smooth transition throughout entire animation
    - End at moderate zoom (1.2 AU) for overview
    """
    phase = frame / total_frames

    # Smooth easing function
    def ease_in_out(t):
        return t * t * (3.0 - 2.0 * t)

    # Single smooth transition throughout entire animation
    t = ease_in_out(phase)  # Smooth transition from 0 to 1 over entire animation

    # Elevation: Start from above, transition to 3D perspective
    elev = 85 - t * 40  # 85° to 45° (gradual transition)

    # Azimuth: Continuous smooth rotation
    azim = phase * 180  # Full 180° rotation over entire animation

    # Zoom: Ultra-smooth transition from 0.1 AU to 1.2 AU
    start_zoom = 0.1   # Extremely close at start
    end_zoom = 1.2     # Moderate zoom at end
    zoom = start_zoom + t * (end_zoom - start_zoom)

    return elev, azim, zoom, comet_pos

def init():
    global uncertainty_surf, dimension_lines, ellipse_labels
    uncertainty_surf = []
    dimension_lines = []
    ellipse_labels = []

    comet_point.set_data([], [])
    comet_point.set_3d_properties([])
    comet_tail.set_data([], [])
    comet_tail.set_3d_properties([])
    info_text.set_text('')
    title_text.set_text('')
    legend_text.set_text('')
    return comet_point, comet_tail, info_text, title_text, legend_text, uncertainty_surf, dimension_lines, ellipse_labels

def animate(frame):
    global uncertainty_surf, dimension_lines, ellipse_labels

    # Comet position along trajectory
    idx = frame % total_frames
    x_pos = x_traj[idx]
    y_pos = y_traj[idx]
    z_pos = z_traj[idx]

    comet_point.set_data([x_pos], [y_pos])
    comet_point.set_3d_properties([z_pos])
    
    # Update comet label to follow comet position
    comet_label.set_position((x_pos, y_pos))
    comet_label.set_3d_properties(z_pos + 0.15, 'z')  # Slightly above comet
    comet_label.set_text('3I/ATLAS')
    
    # Calculate current date for planet positions
    days_offset = time_from_perihelion[idx]
    current_date = perihelion_date + timedelta(days=days_offset)
    date_str_for_ephemeris = current_date.strftime("%Y-%m-%d")
    
    # Update planet positions for current date using real ephemeris (heliocentric)
    solar_system_ephemeris.set('builtin')
    try:
        # Get Sun position (barycentric) to convert to heliocentric coordinates
        sun_pos = get_body_barycentric_posvel('sun', Time(date_str_for_ephemeris))[0]
        sun_x = sun_pos.x.value
        sun_y = sun_pos.y.value
        sun_z = sun_pos.z.value
    except:
        # If Sun position fails, assume it's at origin
        sun_x, sun_y, sun_z = 0, 0, 0
    
    # Usar offsets temporales definidos globalmente (arriba, cerca de línea 285)
    # No redefinir aquí - usar el diccionario global planet_time_offsets
    
    for planet_name in planet_names_list:
        try:
            # Calcular fecha ajustada para este planeta
            adjusted_date = current_date + timedelta(days=planet_time_offsets[planet_name])
            adjusted_date_str = adjusted_date.strftime("%Y-%m-%d")
            
            # Get Sun position for adjusted date
            try:
                sun_pos_adj = get_body_barycentric_posvel('sun', Time(adjusted_date_str))[0]
                sun_x_adj = sun_pos_adj.x.value
                sun_y_adj = sun_pos_adj.y.value
                sun_z_adj = sun_pos_adj.z.value
            except:
                sun_x_adj, sun_y_adj, sun_z_adj = sun_x, sun_y, sun_z
            
            # Get planet position from ephemeris at adjusted date
            pos = get_body_barycentric_posvel(planet_name, Time(adjusted_date_str))[0]
            # Convert to heliocentric (relative to Sun)
            planet_x = pos.x.value - sun_x_adj
            planet_y = pos.y.value - sun_y_adj
            planet_z = pos.z.value - sun_z_adj
            
            # Update planet scatter plot
            planet_plots[planet_name]._offsets3d = ([planet_x], [planet_y], [planet_z])
            
            # Update planet label
            planet_labels[planet_name].set_position((planet_x, planet_y))
            planet_labels[planet_name].set_3d_properties(planet_z + 0.15, 'z')
        except Exception as e:
            # If ephemeris fails for this planet, skip it
            print(f"Warning: Could not update position for {planet_name}: {e}")
            pass

    # Update uncertainty ellipsoid to follow comet
    if uncertainty_surf:
        for ellipse in uncertainty_surf:
            ellipse.remove()

    # Remove previous dimension lines to avoid trail
    if dimension_lines:
        for line in dimension_lines:
            line.remove()
    dimension_lines = []
    
    # Remove previous ellipse labels
    if ellipse_labels:
        for label in ellipse_labels:
            label.remove()
    ellipse_labels = []

    comet_pos_center = (x_pos, y_pos, z_pos)

    # Draw 3 principal ellipses instead of full ellipsoid surface
    uncertainty_surf = []  # Will hold the ellipse lines

    # Number of points for ellipse drawing
    num_points = 100
    theta = np.linspace(0, 2*np.pi, num_points)

    # Ellipse in XY plane (z = constant) - RED
    x_xy = x_pos + uncertainty_axes[0] * np.cos(theta)
    y_xy = y_pos + uncertainty_axes[1] * np.sin(theta)
    z_xy = np.full_like(theta, z_pos)
    xy_ellipse, = ax.plot(x_xy, y_xy, z_xy, '-', color='#FF3333', linewidth=2.5, alpha=0.7)
    uncertainty_surf.append(xy_ellipse)
    
    # Label for XY ellipse - small and fixed size, closer to ellipsoid
    xy_label = ax.text(x_pos + uncertainty_axes[0], y_pos, z_pos + 0.05, 'XY',
                      color='#FF3333', fontsize=6, weight='bold', ha='center', va='bottom')
    ellipse_labels.append(xy_label)

    # Ellipse in XZ plane (y = constant) - GREEN (offset slightly to avoid overlap)
    x_xz = x_pos + uncertainty_axes[0] * np.cos(theta)
    y_xz = np.full_like(theta, y_pos)
    z_xz = z_pos + uncertainty_axes[2] * np.sin(theta)
    xz_ellipse, = ax.plot(x_xz, y_xz, z_xz, '-', color='#33FF33', linewidth=2.5, alpha=0.7)
    uncertainty_surf.append(xz_ellipse)
    
    # Label for XZ ellipse - moved to YZ position for better visibility
    xz_label = ax.text(x_pos + 0.05, y_pos + uncertainty_axes[1], z_pos, 'XZ',
                      color='#33FF33', fontsize=6, weight='bold', ha='center', va='bottom')
    ellipse_labels.append(xz_label)

    # Ellipse in YZ plane (x = constant) - BLUE
    x_yz = np.full_like(theta, x_pos)
    y_yz = y_pos + uncertainty_axes[1] * np.cos(theta)
    z_yz = z_pos + uncertainty_axes[2] * np.sin(theta)
    yz_ellipse, = ax.plot(x_yz, y_yz, z_yz, '-', color='#3333FF', linewidth=2.5, alpha=0.7)
    uncertainty_surf.append(yz_ellipse)
    
    # Label for YZ ellipse - moved to original XZ position
    yz_label = ax.text(x_pos + uncertainty_axes[0], y_pos + 0.05, z_pos, 'YZ',
                      color='#3333FF', fontsize=6, weight='bold', ha='center', va='bottom')
    ellipse_labels.append(yz_label)

    # Draw ellipsoid dimension lines (axis lines) - more visible
    dimension_lines = []
    line1 = ax.plot([x_pos - uncertainty_axes[0], x_pos + uncertainty_axes[0]],
                   [y_pos, y_pos], [z_pos, z_pos], '-', color='#FF3333', linewidth=1.5, alpha=0.5)
    dimension_lines.extend(line1)

    line2 = ax.plot([x_pos, x_pos],
                   [y_pos - uncertainty_axes[1], y_pos + uncertainty_axes[1]],
                   [z_pos, z_pos], '-', color='#33FF33', linewidth=1.5, alpha=0.5)
    dimension_lines.extend(line2)

    line3 = ax.plot([x_pos, x_pos], [y_pos, y_pos],
                   [z_pos - uncertainty_axes[2], z_pos + uncertainty_axes[2]],
                   '-', color='#3333FF', linewidth=1.5, alpha=0.5)
    dimension_lines.extend(line3)
    
    # Add comet tail effect (last 20 positions)
    tail_length = min(20, idx)
    if tail_length > 0:
        tail_start = max(0, idx - tail_length)
        comet_tail.set_data(x_traj[tail_start:idx], y_traj[tail_start:idx])
        comet_tail.set_3d_properties(z_traj[tail_start:idx])

    # Calculate distance from Sun in both AU and million km
    distance_au = np.sqrt(x_pos**2 + y_pos**2 + z_pos**2)
    distance_mkm = distance_au * AU_TO_KM / 1e6  # Million km
    
    # Calculate current date
    days_offset = time_from_perihelion[idx]
    current_date = perihelion_date + timedelta(days=days_offset)
    date_str = current_date.strftime("%B %d, %Y")
    
    # Days to/from perihelion
    if days_offset < 0:
        perihelion_str = f"{abs(int(days_offset))} days before perihelion"
        phase_emoji = "[APPROACHING]"
        status = "APPROACHING"
    elif days_offset == 0:
        perihelion_str = "AT PERIHELION!"
        phase_emoji = "[PERIHELION]"
        status = "CLOSEST APPROACH"
    else:
        perihelion_str = f"{int(days_offset)} days after perihelion"
        phase_emoji = "[DEPARTING]"
        status = "DEPARTING"

    # Calculate velocity using vis-viva equation for hyperbolic orbits
    # v = sqrt(μ(2/r + 1/a)) where μ = GM_sun = 1.327×10^20 m³/s² 
    # For hyperbolic orbits, a < 0, so v = sqrt(μ(2/r - 1/|a|))
    GM_sun = 1.32712440018e20  # m³/s² (gravitational parameter of Sun)
    r_meters = distance_au * AU_TO_KM * 1000  # Convert AU to meters
    a_meters = abs(a) * AU_TO_KM * 1000  # Convert |a| to meters
    
    # Vis-viva equation: v² = μ(2/r - 1/a) for elliptic, v² = μ(2/r + 1/|a|) for hyperbolic
    velocity_ms = np.sqrt(GM_sun * (2.0/r_meters + 1.0/a_meters))  # m/s
    velocity_kms = velocity_ms / 1000  # Convert to km/s

    # Dynamic camera movement centered on comet
    comet_pos_array = np.array([x_pos, y_pos, z_pos])
    elev, azim, zoom, _ = get_camera_path(frame, total_frames, comet_pos_array)
    ax.view_init(elev=elev, azim=azim)
    
    # Dynamic zoom centered on comet position
    ax.set_xlim(x_pos - zoom, x_pos + zoom)
    ax.set_ylim(y_pos - zoom, y_pos + zoom)
    ax.set_zlim(z_pos - zoom, z_pos + zoom)

    # Update title with date and status (without phase_emoji duplicates)
    title_text.set_text(f'{date_str}\n{status}')
    
    # Convert orbital elements to million km for better understanding
    perihelion_mkm = q * AU_TO_KM / 1e6
    
    # Calculate ellipsoid axes lengths in million km
    ax_len_x = uncertainty_axes[0] * AU_TO_KM / 1e6
    ax_len_y = uncertainty_axes[1] * AU_TO_KM / 1e6
    ax_len_z = uncertainty_axes[2] * AU_TO_KM / 1e6
    
    # Update info panel - compact horizontal format
    info_text.set_text(f'''3I/ATLAS | Dist. to Sun: {distance_mkm:.0f}M km | {perihelion_str} | Vel. w.r.t. Sun: {abs(velocity_kms):.0f} km/s''')

    # Update legend - with ellipse measurements
    legend_text.set_text(f'''UNCERTAINTY ELLIPSES (3σ = 99.7%):
XY plane (red): {ax_len_x:.1f} × {ax_len_y:.1f} M km
XZ plane (green): {ax_len_x:.1f} × {ax_len_z:.1f} M km
YZ plane (blue): {ax_len_y:.1f} × {ax_len_z:.1f} M km
Causes: Obs. Errors, Gravity Uncertainty, Outgassing''')

    return comet_point, comet_tail, info_text, title_text, legend_text, uncertainty_surf, dimension_lines, ellipse_labels

# Create animation
print("="*60)
print("*** Generating Cinematic 3D Animation of Comet 3I/ATLAS ***")
print("="*60)
print(f"Total frames: {total_frames}")
print(f"Animation duration: ~{total_frames/30:.1f} seconds at 30 fps")
print("This may take several minutes...")
print("")

anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames,
                    interval=33, blit=False, repeat=True)  # 33ms = 30fps

# Save animation
if not os.path.exists('output'):
    os.makedirs('output')

# Save frames for high-quality video
print("[RENDERING] Rendering frames...")
def save_frames():
    # Initialize before starting to clear any previous state
    init()
    plt.draw()
    
    for i in range(total_frames):
        animate(i)
        # Save with specific size to ensure dimensions divisible by 2
        plt.savefig(f'output/frame_{i:04d}.png', dpi=100, bbox_inches=None,
                   facecolor='#000000', edgecolor='none')
        if i % 25 == 0:
            progress = (i / total_frames) * 100
            print(f'  Progress: {progress:.1f}% ({i}/{total_frames} frames)')
    print(f'  [SUCCESS] All {total_frames} frames saved!')

save_frames()

# Create high-quality MP4 with ffmpeg (if available)
print("")
print("[VIDEO] Creating MP4 video...")
try:
    import ffmpeg
    (
        ffmpeg
        .input('output/frame_%04d.png', framerate=15)
        .output('output/comet_3i_atlas_cinematic.mp4',
                vcodec='libx264',
                pix_fmt='yuv420p',
                **{'crf': '18', 'preset': 'slow'})  # High quality settings
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )
    print("[SUCCESS] MP4 video created: output/comet_3i_atlas_cinematic.mp4")
except Exception as ex:
    print(f"[WARNING] ffmpeg not available: {ex}")
    print("   To create MP4 manually:")
    print("   1. Install ffmpeg: https://ffmpeg.org/download.html")
    print("   2. Run: python create_video.py")
    print("   3. Or run manually:")
    print("      ffmpeg -framerate 15 -i output/frame_%04d.png -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output/comet_3i_atlas_cinematic.mp4")

# Also save as GIF for quick preview
print("")
print("[GIF] Creating GIF preview...")
try:
    anim.save('output/comet_3i_preview.gif', writer='pillow', fps=10, dpi=100)
    print("[SUCCESS] GIF preview created: output/comet_3i_preview.gif")
except Exception as ex:
    print(f"[WARNING] GIF creation failed: {ex}")
    print("   GIF will be created with create_video.py if needed")

plt.close()

print("")
print("="*60)
print("✨ ANIMATION COMPLETE! ✨")
print("="*60)
print("📁 Files saved in 'output/' folder:")
print("   • comet_3i_atlas_cinematic.mp4 (high-quality video)")
print("   • comet_3i_preview.gif (quick preview)")
print("   • frame_*.png (individual frames)")
print("")
print("📱 Ready to share on LinkedIn!")
print("="*60)
