import math
import matplotlib.pyplot as graph
import pandas


#0:dati del problema

Re = float(input("Reynolds Number (Re)     = "))
k  = float(input("Pipe Roughness (k) [m]  = "))
D  = float(input("Pipe Diameter (D) [m]   = "))

#1:calcolo la scabrezza relativa

epsilon = k / D
print(f"Relative roughness (ε) = {epsilon}")

#2:preparo i dati per il ciclo while di colebrook

f_old = 0.079 * Re**(-0.25)     #
st_f = []
st_iter = []
iter = 0
err = 1

#3:imposto il ciclo if che separa regime laminare da turbolento

if Re <= 2100 :
    print("Laminar Flow. The program will calculate Fanning's friction factor:")
    f = 16 / Re       #fattore di attrito per regime laminare
    print(f"Friction Factor (f) = {f}")
elif Re >= 4000 :
    print("Turbolent Flow. The program will calculate the friction factor via Colebrook equation: ")
    while err >= 0.01 : 
        iter = iter + 1     #aumento l'terazione
        RHS = -2 * math.log10(epsilon / 3.7 + 2.51 / (Re * math.sqrt(f_old)))       #calcolo la right-hand side
        f_new = (1 / RHS) ** 2      #calcolo il fattore di attrito girando colebrook
        err = (abs(f_new - f_old)) / f_old      #calcolo la differena tra fattore di attr nuovo e vecchio
        st_f.append(f_new)
        st_iter.append(iter)
        f_old = f_new       #cambio il fattore di attrito di partenza della nuova iterazione
    print(f"Friction Factor (f) = {f_new}")
    #TABELLA   
    tab = {
    "Iteration" : st_iter , 
    "Friction Factor (f)" : st_f
    }
    dfp = pandas.DataFrame(tab)
    dfp["Deviation %"] = dfp["Friction Factor (f)"].pct_change() * 100
    print("Iterations Recap:")
    print(dfp)
    #GRAFICO
    graph.figure(figsize = ( 8 , 5))
    graph.plot(st_iter , st_f , marker = "s" , linestyle = ":" , color = "red" , linewidth = 2 , label = "Calculated value")
    graph.legend()

    graph.title("Friction Factor (f) Convergence")
    graph.xlabel("Iterations")
    graph.ylabel("Friction Factor (f)")
    graph.grid(True , linestyle="--" , alpha = 0.7)
    #limiti comparativi per il grafico (scabro turbolento; liscio turbolento)
    f_bls = 0.079 * Re**(-0.25)     #tubo completamente liscio (equazione di blasius)
    graph.axhline(y = f_bls , color = "b" , linestyle = "--", label = "Friction Factor for a smooth pipe (Blasius Formula)")
    f_vkrm = (1 / (-2 * math.log10(epsilon / 3.7))) ** 2        #velocità talmente alta che comanda solamente la rugosità (formula di von karman)
    graph.axhline(y = f_vkrm , color = "g" , linestyle = "--", label = "Roughness Turbolence (Von Karman Formula)")

    graph.legend()

    graph.yscale("log")

    graph.show()

