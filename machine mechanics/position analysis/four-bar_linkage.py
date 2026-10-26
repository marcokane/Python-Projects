import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

#DEFINISCO I DATI DI PARTENZA

print(f"DATI NOTI:")
#lunghezze dei membri
z1 = np.sqrt(2)
print(f"Lunghezza della manovella: z1 = {z1} m ",)
z2 = 2
print(f"Lunghezza della biella: z2 = {z2} m")
z3 = 4
print(f"Lunghezza del bilancere: z3 = {z3} m")
#angolo di manovella (coordinata libera)
phi1 = np.pi / 10
phi1deg = np.rad2deg(phi1)
print(f"Angolo di manovella: \u03C61 = {phi1deg}°")
#posizione degli estremi del telaio rispetto al sistema di riferimento
A = np.array ([0 , 3])
D = np.array ([3 , 0])
O = np.array ([0 , 0])
print(f"Posizione di un estremo del telaio (rispetto al sistema di riferimento) [m]: A = {A}")
print(f"Posizione di un estremo del telaio (rispetto al sistema di riferimento) [m]: D = {D}")
print(f"Posizione del sistema di riferimento [m]: O = {O}")

#RICAVO LA LUNGHEZZA DEL TELAIO E IL SUO ANGOLO RISPETTO ALL'ASSE X

print(f"RICAVO LA LUNGHEZZA DEL TELAIO E IL SUO ANGOLO RISPETTO ALL'ASSE X:")
z4 = np.sqrt((D[0] - A[0])**2 + (D[1] - A[1])**2)
print(f"Lunghezza del telaio: z4 = {z4} m")
phi4 = np.atan2 (D[1] - A[1] , D[0] - A[0])
phi4deg = np.rad2deg(phi4)
print(f"Angolo del telaio: \u03C64 = {phi4deg}°")

#IMPOSTO LE EQUAZIONI DI CHIUSURA LUNGO GLI ASSI

#imposto la funzione che imposta il modello matematico basato sulla chiusura vettoriale
def mechanism_equations (vars, phi1, phi4, z1, z2, z3, z4):
    phi2, phi3 = vars

    eq1 = z1 * np.cos(phi1) + z2 * np.cos(phi2) + z3 * np.cos(phi3) + z4 * np.cos(phi4)     #lungo x
    eq2 = z1 * np.sin(phi1) + z2 * np.sin(phi2) + z3 * np.sin(phi3) + z4 * np.sin(phi4)     #lungo y

    return  [eq1, eq2]

#IMPOSTO I VALORI DELLA PRIMA ITERAZIONE

print(f"IMPOSTO I VALORI PER LA PRIMA ITERAZIONE")
guess = [np.pi /8 , -(np.pi *5)/8]
print(f"Valori di partenza: t1 = 225° ; t2 = -112,5°")

#IMPOSTO LA STRUTTURA DEI CALCOLI COMPUTAZIONALI

sol, info, ier, mesg = fsolve(mechanism_equations, guess, args=(phi1, phi4, z1, z2, z3, z4), full_output=True)

#CONTROLLO IL SUCCESSO DEL METODO E STAMPO I RISULTATI

print(f"RISULTATI OTTENUTI:")
if ier == 1:
    phi2_res = np.rad2deg(sol[0])
    phi3_res = np.rad2deg(sol[1])
    
    print(f"Angolo della biella: phi2 = {phi2_res}°")
    print(f"Angolo del bilanciere: phi3 = {phi3_res}°")
else:
    print("Attenzione: il risolutore non è riuscito a convergere.")


#GRAFICO ILLUSTRATIVO DEL MECCANISMO

#CALCOLO DELLE COORDINATE DEI NODI PER IL DISEGNO 
#Estraggo gli angoli calcolati dal risolutore (in radianti)
phi2 = sol[0]
phi3 = sol[1]

#Coordinate dei perni fissi del telaio
xA, yA = A[0], A[1]
xD, yD = D[0], D[1]

#Coordinate del nodo B (estremo tra manovella z1 e biella z2)
xB = xA + z1 * np.cos(phi1)
yB = yA + z1 * np.sin(phi1)

#Coordinate del nodo C (estremo tra biella z2 e bilanciere z3)
xC = xB + z2 * np.cos(phi2)
yC = yB + z2 * np.sin(phi2)

#CREAZIONE DEL GRAFICO ILLUSTRATIVO DEL MECCANISMO 
plt.figure(figsize=(8, 8))

#Disegno del telaio z4 (collegamento fisso tra A e D) con linea tratteggiata
plt.plot([xA, xD], [yA, yD], color='gray', linestyle='--', linewidth=3, label='Telaio ($z_4$)')

#Disegno della manovella z1 (da A a B)
plt.plot([xA, xB], [yA, yB], color='blue', linewidth=4, marker='o', markersize=8, label='Manovella ($z_1$)')

#Disegno della biella z2 (da B a C)
plt.plot([xB, xC], [yB, yC], color='green', linewidth=4, marker='o', markersize=8, label='Biella ($z_2$)')

#Disegno del bilanciere z3 (da C a D)
plt.plot([xC, xD], [yC, yD], color='orange', linewidth=4, marker='o', markersize=8, label='Bilanciere ($z_3$)')

#Aggiunta delle etichette testuali per identificare i nodi A, B, C, D
plt.text(xA - 0.3, yA - 0.3, 'A', fontsize=14, fontweight='bold', color='black')
plt.text(xB - 0.2, yB + 0.3, 'B', fontsize=14, fontweight='bold', color='black')
plt.text(xC + 0.2, yC + 0.3, 'C', fontsize=14, fontweight='bold', color='black')
plt.text(xD + 0.3, yD - 0.3, 'D', fontsize=14, fontweight='bold', color='black')

#Impostazioni estetiche del grafico
plt.axhline(0, color='lightgray', linestyle=':')
plt.axvline(0, color='lightgray', linestyle=':')
plt.xlabel('Coordinata X [m]', fontsize=12)
plt.ylabel('Coordinata Y [m]', fontsize=12)
plt.title(f'Configurazione del Meccanismo ($\phi_1 = {phi1deg:.1f}°$)', fontsize=14)
plt.grid(True, linestyle=':', alpha=0.6)

#FONDAMENTALE: mantiene le proporzioni geometriche reali 1:1 tra gli assi x e y
plt.axis('equal') 

plt.legend(loc='upper right', fontsize=11)
plt.show()
