# Importing Packages
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import animation

# Earth model (we could replace this with any other body)
def model_2BP(state, t):
    mu = 3.986004418E+05 # Earth's gravitational parameter [km^3/s^2]

    x = state[0]
    y = state[1]
    z = state[2]
    x_dot = state[3]
    y_dot = state[4]
    z_dot = state[5]
    x_ddot = -mu * x / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2)
    y_ddot = -mu * y / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2)
    z_ddot = -mu * z / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2)
    dstate_dt = [x_dot, y_dot, z_dot, x_ddot, y_ddot, z_ddot]
    return dstate_dt

# Initial Conditions
X_0 = -2500  # [km]
Y_0 = -5500  # [km]
Z_0 = 3400  # [km]
VX_0 = 7.5  # [km/s]
VY_0 = 0.0  # [km/s]
VZ_0 = 4.0  # [km/s]
state_0 = [X_0, Y_0, Z_0, VX_0, VY_0, VZ_0]

# Time Array
t = np.linspace(0, 6*3600, 200)  # Simulates for a time period of 6 hours [s]

# Solving ODE
sol = odeint(model_2BP, state_0, t)
X_Sat = sol[:, 0]  # X-coord [km] of satellite over time interval 
Y_Sat = sol[:, 1]  # Y-coord [km] of satellite over time interval
Z_Sat = sol[:, 2]  # Z-coord [km] of satellite over time interval

# Setting up Spherical Earth to Plot
N = 50
phi = np.linspace(0, 2 * np.pi, N)
theta = np.linspace(0, np.pi, N)
theta, phi = np.meshgrid(theta, phi)

r_Earth = 6378.14  # Average radius of Earth [km]
X_Earth = r_Earth * np.cos(phi) * np.sin(theta)
Y_Earth = r_Earth * np.sin(phi) * np.sin(theta)
Z_Earth = r_Earth * np.cos(theta)

# Plotting Earth and Orbit
N = 50
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')

# Earth
ax.plot_surface(X_Earth, Y_Earth, Z_Earth,
                color='blue', alpha=0.6)

# Orbit trail
ax.plot3D(X_Sat, Y_Sat, Z_Sat,
          color='gray', linestyle='--', alpha=0.5)

# Satellite point
satellite, = ax.plot([], [], [], 'ro', markersize=6)

# Labels
ax.set_xlabel('X [km]')
ax.set_ylabel('Y [km]')
ax.set_zlabel('Z [km]')
plt.title('Two-Body Problem')

# Equal axis scaling
max_range = np.max(np.abs([X_Sat, Y_Sat, Z_Sat])) + 1000

ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)

ax.set_box_aspect([1,1,1])

ax.view_init(30, 145)

# Animation function
def update(frame):

    satellite.set_data([X_Sat[frame]], [Y_Sat[frame]])
    satellite.set_3d_properties([Z_Sat[frame]])

    return satellite,

# Create animation
ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(t),
    interval=50,
    blit=True
)

plt.show()