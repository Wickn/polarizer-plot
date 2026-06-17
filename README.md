# Polarization Plots in Python
## Dependencies
- Python 3.12 (higher or lower might very well work)
- MatPlotLib (PyPlot and Animation)
- NumPy
- FFMPEG in PATH (If you wish to export to .mp4)
- Pillow (If you wish to export to .gif)
## Features
Visualize the state of polarization of light as it traverses through a polarizer, calculated through Jones Calculus.
- Show a 2D representation of the light pre- and post polarization
- Show a 2D and 3D animation that shows the wave transversing free space in time
- Allows exporting to .gif and .mp4 formats. (Note: .mp4 export requires ffmpeg in PATH)
- Panning 3D plot to better visualize that the wave propagates in 3 dimensions (NOT recommended if you get seasick)

Visualize the Poincaré Sphere through Stokes Parameters.
- Shows a 3D plot of the Poincaré sphere, along with a Stokes Vector generated based on the chosen Jones Vector
- Shows a 2D plot of the Jones Vector based on the Stokes Parameters
- A 3D animation is shown, showing the Stokes Parameters traverse the sphere, and updating the Jones Vector representation in real time
- Allows exporting to .gif and .mp4 formats. (Note: .mp4 export requires ffmpeg in PATH)
## Usage
Simply run the script "polarizer plot.py" and indicate your desired settings when prompted.

## Examples
### Polarizer plots with default settings:

![](https://github.com/Wickn/polarizer-plot/blob/main/example%20images/2d%20polarization%20plots.png)
![](https://github.com/Wickn/polarizer-plot/blob/main/example%20images/polarizer.gif)
### Poincaré plots with default elliptical polarization:

![](https://github.com/Wickn/polarizer-plot/blob/main/example%20images/poincare%20plot.png)
![](https://github.com/Wickn/polarizer-plot/blob/main/example%20images/poincare.gif)
