### Written by Victor Kappelhøj Andersen (s244824@dtu.dk)

import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch

import matplotlib 
matplotlib.rcParams['animation.embed_limit'] = 2**128
dir_path = os.path.dirname(os.path.realpath(__file__))

# user inputs
mode = int(input("""1: Default settings
          \n2: Custom settings\n""") or 1)

match mode:
    case 0: #FOR TESTING STOKES
        E0x, E0y = 1, 1
        psi_custom = np.deg2rad(int(input("Enter orientation in degrees: ") or 30))
        chi_custom = np.deg2rad(int(input("Enter ellipticity in degrees (sign = orientation): ") or 30))
        E0x, E0y = (
        (np.cos(psi_custom)*np.cos(chi_custom) - 1j*np.sin(psi_custom)*np.sin(chi_custom)), 
        (np.sin(psi_custom)*np.cos(chi_custom) + 1j*np.cos(psi_custom)*np.sin(chi_custom)))
        JM = np.array([
                    [0, 0],
                    [0, 1]])
        animation_mode, panning, pan_span, fps, step, plot_selection = 1, 1, 10.0, 50, 4, 4
    case 1:
        E0x, E0y = 1, 1j
        JM = np.array([
                    [0, 0],
                    [0, 1]])
        animation_mode, panning, pan_span, fps, step, plot_selection = 1, 1, 10.0, 50, 4, 1

    case 2:
        print("Leave empty for default values\n")
        plot_selection = int(input("""Choose what plots to display:
                                   \n1: All plots
                                   \n2: 2D polarizations only
                                   \n3: Animated plot only
                                   \n4: Poincaré Sphere only\n""") or 1)
        
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
                chi_custom = np.deg2rad(int(input("Enter ellipticity in degrees (sign = orientation): ") or 30))
                E0x, E0y = (
                (np.cos(psi_custom)*np.cos(chi_custom) - 1j*np.sin(psi_custom)*np.sin(chi_custom)), 
                (np.sin(psi_custom)*np.cos(chi_custom) + 1j*np.cos(psi_custom)*np.sin(chi_custom)))

        # skips having to select a jones matrix when dealing with poincaré sphere
        if plot_selection in [1, 2, 3]:
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

        if plot_selection in [1, 3, 4]:
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
# technically unnecessary, as most values eventually gets normalized
phi_x, phi_y = 0, 0             # phase retarders
c = 300000000                   # m/s
wavelength = 1550 * 1e-9        # nm
frequency = c / wavelength      # hz
omega = 2 * np.pi * frequency   # rad/s
k = 2*np.pi/1                   # rad/m (example wavelegnth lambda = 1) 
                                #(i forgot what lambda does in this case but we get 2 periods at 1 and it looks good)
z0 = 0                          # phase / wave number

# time
T = 2*np.pi/omega
t = np.linspace(0, 2*T, 1000) # 2 periods
phi = omega * t - k * z0
t_normal = t/np.max(t)

# physical field
Ex = E0x * np.exp(1j*(phi + phi_x))
Ey = E0y * np.exp(1j*(phi + phi_y))

# polarized light
JV = np.array([Ex, Ey])

# the poincaré sphere doesn't use jones matrix
if plot_selection in [1, 2, 3]:
    E_polarized = JM.dot(JV)
    Epx = E_polarized[0]
    Epy = E_polarized[1]

# jones vector to stokes parameters
def jones2stokes(Ex, Ey):
    S0 = np.abs(Ex)**2 + np.abs(Ey)**2
    S1 = np.abs(Ex)**2 - np.abs(Ey)**2
    S2 = 2 * np.real(np.conjugate(Ex) * Ey)
    S3 = 2 * np.imag(np.conjugate(Ex) * Ey)
    return np.array([S0, S1/S0, S2/S0, S3/S0], dtype=float)
SV = jones2stokes(E0x, E0y)

# stokes to jones vector
def stokes2jones(SV):
    S0, S1, S2, S3 = SV[0], SV[1], SV[2], SV[3]
    # S0 will always be = 1 because of normalization, so i won't be doing handling zero/nonzero cases

    if S1 >= 0:
        Ex = np.sqrt((1 + S1) / 2)
        Ey = (S2 + 1j * S3) / (2 * Ex) if not np.isclose(Ex, 0.0) else 0.0j # handles division by 0 cases
    else:
        Ey = np.sqrt((1 - S1) / 2)
        Ex = (S2 - 1j * S3) / (2 * Ey) if not np.isclose(Ey, 0.0) else 0.0j

    return np.sqrt(S0) * np.array([Ex, Ey], dtype=complex)

# test cases to prove the black magic fuckery works somehow
"""
jonesreconstructed = stokes2jones(SV)
print(f"Ex and Ey in jones: {E0x, E0y}")
print(f"stokes paramter: {SV}")
print(f"Ex and Ey reconstructed: {jonesreconstructed[0], jonesreconstructed[1]}")
print(f"stokes reconstructed: {jones2stokes(jonesreconstructed[0], jonesreconstructed[1])}")

Ex_rec = jonesreconstructed[0] * np.exp(1j*(phi + phi_x))
Ey_rec = jonesreconstructed[1] * np.exp(1j*(phi + phi_x))

plt.plot(Ex.real, Ey.real)
plt.plot(Ex_rec.real, Ey_rec.real, '--')
plt.plot()"""

# 2D plots
if plot_selection in [1, 2]:
    # pre polar
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))
    # 1) Complex Ex: real + imag
    ax[0].plot(t_normal, Ex.real, label='Re(Ex)')
    ax[0].plot(t_normal, Ex.imag, label='Im(Ex)')
    ax[0].set_title('Ex(t) in complex form')
    ax[0].set_xlabel('Normalized time (t)')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # 2) Complex Ey: real + imag
    ax[1].plot(t_normal, Ey.real, label='Re(Ey)')
    ax[1].plot(t_normal, Ey.imag, label='Im(Ey)')
    ax[1].set_title('Ey(t) in complex form')
    ax[1].set_xlabel('Normalized time (t)')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)

    # 3) Physical polarization curve (real projection)
    ax[2].plot(Ex.real, Ey.real)
    ax[2].set_title('Physical polarization: Re(Ey) vs Re(Ex)')
    ax[2].set_xlabel('Re(Ex)')
    ax[2].set_ylabel('Re(Ey)')
    ax[2].set_box_aspect(1)
    ax[2].axis('equal')
    ax[2].grid(True, alpha=0.3)

    fig.suptitle("Pre-polarization")
    plt.tight_layout()
    plt.show(block=False)
    plt.draw()

    # post polar
    fig, ax = plt.subplots(1, 3, figsize=(13, 4))

    # 1) Complex Epx: real + imag
    ax[0].plot(t_normal, Epx.real, label='Re(Epx)')
    ax[0].plot(t_normal, Epx.imag, label='Im(Epx)')
    ax[0].set_title('Epx(t) in complex form')
    ax[0].set_xlabel('Normalized time (t)')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # 2) Complex Epy: real + imag
    ax[1].plot(t_normal, Epy.real, label='Re(Epy)')
    ax[1].plot(t_normal, Epy.imag, label='Im(Epy)')
    ax[1].set_title('Epy(t) in complex form')
    ax[1].set_xlabel('Normalized time (t)')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)

    # 3) Physical polarization curve (real projection)
    ax[2].plot(Epx.real, Epy.real)
    ax[2].set_title('Physical polarization: Re(Epy) vs Re(Epx)')
    ax[2].set_xlabel('Re(Epx)')
    ax[2].set_ylabel('Re(Epy)')
    ax[2].set_box_aspect(1)
    ax[2].axis('equal')
    ax[2].grid(True, alpha=0.3)

    fig.suptitle("Post-polarization")
    plt.tight_layout()
    plt.show(block=False)
    plt.draw()

# animated polarizer plot
if plot_selection in [1, 3]:
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

    # 3D axis
    ax_left.quiver(-lim, 0, 0,  2 * lim, 0, 0, color="k", arrow_length_ratio=0.05, alpha=0.5)
    ax_left.quiver(0, -lim, 0,  0, 2 * lim, 0, color="k", arrow_length_ratio=0.05, alpha=0.5)
    ax_left.quiver(0, 0, 0, 0, 0, zmax, color="k", arrow_length_ratio=0.05, alpha=0.5)

    # represents the polarizer
    x_plane = np.linspace(-1, 1, 2)
    y_plane = np.linspace(-1, 1, 2)
    X_plane, Y_plane = np.meshgrid(x_plane, y_plane)
    Z_plane = np.ones_like(X_plane)

    ax_left.plot_surface( 
        X_plane, Y_plane, Z_plane,
        color="gray",
        alpha=0.15,
        linewidth=0,
        shade=False,
    )

    # axis labels
    ax_left.set_xlabel("Ex / Epx")
    ax_left.set_ylabel("Ey / Epy", labelpad=10)
    ax_left.set_zlabel("Normalized time (t)")
    ax_left.set_title("Polarization in 3D")
    ax_left.legend()

    # animation parameters
    frame_idx = np.arange(0, len(Ex), step)

    n = len(frame_idx)
    half = n // 2

    # panning
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

    # wave function
    periods = 2
    def wave(E0x, E0y, z_axis, t):
        phase = omega * t - periods * k * z_axis
        x = np.real(E0x * np.exp(1j * (phase + phi_x)))
        y = np.real(E0y * np.exp(1j * (phase + phi_y)))
        return x, y

    # initial first position
    E0x_post = Epx[0]
    E0y_post = Epy[0]

    # update animation
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

    # choose output file type
    match animation_mode:
        case 2: 
            print("Saving video animation, please allow a few minutes ...")
            ani.save(f"{dir_path}/polarizer.gif", writer="pillow")
            plt.close(fig)
            print(f"Saved in {dir_path}/polarizer.gif")
        case 3:
            print("Saving video animation, please allow a few minutes  ...")
            ani.save(f"{dir_path}/polarizer.mp4", writer="ffmpeg")
            plt.close(fig)
            print(f"Saved in {dir_path}/polarizer.mp4")
    plt.show()

# poincaré and stokes
if plot_selection in [1, 4]:
    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.25)
    fig.subplots_adjust(left=0.0, right=0.97, bottom=0.0, top=1.0, hspace=0.2, wspace=0.2)

    ax_left = fig.add_subplot(gs[0, 0], projection="3d")
    ax_right = fig.add_subplot(gs[0, 1])

    theta = np.linspace(0, 2 * np.pi, 120)
    phi = np.linspace(0, np.pi, 60)
    theta, phi = np.meshgrid(theta, phi)

    r = 1.0
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)

    # sphere
    ax_left.plot_surface(x, y, z, alpha=0.05, linewidth=0.25, color="black", edgecolor="black", antialiased=True, shade=False)

    # stokes vector
    ax_left.quiver(0, 0, 0, SV[1], SV[2], SV[3], color="red", arrow_length_ratio=0.1)
    ax_left.quiver(SV[1], SV[2], 0, 0, 0, SV[3], color="red", arrow_length_ratio=0, alpha=0.3, linestyle="--")

    # axis
    ax_left.quiver(-1,  0,  0,  2, 0, 0, color="k", arrow_length_ratio=0, alpha=0.5)
    ax_left.quiver( 0, -1,  0,  0, 2 ,0, color="k", arrow_length_ratio=0, alpha=0.5)
    ax_left.quiver( 0,  0, -1,  0, 0, 2, color="k", arrow_length_ratio=0, alpha=0.5)

    # circles
    x_xy = r * np.cos(theta)
    y_xy = r * np.sin(theta)
    z_xy = np.full_like(theta, 0) # Constant Z
    ax_left.plot(x_xy, y_xy, z_xy, label='Parallel to XY plane', color='red', alpha=0.25)

    x_xz = r * np.cos(theta)
    y_xz = np.full_like(theta, 0) # Constant Y
    z_xz = r * np.sin(theta)
    ax_left.plot(x_xz, y_xz, z_xz, label='Parallel to XZ plane', color='green', alpha=0.25)

    x_xz = np.full_like(theta, 0) # Constant X
    y_xz = r * np.cos(theta)
    z_xz = r * np.sin(theta)
    ax_left.plot(x_xz, y_xz, z_xz, label='Parallel to YZ plane', color='blue', alpha=0.25)

    # limits
    ax_left.set_title("Poincaré sphere")
    ax_left.set_box_aspect((1, 1, 1))
    ax_left.set_xlim(-1, 1)
    ax_left.set_ylim(-1, 1)
    ax_left.set_zlim(-1, 1)
    ax_left.view_init(elev=15, azim=-20, roll=None)

    # useful for determining view_init
    # %matplotlib qt
    #def update_view(event):
    #    fig.suptitle(f"elev={ax.elev:.1f}, azim={ax.azim:.1f}, roll={ax.roll:.1f}")
    #    fig.canvas.draw_idle()
    #    fig.canvas.mpl_connect("motion_notify_event", update_view)
    #    fig.canvas.mpl_connect("button_release_event", update_view)

    # normal 2D polarization plot
    ax_right.plot(Ex.real, Ey.real)
    ax_right.set_xlim(-1, 1)
    ax_right.set_ylim(-1, 1)
    ax_right.set_box_aspect(1)
    ax_right.set_title('Physical polarization: Re(Ey) vs Re(Ex)')
    ax_right.set_xlabel('Re(Ex)')
    ax_right.set_ylabel('Re(Ey)')
    ax_right.axis('equal')
    ax_right.grid(True, alpha=0.3)

    plt.show(block=False)

# animated poincaré and stokes
if plot_selection in [1, 4]:
    fig = plt.figure(figsize=(12, 6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.25)
    fig.subplots_adjust(left=0.0, right=0.97, bottom=0.0, top=1.0, hspace=0.2, wspace=0.2)

    ax_left = fig.add_subplot(gs[0, 0], projection="3d")
    ax_right = fig.add_subplot(gs[0, 1])
    ax_right.set_autoscale_on(False)
    ### 3D plot
    # sphere paramters
    theta = np.linspace(0, 2 * np.pi, 120)
    phi = np.linspace(0, np.pi, 60)
    theta, phi = np.meshgrid(theta, phi)

    r = 1.0
    x = r * np.cos(theta) * np.sin(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(phi)

    # sphere
    ax_left.plot_surface(x, y, z, alpha=0.05, linewidth=0.25, color="black", edgecolor="black", antialiased=True, shade=False)

    # axis
    ax_left.quiver(-1,  0,  0,  2, 0, 0, color="k", arrow_length_ratio=0, alpha=0.5)
    ax_left.quiver( 0, -1,  0,  0, 2 ,0, color="k", arrow_length_ratio=0, alpha=0.5)
    ax_left.quiver( 0,  0, -1,  0, 0, 2, color="k", arrow_length_ratio=0, alpha=0.5)

    # circles
    x_xy = r * np.cos(theta)
    y_xy = r * np.sin(theta)
    z_xy = np.full_like(theta, 0) # Constant Z
    ax_left.plot(x_xy, y_xy, z_xy, label='Parallel to XY plane', color='red', alpha=0.25)

    x_xz = r * np.cos(theta)
    y_xz = np.full_like(theta, 0) # Constant Y
    z_xz = r * np.sin(theta)
    ax_left.plot(x_xz, y_xz, z_xz, label='Parallel to XZ plane', color='green', alpha=0.25)

    x_xz = np.full_like(theta, 0) # Constant X
    y_xz = r * np.cos(theta)
    z_xz = r * np.sin(theta)
    ax_left.plot(x_xz, y_xz, z_xz, label='Parallel to YZ plane', color='blue', alpha=0.25)

    # limits
    ax_left.set_box_aspect((1, 1, 1))
    ax_left.set_xlim(-1, 1)
    ax_left.set_ylim(-1, 1)
    ax_left.set_zlim(-1, 1)
    ax_left.view_init(elev=15, azim=-20, roll=None)
        
    ### 2D plot
    ax_right.set_xlim(-1.05, 1.05)
    ax_right.set_ylim(-1.05, 1.05)
    ax_right.set_box_aspect(1)
    ax_right.set_aspect("equal", adjustable="box")
    ax_right.set_title('Physical polarization: Re(Ey) vs Re(Ex)')
    ax_right.set_xlabel('Re(Ex)')
    ax_right.set_ylabel('Re(Ey)')
    ax_right.grid(True, alpha=0.3)

    # points to be traced
    # every point shall be a unit vector on the sphere
    path_points = [
        SV[1:],
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
        np.array([0.0, -1.0, 0]),
        np.array([1.0, 0.0, 0.0]),
        SV[1:],
    ]

    ### DISCLAIMER: Most code from this point onwards was heavily AI generated, but thoroughly reviewed and slightly revised

    def normalize(v):
        v = np.asarray(v, dtype=float)
        n = np.linalg.norm(v)
        return v / n if n != 0 else v

    def make_path(points, steps_per_segment=60):
        points = [normalize(p) for p in points]
        path = []
        for p0, p1 in zip(points[:-1], points[1:]):
            for a in np.linspace(0.0, 1.0, steps_per_segment, endpoint=False):
                path.append(normalize((1.0 - a) * p0 + a * p1))
        path.append(points[-1])
        return np.array(path)
    
    path_resolution = 50
    path = make_path(path_points, steps_per_segment= path_resolution)
    
    # 3D path artists
    path_line, = ax_left.plot([], [], [], color="red", lw=2)
    current_tip = {"artist": ax_left.quiver(0, 0, 0, *path[0], color="red", arrow_length_ratio=0.1)}
    current_marker, = ax_left.plot([], [], [], "o", color="red", markersize=5)

    # 2D path artists
    jones_curve, = ax_right.plot([], [], lw=2)
    jones_marker, = ax_right.plot([], [], "o", markersize=5)

    jones_arrow_length = 0.1
    jones_arrow = FancyArrowPatch(
        (0, 0), (0, 0),
        arrowstyle="->",
        mutation_scale=18,
        color="red",
        linewidth=2,
        zorder=10,
    )
    ax_right.add_patch(jones_arrow)

    phase = np.linspace(0.0, 2 * np.pi, 250)

    def jones_ellipse(jv):
        Ex0, Ey0 = jv
        return np.real(Ex0 * np.exp(1j * phase)), np.real(Ey0 * np.exp(1j * phase))
    
    def update_jones_arrow(arrow, x0, y0, x1, y1, length):
        direction = np.array([x1 - x0, y1 - y0], dtype=float)
        norm = np.linalg.norm(direction)
        if norm == 0:
            return
        direction /= norm
        arrow.set_positions(
            (x0, y0),
            (x0 + direction[0] * length, y0 + direction[1] * length),
    )
    
    frame_idx = np.arange(0, len(path))
    n = len(frame_idx)

    # update animation
    def update(i):
        k = frame_idx[i]
        sv_xyz = path[k]

        # trace the line already visited
        trace = path[:k + 1]
        path_line.set_data_3d(trace[:, 0], trace[:, 1], trace[:, 2])

        # move the arrow tip
        current_tip["artist"].remove()
        current_tip["artist"] = ax_left.quiver(
            0, 0, 0, sv_xyz[0], sv_xyz[1], sv_xyz[2],
            color="red", arrow_length_ratio=0.1
        )
        current_marker.set_data_3d([sv_xyz[0]], [sv_xyz[1]], [sv_xyz[2]])

        # convert the current Stokes point back to a Jones vector
        current_sv = np.array([1.0, sv_xyz[0], sv_xyz[1], sv_xyz[2]], dtype=float)
        jv = stokes2jones(current_sv)

        Ex_curve, Ey_curve = jones_ellipse(jv)

        jones_curve.set_data(Ex_curve, Ey_curve)
        
        x0, y0 = Ex_curve[0], Ey_curve[0]
        x1, y1 = Ex_curve[1], Ey_curve[1]
        update_jones_arrow(jones_arrow, x0, y0, x1, y1, jones_arrow_length)

        #jones_marker.set_data([Ex_curve[0]], [Ey_curve[0]])
        #return path_line, current_marker, current_tip["artist"], jones_curve, jones_marker
        return path_line, current_marker, current_tip["artist"], jones_curve

    ani = animation.FuncAnimation(fig=fig, func=update, frames=len(frame_idx), interval=1000/fps, blit=False)

    # choose output file type
    match animation_mode:
        case 2: 
            print("Saving video animation, please allow a few minutes ...")
            ani.save(f"{dir_path}/poincare.gif", writer="pillow")
            plt.close(fig)
            print(f"Saved in {dir_path}/poincare.gif")
        case 3:
            print("Saving video animation, please allow a few minutes ...")
            ani.save(f"{dir_path}/poincare.mp4", writer="ffmpeg")
            plt.close(fig)
            print(f"Saved in {dir_path}/poincare.gif")
    plt.show()
