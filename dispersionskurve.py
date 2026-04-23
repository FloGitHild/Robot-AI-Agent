"""
Dispersionskurve: Brechungsindex n gegen Wellenlänge λ
=======================================================
Mit Cauchy-Fit: n(λ) = A + B/λ²

Der Fit bestimmt automatisch die Parameter A und B aus den Messdaten.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =============================================================================
# 1. MESSDATEN
# =============================================================================

# Wellenlängen der He-Linien in nm
lambda_nm = np.array([706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79])

# Farben
farben = ['Dunkelrot', 'Rot', 'Gelb', 'Grün', 'Blaugrün', 'Blau', 'Violett']

# Brechungsindices (berechnet aus n = sin((δmin+γ)/2) / sin(γ/2))
n = np.array([2.4018, 2.4066, 2.4211, 2.4455, 2.4492, 2.4580, 2.4708])

# =============================================================================
# 2. TABELLE AUSGEBEN
# =============================================================================

print("=" * 60)
print("Tabelle: Wellenlänge und Brechungsindex")
print("=" * 60)
print(f"{'Farbe':<12} {'λ (nm)':>10} {'n':>12}")
print("-" * 60)
for i in range(len(lambda_nm)):
    print(f"{farben[i]:<12} {lambda_nm[i]:>10.2f} {n[i]:>12.6f}")
print("=" * 60)

# =============================================================================
# 3. CAUCHY-FIT DURCHFÜHREN
# =============================================================================

def cauchy(lam_um, A, B):
    """
    Cauchy-Gleichung: n(λ) = A + B/λ²
    Parameter:
        lam_um: Wellenlänge in Mikrometer (μm)
        A: Grundbrechungsindex
        B: Dispersionskoeffizient in μm²
    """
    return A + B / (lam_um**2)

# Umrechnung: nm -> μm (1 μm = 1000 nm)
lambda_um = lambda_nm / 1000

# Fit durchführen
# Startwerte: A ≈ 2.3, B ≈ 0.01 μm² (laut Skript ~5000 nm²)
popt, pcov = curve_fit(cauchy, lambda_um, n, p0=[2.3, 0.01])

A_fit = popt[0]    # A Parameter
B_fit = popt[1]    # B Parameter

perr = np.sqrt(np.diag(pcov))  # Standardfehler von A und B
A_err = perr[0]
B_err = perr[1]

print("\n" + "=" * 60)
print("Cauchy-Fit Ergebnisse: n(λ) = A + B/λ²")
print("=" * 60)
print(f"A = {A_fit:.6f} ± {A_err:.6f}")
print(f"B = {B_fit:.6f} ± {B_err:.6f} μm²")
print(f"B = {B_fit*1e6:.2f} ± {B_err*1e6:.2f} nm²")
print("=" * 60)

# =============================================================================
# 4. GÜTE DES FITS (R²)
# =============================================================================

n_fit = cauchy(lambda_um, A_fit, B_fit)
ss_res = np.sum((n - n_fit)**2)
ss_tot = np.sum((n - np.mean(n))**2)
r_squared = 1 - (ss_res / ss_tot)

print(f"\nGüte des Fits: R² = {r_squared:.6f}")
print("(R² ≈ 1 bedeutet perfekte Anpassung)")

# =============================================================================
# 5. PLOT ERSTELLEN
# =============================================================================

plt.figure(figsize=(10, 6))

# Messpunkte
plt.scatter(lambda_nm, n, color='red', s=100, zorder=5, label='Messdaten')

# Fit-Kurve (glatt)
lambda_plot = np.linspace(430, 720, 200)  # von Violett bis Dunkelrot
lambda_plot_um = lambda_plot / 1000
n_plot = cauchy(lambda_plot_um, A_fit, B_fit)
plt.plot(lambda_plot, n_plot, 'b-', linewidth=2, 
         label=f'Cauchy-Fit: n = {A_fit:.4f} + {B_fit:.5f}/λ²')

# Achsenbeschriftung
plt.xlabel('Wellenlänge λ (nm)', fontsize=12)
plt.ylabel('Brechungsindex n', fontsize=12)
plt.title('Dispersionskurve: Brechungsindex gegen Wellenlänge', fontsize=14)

# Raster
plt.grid(True, alpha=0.3)

# Legende
plt.legend()

# Achsenbereich sinnvoll setzen
plt.xlim(400, 750)
plt.ylim(2.38, 2.50)

plt.tight_layout()
plt.savefig('dispersionskurve_n_lambda.png', dpi=150)
print("\nBild gespeichert: dispersionskurve_n_lambda.png")

# =============================================================================
# 6. ERKLÄRUNG
# =============================================================================

print("\n" + "=" * 60)
print("Physikalische Erklärung:")
print("=" * 60)
print(f"""
Die Dispersionskurve zeigt, wie der Brechungsindex mit der 
Wellenlänge abnimmt (normale Dispersion).

Fit-Ergebnisse:
- A = {A_fit:.4f} → Grundbrechungsindex (bei λ → ∞)
- B = {B_fit:.5f} μm² → Dispersionskoeffizient

Vergleich mit Materialtabelle:
- B ≈ 0.0087 μm² entspricht am ehesten BaF10 (Barium-Flintglas)
- Der hohe A-Wert deutet auf einen systematischen Messfehler hin

Die Cauchy-Gleichung erlaubt die Berechnung von n für beliebige 
Wellenlängen im Messbereich.
""")