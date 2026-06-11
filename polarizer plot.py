### Written by Victor Kappelhøj Andersen (s244824@dtu.dk)

import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import matplotlib 
matplotlib.rcParams['animation.embed_limit'] = 2**128

dir_path = os.path.dirname(os.path.realpath(__file__))

# user inputs
print("Leave empty for defaults\n")
pre_polar = int(input("""Light polarization:
                      \n1: Right hand circular
                      \n2: Left hand circular
                      \n3: Linear (Horizontal)
                      \n4: Linear (Vertical)
                      \n5: Linear (45 degrees)
                      \n6: Linear (-45 degrees)
                      \n7: Linear (Custom)
                      \n8: Elliptical polarization (Custom)\n""") or 1)
match pre_polar:
    case 1: # right hand circular
        E0x, E0y = 1, 1j
    case 2: # left hand circular
        E0x, E0y = 1, -1j
    case 3: # linear, horizontal
        E0x, E0y = 1, 0
    case 4: # linear, vertical
        E0x, E0y = 0, 1
    case 5: # linear, 45 degrees
        E0x, E0y = 1, 1 
    case 6: # linear, -45 degrees
        E0x, E0y = 1, -1
    case 7: # linear, custom rotation
        phi_custom = np.deg2rad(int(input("Enter rotation in degrees: ") or 30))
        E0x, E0y = np.cos(phi_custom), np.sin(phi_custom)
    case 8: # ellipical, custom
        psi_custom = np.deg2rad(int(input("Enter orientation in degrees: ") or 30))
        chi_custom = (int(input("Enter ellipticity in degrees (sign = orientation): ") or 30))
        E0x, E0y = (
        (np.cos(psi_custom)*np.cos(chi_custom) - 1j*np.sin(psi_custom)*np.sin(chi_custom)), 
        (np.sin(psi_custom)*np.cos(chi_custom) + 1j*np.cos(psi_custom)*np.sin(chi_custom)))

post_polar = int(input("""Polarizer:
                      \n1: Right hand circular
                      \n2: Left hand circular
                      \n3: Linear (Horizontal)
                      \n4: Linear (Vertical)
                      \n5: Linear (45 degrees)
                      \n6: Linear (-45 degrees)
                      \n7: Linear (Custom rotation)\n""") or 4)
match post_polar:
    case 1: # right hand circular
        JM = 1/2 * np.array([
            [1, 1j],
            [-1j, 1]]) 
    case 2: # left hand circular
        JM = 1/2 * np.array([
            [1, -1j],
            [1j, 1]]) 
    case 3: # linear, horizsontal
        JM = np.array([
            [1, 0],
            [0, 0]]) 
    case 4: # linear, vertical
        JM = np.array([
            [0, 0],
            [0, 1]])
    case 5: # linear, 45 degrees
        JM = 1/2 * np.array([
            [1, 1],
            [1, 1]]) 
    case 6: # linear, -45 degrees
        JM = 1/2 * np.array([
            [1, -1],
            [-1, 1]])
    case 7: # linear, custom rotation
        phi_custom = np.deg2rad(int(input("Enter rotation in degrees: ") or 30))
        JM = np.array([
            [np.cos(phi_custom)*np.cos(phi_custom), np.cos(phi_custom)*np.sin(phi_custom)],
            [np.cos(phi_custom)*np.sin(phi_custom), np.sin(phi_custom)*np.sin(phi_custom)]])

animation_mode = int(input("""Choose animation output: 
                           \n1: MatPlotLib interactive
                           \n2: .gif (Need package Pillow)
                           \n3: .mp4 (Need ffmpeg in PATH)\n""") or 1)

panning = int(input("""Animation pan?
                    \n1: No pan
                    \n2: Pan\n""") or 1)

if panning == 2: pan_span = float(input("Pan span (Default 10.0): ") or 10.0)

fps = int(input("Framerate (Default 50fps): ") or 50)

step = int(input("Animation speed (Default 4): ") or 4)

# parameters
phi_x, phi_y = 0, 0             # phase retarders
c = 300000000                   # m/s
wavelength = 1550 * 1e-9        # nm
frequency = c / wavelength      # hz
omega = 2 * np.pi * frequency   # rad/s
k = 2*np.pi/1                   # rad/m (example wavelegnth lambda = 1) 
                                #(i forgot what lambda does in this case but we get 2 periods at 1 and it looks good)
z0 = 0

# time
T = 2*np.pi/omega
t = np.linspace(0, 2*T, 1000) # 2 periods
phi = omega * t - k * z0

# physical field
Ex = E0x * np.exp(1j*(phi + phi_x))
Ey = E0y * np.exp(1j*(phi + phi_y))

fig, ax = plt.subplots(1, 3, figsize=(13, 4))

# 1) Complex Ex: real + imag
ax[0].plot(t, Ex.real, label='Re(Ex)')
ax[0].plot(t, Ex.imag, label='Im(Ex)')
ax[0].set_title('Ex(t) in complex form')
ax[0].set_xlabel('t')
ax[0].legend()
ax[0].grid(True, alpha=0.3)

# 2) Complex Ey: real + imag
ax[1].plot(t, Ey.real, label='Re(Ey)')
ax[1].plot(t, Ey.imag, label='Im(Ey)')
ax[1].set_title('Ey(t) in complex form')
ax[1].set_xlabel('t')
ax[1].legend()
ax[1].grid(True, alpha=0.3)

# 3) Physical polarization curve (real projection)
ax[2].plot(Ex.real, Ey.real)
ax[2].set_title('Physical polarization: Re(Ey) vs Re(Ex)')
ax[2].set_xlabel('Re(Ex)')
ax[2].set_ylabel('Re(Ey)')
ax[2].axis('equal')
ax[2].grid(True, alpha=0.3)

fig.suptitle("Pre-polarization")
plt.tight_layout()
plt.show(block=False)
plt.draw()

JV = np.array([Ex, Ey])

E_polarized = JM.dot(JV)
Epx = E_polarized[0]
Epy = E_polarized[1]

fig, ax = plt.subplots(1, 3, figsize=(13, 4))

# 1) Complex Epx: real + imag
ax[0].plot(t, Epx.real, label='Re(Epx)')
ax[0].plot(t, Epx.imag, label='Im(Epx)')
ax[0].set_title('Epx(t) in complex form')
ax[0].set_xlabel('t')
ax[0].legend()
ax[0].grid(True, alpha=0.3)

# 2) Complex Epy: real + imag
ax[1].plot(t, Epy.real, label='Re(Epy)')
ax[1].plot(t, Epy.imag, label='Im(Epy)')
ax[1].set_title('Epy(t) in complex form')
ax[1].set_xlabel('t')
ax[1].legend()
ax[1].grid(True, alpha=0.3)

# 3) Physical polarization curve (real projection)
ax[2].plot(Epx.real, Epy.real)
ax[2].set_title('Physical polarization: Re(Epy) vs Re(Epx)')
ax[2].set_xlabel('Re(Epx)')
ax[2].set_ylabel('Re(Epy)')
ax[2].axis('equal')
ax[2].grid(True, alpha=0.3)

fig.suptitle("Post-polarization")
plt.tight_layout()
plt.show(block=False)
plt.draw()

# layout
fig = plt.figure(figsize=(13, 8), dpi=125)
gs = fig.add_gridspec(2, 2, width_ratios=[2.45, 1.35], wspace=0.03, hspace=0.32)
fig.subplots_adjust(left=0.001, right=0.985, bottom=0.07, top=0.95)

ax_left = fig.add_subplot(gs[:, 0], projection="3d")
ax_top = fig.add_subplot(gs[0, 1])
ax_bot = fig.add_subplot(gs[1, 1])

x0, y0 = 0.0, 0.0

zmax = 2.0
z = np.linspace(0.0, 1, len(Ex))
z_after = z + 1

lim = 1.1 * max(
    np.max(np.abs(Ex.real)), np.max(np.abs(Ey.real)),
    np.max(np.abs(Epx.real)), np.max(np.abs(Epy.real))
)

# 2D before polarizer
ax_top.set_title("Before polarizer", pad=8)
ax_top.set_xlabel("E0x", labelpad=6)
ax_top.set_ylabel("E0y")
ax_top.set_xlim(-lim, lim)
ax_top.set_ylim(-lim, lim)
ax_top.set_aspect("equal", adjustable="box")
ax_top.grid()
ax_top.plot(Ex.real, Ey.real, alpha=0.3)
q_pre = ax_top.quiver(x0, y0, Ex.real[0], Ey.real[0], angles="xy", scale_units="xy", scale=1)

# 2D after polarizer
ax_bot.set_title("After polarizer", pad=12)
ax_bot.set_xlabel("Epx", labelpad=6)
ax_bot.set_ylabel("Epy")
ax_bot.set_xlim(-lim, lim)
ax_bot.set_ylim(-lim, lim)
ax_bot.set_aspect("equal", adjustable="box")
ax_bot.grid()
ax_bot.plot(Epx.real, Epy.real, alpha=0.3)
q_post = ax_bot.quiver(x0, y0, Epx.real[0], Epy.real[0], angles="xy", scale_units="xy", scale=1)
E_pre, = ax_left.plot(Ex.real, Ey.real, z, label="Before")
E_post, = ax_left.plot(Epx.real, Epy.real, z_after, label="After")

# 3D
ax_left.set_xlim(-lim, lim)
ax_left.set_ylim(lim, -lim)
ax_left.set_zlim(0.0, zmax)
ax_left.set_box_aspect((2 * lim, 2 * lim, zmax))
ax_left.set_anchor("E")

ax_left.quiver(-lim, 0, 0,  2 * lim, 0, 0, color="k", arrow_length_ratio=0.05, alpha=0.5)
ax_left.quiver(0, -lim, 0,  0, 2 * lim, 0, color="k", arrow_length_ratio=0.05, alpha=0.5)
ax_left.quiver(0, 0, 0, 0, 0, zmax, color="k", arrow_length_ratio=0.05, alpha=0.5)

x_plane = np.linspace(-0.75, 0.75, 2)
y_plane = np.linspace(-0.75, 0.75, 2)
X_plane, Y_plane = np.meshgrid(x_plane, y_plane)
Z_plane = np.ones_like(X_plane)

ax_left.plot_surface(
    X_plane, Y_plane, Z_plane,
    color="gray",
    alpha=0.15,
    linewidth=0,
    shade=False,
)

ax_left.set_xlabel("Ex / Epx")
ax_left.set_ylabel("Ey / Epy", labelpad=10)
ax_left.set_zlabel("Normalized time")
ax_left.set_title("Polarization in 3D")
ax_left.legend()

# update animations
frame_idx = np.arange(0, len(Ex), step)

periods = 2
def wave(E0x, E0y, z_axis, t):
    phase = omega * t - periods * k * z_axis
    x = np.real(E0x * np.exp(1j * (phase + phi_x)))
    y = np.real(E0y * np.exp(1j * (phase + phi_y)))
    return x, y

E0x_post = Epx[0]
E0y_post = Epy[0]

n = len(frame_idx)
half = n // 2

elev_default = 160
azim_default = 150
roll_default = 80

if panning == 2:
    roll_up = np.linspace(0, pan_span, half, endpoint=False)
    roll_down = np.linspace(pan_span, 0, n - half)
    roll_delta = np.concatenate([roll_up, roll_down])

    elev_delta = 2 * roll_delta

    elev_start = elev_default - pan_span/2
    azim_start = 150
    roll_start = roll_default - pan_span/4

if panning == 2:
    ax_left.view_init(elev=elev_start, azim=azim_start, roll=roll_start)        # initial position
else:    
    ax_left.view_init(elev=elev_default, azim=azim_default, roll=roll_default)  # default position

def update(i):
    k = frame_idx[i]
    t_i = t[k]
    x_pre, y_pre = wave(E0x, E0y, z, t_i)
    x_post, y_post = wave(E0x_post, E0y_post, z_after, t_i)

    E_pre.set_data_3d(x_pre, y_pre, z)
    E_post.set_data_3d(x_post, y_post, z_after)

    q_pre.set_UVC(Ex.real[k], Ey.real[k])
    q_post.set_UVC(Epx.real[k], Epy.real[k])

    if panning == 2:
        ax_left.view_init(elev=elev_start + elev_delta[i], azim=azim_start, roll=roll_start + roll_delta[i])

    return (q_pre, q_post, E_pre, E_post)

ani = animation.FuncAnimation(fig=fig, func=update, frames=len(frame_idx), interval=1000/fps, blit=False)

match animation_mode:
    case 2: 
        print("Saving video animation, please wait up to 1 minute...")
        ani.save(f"{dir_path}/polarizer.gif", writer="pillow")
        plt.close(fig)
        print(f"Saved in {dir_path}/polarizer.gif")
    case 3:
        print("Saving video animation, please wait up to 1 minute ...")
        ani.save(f"{dir_path}/polarizer.mp4", writer="ffmpeg")
        plt.close(fig)
        print(f"Saved in {dir_path}/polarizer.mp4")
plt.show()