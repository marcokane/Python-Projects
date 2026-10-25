import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from scipy.optimize import fsolve

# --- 1. DATI GEOMETRICI E CONFIGURAZIONE INIZIALE ---
z1 = np.sqrt(2)
z2 = 2.0
z3 = 4.0

A = np.array([0.0, 3.0])
D = np.array([3.0, 0.0])

AD = D - A
z4 = np.linalg.norm(AD)
phi4 = np.arctan2(AD[1], AD[0])

def mechanism_equations(vars, phi1, phi4, z1, z2, z3, z4):
    phi2, phi3 = vars
    eq1 = z1 * np.cos(phi1) + z2 * np.cos(phi2) + z3 * np.cos(phi3) + z4 * np.cos(phi4)
    eq2 = z1 * np.sin(phi1) + z2 * np.sin(phi2) + z3 * np.sin(phi3) + z4 * np.sin(phi4)
    return [eq1, eq2]

# --- 2. PRE-CALCOLO DELLE POSIZIONI PER L'INTERO CICLO (360°) ---
n_frames = 180
phi1_values = np.linspace(0, 2 * np.pi, n_frames)

xB_list, yB_list = [], []
xC_list, yC_list = [], []
phi1_deg_list = []

guess = [np.pi / 8, -(np.pi * 5) / 8]

for phi1 in phi1_values:
    sol, info, ier, mesg = fsolve(
        mechanism_equations, guess, 
        args=(phi1, phi4, z1, z2, z3, z4), 
        full_output=True
    )
    if ier == 1:
        guess = sol
        phi2, phi3 = sol[0], sol[1]
        xB = A[0] + z1 * np.cos(phi1)
        yB = A[1] + z1 * np.sin(phi1)
        xC = xB + z2 * np.cos(phi2)
        yC = yB + z2 * np.sin(phi2)
        
        xB_list.append(xB)
        yB_list.append(yB)
        xC_list.append(xC)
        yC_list.append(yC)
        phi1_deg_list.append(np.rad2deg(phi1))
    else:
        xB_list.append(np.nan)
        yB_list.append(np.nan)
        xC_list.append(np.nan)
        yC_list.append(np.nan)
        phi1_deg_list.append(np.rad2deg(phi1))

# --- 3. CREAZIONE DELLA FIGURA E DEI WIDGET ---
fig, ax = plt.subplots(figsize=(8, 9))
plt.subplots_adjust(bottom=0.25)

# CALCOLO AUTOMATICO DEI LIMITI DINAMICI (Evita che il meccanismo esca dal grafico)
all_x = [A[0], D[0]] + xB_list + xC_list
all_y = [A[1], D[1]] + yB_list + yC_list
margin = 1.0
ax.set_xlim(np.nanmin(all_x) - margin, np.nanmax(all_x) + margin)
ax.set_ylim(np.nanmin(all_y) - margin, np.nanmax(all_y) + margin)

ax.set_aspect('equal')
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlabel('Coordinata X [m]', fontsize=12)
ax.set_ylabel('Coordinata Y [m]', fontsize=12)

title_text = ax.set_title('', fontsize=14)

# Disegno del telaio fisso
ax.plot([A[0], D[0]], [A[1], D[1]], color='gray', linestyle='--', linewidth=3, label='Telaio ($z_4$)')

# Elementi mobili del meccanismo
link1, = ax.plot([], [], color='blue', linewidth=4, marker='o', markersize=8, label='Manovella ($z_1$)')
link2, = ax.plot([], [], color='green', linewidth=4, marker='o', markersize=8, label='Biella ($z_2$)')
link3, = ax.plot([], [], color='orange', linewidth=4, marker='o', markersize=8, label='Bilanciere ($z_3$)')
ax.legend(loc='upper right', fontsize=11)

def update_plot(frame):
    idx = int(frame) % n_frames
    if np.isnan(xB_list[idx]):
        return
    
    xB, yB = xB_list[idx], yB_list[idx]
    xC, yC = xC_list[idx], yC_list[idx]
    p1_deg = phi1_deg_list[idx]
    
    link1.set_data([A[0], xB], [A[1], yB])
    link2.set_data([xB, xC], [yB, yC])
    link3.set_data([xC, D[0]], [yC, D[1]])
    
    title_text.set_text(rf'Animazione del Quadrilatero Articolato ($\phi_1 = {p1_deg:.1f}°$)')
    fig.canvas.draw_idle()

# --- 4. AGGIUNTA DELLO SLIDER E DEL PULSANTE ---
ax_slider = plt.axes([0.15, 0.12, 0.7, 0.03], facecolor='lightgoldenrodyellow')
slider_phi = Slider(
    ax=ax_slider,
    label=r'Angolo $\phi_1$ [°]',
    valmin=0.0,
    valmax=360.0,
    valinit=0.0,
    valstep=360.0 / n_frames
)

def on_slider_changed(val):
    frame = int((val / 360.0) * n_frames)
    update_plot(frame)

slider_phi.on_changed(on_slider_changed)

ax_button = plt.axes([0.4, 0.04, 0.2, 0.05])
btn_play = Button(ax_button, 'Pausa / Riprendi', color='lightgoldenrodyellow', hovercolor='0.975')

is_playing = True

def toggle_play(event):
    global is_playing
    is_playing = not is_playing
    if is_playing:
        ani.event_source.start()
    else:
        ani.event_source.stop()

btn_play.on_clicked(toggle_play)

current_frame = [0]
def animate(i):
    if is_playing:
        current_frame[0] = (current_frame[0] + 1) % n_frames
        slider_phi.eventson = False
        slider_phi.set_val(phi1_deg_list[current_frame[0]])
        slider_phi.eventson = True
        update_plot(current_frame[0])
    return link1, link2, link3

ani = FuncAnimation(fig, animate, frames=n_frames, interval=30, blit=False)

plt.show()