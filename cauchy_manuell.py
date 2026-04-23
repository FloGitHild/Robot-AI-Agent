import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ================================
# 1. MESSWERTE EINTRAGEN
# ================================

# Wellenlängen in nm
lambda_nm = np.array([706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79])

# Berechnete Brechungsindices (aus Aufgabe 4.2)
n = np.array([2.393306803, 2.39771782, 2.412238138, 2.436533183, 2.440240066, 2.448512544, 2.461319579])

# ================================
# 2. CAUCHY-FUNKTION
# ================================

def cauchy(lambda_nm, A, B):
    return A * (1 + B / (lambda_nm**2))


# ================================
# 3. FIT DURCHFÜHREN
# ================================

# Startwerte
p0 = [1.5, 5000]

popt, pcov = curve_fit(cauchy, lambda_nm, n, p0=p0)

A, B = popt

# ================================
# 4. UNSICHERHEITEN
# ================================

# Standardabweichungen
errors = np.sqrt(np.diag(pcov))
dA, dB = errors

# Freiheitsgrade
N = len(lambda_nm)
f = N - 2

# t-Wert (ca. für 95% Konfidenzintervall)
t = 2.3  

# 95%-Unsicherheiten
A_err_95 = t * dA
B_err_95 = t * dB

# ================================
# 5. ERGEBNISSE AUSGEBEN
# ================================

print("Fit-Ergebnisse:")
print(f"A = {A:.6f} ± {A_err_95:.6f}")
print(f"B = {B:.2f} ± {B_err_95:.2f}")

# ================================
# 6. PLOT
# ================================

x_plot = np.linspace(min(lambda_nm), max(lambda_nm), 1000)

plt.figure()
plt.scatter(lambda_nm, n, label="Messwerte")
plt.plot(x_plot, cauchy(x_plot, A, B), label="Cauchy-Fit")

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Brechungsindex n")
plt.title("Dispersionskurve n(λ)")
plt.legend()
plt.grid()

plt.show()