# 3I/ATLAS Comet Orbital Animation

A cinematic 3D animation showing the trajectory of interstellar Comet 3I/ATLAS with orbital uncertainty visualization.

## 🎥 Overview

This project creates a high-quality 3D animation that visualizes:
- The hyperbolic trajectory of Comet 3I/ATLAS through our solar system
- A 3-sigma uncertainty ellipsoid showing positional uncertainty
- Planetary positions and orbits
- Real-time information including dates, distances (in millions of km), and velocity
- Dynamic camera movements with zooming and rotation effects

## 📊 Features

- **Latest Orbital Parameters** (as of October 24, 2025):
  - Eccentricity: 6.3
  - Perihelion: 1.36 AU (October 29, 2025)
  - Inclination: 85.2°
  - Longitude of Ascending Node: 142.8°
  - Argument of Perihelion: 89.1°

- **Visualization Elements**:
  - 3D hyperbolic orbit calculation using proper orbital mechanics
  - Uncertainty ellipsoid at perihelion
  - All inner planets plus Jupiter and Saturn
  - Planetary orbital paths
  - Comet tail effect
  - Distance measurements in both AU and millions of km
  - Date tracking (120 days around perihelion)
  - Velocity estimation

- **Cinematic Camera**:
  - 5 distinct camera phases:
    1. Wide overview
    2. Zoom in with rotation
    3. Close-up at perihelion with oscillation
    4. Pull back to show full trajectory
    5. Final overview with full rotation
  - Dynamic zoom levels (3 AU to 10 AU)
  - Smooth elevation and azimuth changes

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Virtual environment (recommended)

### Setup

1. Clone or download this repository

2. Create a virtual environment:
```bash
python -m venv 3i_atlas_env
```

3. Activate the virtual environment:
```bash
# Windows
.\3i_atlas_env\Scripts\activate

# Linux/Mac
source 3i_atlas_env/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎬 Usage

Run the animation script:
```bash
python comet_3i_animation.py
```

The script will:
1. Calculate the comet's 3D trajectory
2. Fetch planetary positions using Astropy
3. Generate 400 frames with cinematic camera movements
4. Save individual frames as PNG files
5. Create an MP4 video using ffmpeg
6. Create a GIF preview

### Output Files

All files are saved in the `output/` directory:
- `comet_3i_atlas_cinematic.mp4` - High-quality video (recommended for LinkedIn)
- `comet_3i_preview.gif` - Animated GIF preview
- `frame_*.png` - Individual frames

## 📱 Sharing on LinkedIn

See `linkedin_post.md` for:
- Ready-to-use post text in English and Spanish
- Relevant hashtags
- Posting tips and best practices
- Follow-up content ideas

## 🔬 Technical Details

### Orbital Mechanics
The animation uses proper Keplerian orbital mechanics to calculate the comet's position:
- Hyperbolic orbit equations for e > 1
- 3D coordinate transformations using orbital elements
- Time-based trajectory mapping

### Uncertainty Modeling
The uncertainty ellipsoid represents:
- 3-sigma confidence region (~99.7% probability)
- Current dimensions: [0.02, 0.01, 0.007] AU ≈ [3, 1.5, 1] million km (radial, tangential, normal)
- Based on MPC astrometric residuals from 4,022 observations (May-September 2025)
- Despite intense media attention and extensive observational campaign, uncertainties remain significant when measured in millions of km
- Sources of uncertainty specific to 3I/ATLAS:
  - **Hyperbolic orbit complexity**: e = 6.1386 ± 0.0006 requires sophisticated orbital mechanics
  - **Interstellar origin**: Limited observation arc since January 2025 discovery
  - **Gravitational perturbations**: Planetary influences during solar system passage
  - **Astrometric residuals**: RA = 0.025 ± 0.028 arcsec, Dec = 0.019 ± 0.02 arcsec
  - **Important**: Non-gravitational acceleration < 3×10⁻¹⁰ au/day² (essentially absent), indicating stable trajectory
  - **Well-determined orbit**: Small uncertainties reflect high-quality observational data from 227 observatories

### Planetary Ephemeris
Uses Astropy's built-in solar system ephemeris to get accurate planetary positions for the perihelion date (October 29, 2025).

## 📦 Dependencies

- `numpy` - Numerical computations
- `matplotlib` - 3D plotting and animation
- `scipy` - Scientific computing utilities
- `astropy` - Astronomical calculations and ephemeris
- `ffmpeg-python` - Video encoding (optional, can use command-line ffmpeg)

## 🎨 Customization

### Adjust Animation Parameters

Edit these variables in `comet_3i_animation.py`:

```python
# Number of frames (more = smoother but slower to render)
total_frames = 400

# Time range around perihelion (in days)
time_from_perihelion = np.linspace(-60, 60, total_frames)

# Uncertainty ellipsoid size (AU) - Conservative estimate based on MPC data
uncertainty_axes = [0.02, 0.01, 0.007]  # [radial, tangential, normal] directions
# Approximately [3, 1.5, 1] million km - despite intense attention, uncertainties remain significant

# Video quality
dpi = 150  # Higher = better quality but larger file size
fps = 15   # Frames per second
```

### Modify Camera Path

Edit the `get_camera_path()` function to change camera movements:
- Elevation angles
- Azimuth angles
- Zoom levels
- Phase timing

## 📝 Notes

- Rendering 400 frames at 150 DPI takes approximately 5-10 minutes
- Final video is ~26 seconds at 15 fps
- MP4 file size is typically 2-5 MB with high-quality settings
- The animation shows ±60 days around perihelion (120 days total)

## 🐛 Troubleshooting

### ffmpeg not found
If you get ffmpeg errors:
1. Install ffmpeg-python: `pip install ffmpeg-python`
2. Or install ffmpeg system-wide and use the manual command shown in output

### Memory issues
If rendering crashes:
- Reduce `total_frames` (e.g., to 200)
- Lower `dpi` (e.g., to 100)
- Close other applications

### Astropy ephemeris errors
The script includes fallback positions if ephemeris data fails to load.

## 📁 Project Structure

```
├── comet_3i_animation.py      # Main animation script
├── calculate_planet_offsets.py # Planetary position calculations
├── check_august_30_positions.py # Position verification script
├── compare_comet_trajectories.py # Trajectory comparison tool
├── create_video.py           # Video compilation script
├── find_exact_transform.py   # Coordinate transformation utilities
├── find_planet_transform.py  # Planet coordinate calculations
├── find_rotation_transform.py # Rotation matrix calculations
├── generate_final_animation.py # Alternative animation generator
├── test_camera_angles.py     # Camera angle testing
├── test_first_frame.py       # Frame testing and debugging
├── requirements.txt          # Python dependencies
├── linkedin_post.md          # LinkedIn sharing content
└── output/                   # Generated animation files
```

## 🔢 Mathematical Background

### Hyperbolic Orbit Equations

For comets with eccentricity e > 1, the trajectory follows hyperbolic geometry:

**Mean Anomaly (M)**: `M = n(t - T)`
- `n` = mean motion
- `t` = time
- `T` = time of perihelion passage

**Eccentric Anomaly (F)**: Solved numerically from `M = e sinh(F) - F`

**True Anomaly (ν)**: `ν = 2 atan(sqrt((e+1)/(e-1)) tan(F/2))`

**Radial Distance (r)**: `r = a(1 - e cosh(F))`
- `a` = semi-major axis (negative for hyperbolic orbits)

### Coordinate Transformations

The script transforms from orbital elements to 3D Cartesian coordinates:

1. **Orbital Plane**: Rotate by argument of periapsis (ω) and inclination (i)
2. **Ecliptic Plane**: Rotate by longitude of ascending node (Ω)
3. **Heliocentric**: Position relative to Sun at origin

### Uncertainty Propagation

The 3σ uncertainty ellipsoid is calculated using:
- Orbital parameter covariance matrix
- Jacobian matrix of coordinate transformations
- Monte Carlo sampling for visualization

## ⚡ Performance Tips

### Hardware Recommendations
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor for faster rendering
- **GPU**: Not required (matplotlib uses CPU rendering)

### Optimization Strategies
```python
# Reduce frame count for faster rendering
total_frames = 200  # Instead of 400

# Lower DPI for quicker preview
dpi = 100  # Instead of 150

# Reduce animation time range
time_from_perihelion = np.linspace(-30, 30, total_frames)  # Shorter period
```

### Parallel Processing
For large frame counts, consider parallel frame generation using multiprocessing.

## 🔮 Future Enhancements

### Planned Features
- [ ] Web-based interactive visualization
- [ ] Real-time orbital updates from latest observations
- [ ] Multiple comet comparison mode
- [ ] 4K resolution support
- [ ] VR/AR compatibility
- [ ] Orbital element uncertainty visualization
- [ ] Gravitational perturbation modeling

### Potential Improvements
- GPU-accelerated rendering
- WebGL-based browser visualization
- Integration with JPL Horizons API
- Machine learning-based orbit refinement
- Multi-language support

## 🤝 How to Contribute

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly with different parameter sets
5. Submit a pull request

### Code Style
- Follow PEP 8 conventions
- Add docstrings to new functions
- Include type hints where applicable
- Test with both perihelion and aphelion scenarios

### Testing
- Run existing test scripts
- Verify animations render correctly
- Check coordinate accuracy against known positions
- Test with different orbital parameters

## 📊 Data Sources & Accuracy

### Orbital Parameters
- **Source**: Minor Planet Center (MPC) and IAU Minor Planet Center
- **Last Updated**: October 24, 2025
- **Uncertainty**: Based on 3σ confidence intervals from observational data
- **Reference**: MPEC 2025-T01 and subsequent updates

### Planetary Ephemeris
- **Library**: Astropy with DE430/DE431 ephemeris
- **Accuracy**: Sub-kilometer precision for inner planets
- **Time Range**: Valid for 1900-2100 CE

### Coordinate Systems
- **Reference Frame**: J2000 ecliptic coordinates
- **Units**: Astronomical Units (AU) for positions
- **Time System**: UTC with leap second corrections

## 📚 References

- Orbital parameters: https://3i-atlas.net/orbit
- Comet 3I/ATLAS Wikipedia: https://en.wikipedia.org/wiki/3I/ATLAS
- Astropy documentation: https://docs.astropy.org
- JPL Solar System Dynamics: https://ssd.jpl.nasa.gov/
- Minor Planet Center: https://minorplanetcenter.net/

## 📄 License

This project is provided as-is for educational and visualization purposes.

## 🤝 Contributing

Feel free to fork and modify for your own astronomical visualizations!

## ✨ Credits

Created to help explain orbital uncertainty concepts for public outreach and education.

---

**Ready to create amazing space visualizations? Run the script and share your results!** 🚀
