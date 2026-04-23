import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import MultipleLocator

# ================================
# 1. MESSWERTE
# ================================

lambda_nm = np.array([706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79])

n = np.array([2.393306803, 2.39771782, 2.412238138,
              2.436533183, 2.440240066, 2.448512544, 2.461319579])

delta_deg = np.array([46.53333333, 46.7, 47.25,
                      48.175, 48.31666667, 48.63333333, 49.125])

gamma_deg = 59.9833

u_delta_deg = 1/60
u_gamma_deg = 1/60

# Startwerte Fit
p0 = [1.5, 5000]

# ================================
# 2. RADIANT
# ================================

deg_to_rad = np.pi / 180

delta = delta_deg * deg_to_rad
gamma = gamma_deg * deg_to_rad

u_delta = u_delta_deg * deg_to_rad
u_gamma = u_gamma_deg * deg_to_rad

# ================================
# 3. FEHLER BERECHNEN
# ================================

term_delta = (1/np.tan((delta + gamma)/2) - 1/np.tan(gamma/2)) * u_delta
term_gamma = (1/np.tan((delta + gamma)/2)) * u_gamma

rel_error = np.sqrt(term_delta**2 + term_gamma**2)
n_error = rel_error * n

# ================================
# 4. CAUCHY-FUNKTION + FIT
# ================================

def cauchy(lambda_nm, A, B):
    return A * (1 + B / (lambda_nm**2))

popt, pcov = curve_fit(cauchy, lambda_nm, n, p0=p0)
A, B = popt

# ================================
# 5. UNSICHERHEITEN FIT
# ================================

errors = np.sqrt(np.diag(pcov))
dA, dB = errors

t = 2.365  # ca. 95% Konfidenz

A_err_95 = t * dA
B_err_95 = t * dB

# ================================
# 6. PLOT
# ================================

plt.figure()
ax = plt.gca()

# Raster
ax.yaxis.set_major_locator(MultipleLocator(0.01))
ax.yaxis.set_minor_locator(MultipleLocator(0.002))

ax.xaxis.set_major_locator(MultipleLocator(50))
ax.xaxis.set_minor_locator(MultipleLocator(10))

ax.grid(which='major', linestyle='-', linewidth=1)
ax.grid(which='minor', linestyle='--', linewidth=0.4)

# Messwerte
plt.errorbar(lambda_nm, n, yerr=n_error,
             fmt='o', capsize=5, markersize=3,
             label="Messwerte")

# Fit
x_plot = np.linspace(min(lambda_nm), max(lambda_nm), 1000)
plt.plot(x_plot, cauchy(x_plot, A, B), label="Cauchy-Fit")

plt.xlabel("Wellenlänge (nm)")
plt.ylabel("Brechungsindex n")
plt.title("Dispersionskurve mit Fit")
plt.legend()

plt.savefig("dispersionskurve.png", dpi=600)
plt.show()

# ================================
# 7. AUSGABE MESSWERTE
# ================================

print("\n--- Messwerte ---")
print("λ (nm)        n            Δn")

for lam, ni, ei in zip(lambda_nm, n, n_error):
    print(f"{lam:8.2f}   {ni:.9f}   ±{ei:.9f}")

# ================================
# 8. FITERGEBNISSE
# ================================

print("\n--- Cauchy-Fit Parameter ---")
print(f"A = {A:.6f} ± {A_err_95:.6f}")
print(f"B = {B:.2f} ± {B_err_95:.2f}")