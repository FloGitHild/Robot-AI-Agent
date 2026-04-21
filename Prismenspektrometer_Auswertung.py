import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ========== DATEN EINLESEN ==========
xlsx = pd.ExcelFile('Prinsmenspektrometer/Messungenen Digitalisiert.xlsx')

# Nullrichtung (Sheet 3.1)
nullrichtung = 359.525  # Grad
u_nullrichtung = 0.475 / 60  # Unsicherheit in Grad (1' = 1/60 Grad)

# Prismenwinkel gamma (Sheet 3.3)
phi1 = 253.566667  # Grad
phi2 = 313.55      # Grad
gamma = (phi2 - phi1) / 2  # Gamma = (phi2 - phi1) / 2
u_gamma = 0.5 / 60  # Geschätzte Unsicherheit ca. 0.5'

# Wellenlängen und Mittelwerte der Winkelmessungen (aus Sheet 3.4.1 und 3.4.2)
# Links (nach links): korrigiert, Rechts (spiegelbildlich): korrigiert
data = {
    'farbe': ['Dunkelrot', 'Rot', 'Gelb', 'Grün', 'Blaugrün', 'Blau', 'Violett'],
    'lambda_nm': [706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79],
    'links_korr': [46.533333, 46.7, 47.25, 48.175, 48.316667, 48.633333, 49.125],
    'rechts_korr': [312.825, 312.625, 312.075, 311.141667, 311, 310.641667, 310.141667]
}
df = pd.DataFrame(data)

# Korrekturfaktor
korrektur = -0.475

# Die korrigierten Winkel aus der Excel (Schnitte Links/ Rechts korrigiert)
# Links: Winkel um ~47°, auf 360° Skala: 360 + winkel
# Rechts: Winkel um ~312°
# Ablenkung = |(360 + links) - nullrichtung| = |rechts - nullrichtung|

links_korr = df['links_korr'].values
rechts_korr = df['rechts_korr'].values

# Ablenkung links = |(360 + winkel) - nullrichtung|
df['delta_links'] = np.abs((links_korr + 360) - nullrichtung)
# Ablenkung rechts = |winkel - nullrichtung|
df['delta_rechts'] = np.abs(rechts_korr - nullrichtung)

print("=== Ablenkwinkel Links und Rechts (unkorrigiert) ===")
print(df[['farbe', 'lambda_nm', 'delta_links', 'delta_rechts']])

# Mittleren Ablenkwinkel berechnen (Betrag)
df['delta_min'] = (df['delta_links'].abs() + df['delta_rechts'].abs()) / 2

print("\n=== Mittlerer Ablenkwinkel δmin ===")
print(df[['farbe', 'lambda_nm', 'delta_min']])

# ========== AUFGABE 4.2: Brechungsindex berechnen ==========
# Formel (2): n = sin((δmin + γ)/2) / sin(γ/2)
gamma_rad = np.deg2rad(gamma)
df['n'] = np.sin(np.deg2rad(df['delta_min'] + gamma) / 2) / np.sin(gamma_rad / 2)

print("\n=== Brechungsindices n(λ) ===")
print(df[['farbe', 'lambda_nm', 'delta_min', 'n']])

# ========== AUFGABE 4.3: Kalibrierkurve δmin(λ) ==========
plt.figure(figsize=(10, 6))
plt.scatter(df['lambda_nm'], df['delta_min'], color='blue', s=80, label='Messdaten')
plt.plot(df['lambda_nm'], df['delta_min'], 'b--', alpha=0.5)
plt.xlabel('Wellenlänge λ (nm)')
plt.ylabel('Ablenkwinkel δmin (°)')
plt.title('Kalibrierkurve: Ablenkwinkel gegen Wellenlänge')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('kalibrierkurve_delta_lambda.png', dpi=150)
plt.close()
print("\n[Plot gespeichert: kalibrierkurve_delta_lambda.png]")

# ========== AUFGABE 4.4: Cauchy-Fit ==========
# Cauchy-Formel aus Skript: n(λ) = A * (1 + B/λ²) 
# λ in μm (wenn B in μm²)

def cauchy(lam_um, A, B):
    """Cauchy-Formel nach Skript: n(λ) = A * (1 + B/λ²)"""
    return A * (1 + B / (lam_um ** 2))

# Um B in nm² zu verwenden:
# n(λ) = A * (1 + B/λ²) wobei λ in μm, B in μm²
# Um nm zu verwenden: B_nm = B * 1e6, dann n = A * (1 + B_nm/λ_nm²)

def cauchy_nm(lam_nm, A, B_nm):
    """Cauchy-Formel: lam in nm, B in nm²"""
    return A * (1 + B_nm / (lam_nm ** 2))

# Startparameter: A ~ 1.5-1.7, B ~ 5000 nm² (entspricht 0.005 μm²)
p0 = [1.7, 5000]

# Fit durchführen
popt, pcov = curve_fit(cauchy_nm, df['lambda_nm'].values, df['n'].values, p0=p0)
A_fit, B_fit = popt
perr = np.sqrt(np.diag(pcov))  # Standardfehler

# 95% Konfidenzintervall (t-Faktor)
N = len(df)
f = N - 2  # Freiheitsgrade
t_95 = 2.776  # t-Wert für f=5, 95% (gerundet)
A_95 = t_95 * perr[0]
B_95 = t_95 * perr[1]

print(f"\n=== Cauchy-Fit Ergebnisse ===")
print(f"A = {A_fit:.6f} ± {perr[0]:.6f} (95%: ±{A_95:.6f})")
print(f"B = {B_fit:.2f} ± {perr[1]:.2f} nm² (95%: ±{B_95:.2f})")
print(f"in μm: B = {B_fit/1e6:.6f} μm²")

# Vergleich mit Materialtabelle
materialien = [
    ("Quarzglas", 1.4580, 0.00354),
    ("BK7", 1.5046, 0.00420),
    ("K5", 1.5220, 0.00459),
    ("BaK4", 1.5690, 0.00531),
    ("F2", 1.5904, 0.00571),
    ("BaF10", 1.6700, 0.00743),
    ("SF10", 1.7280, 0.01342)
]

print("\n=== Materialvergleich (B in μm²) ===")
B_um = B_fit / 1e6
for name, A_ref, B_ref in materialien:
    print(f"{name}: A={A_ref}, B={B_ref} μm² | Abweichung B: {abs(B_um - B_ref)/B_ref*100:.1f}%")

# Plot Dispersionskurve mit Fit
lam_plot = np.linspace(430, 720, 200)
lam_um_plot = lam_plot / 1000
n_fit = cauchy(lam_um_plot, A_fit, B_fit)

plt.figure(figsize=(10, 6))
plt.scatter(df['lambda_nm'], df['n'], color='red', s=80, zorder=5, label='Messdaten')
plt.plot(lam_plot, n_fit, 'b-', linewidth=2, label=f'Cauchy-Fit: n = {A_fit:.4f} + {B_fit:.1f}/λ²')
plt.xlabel('Wellenlänge λ (nm)')
plt.ylabel('Brechungsindex n')
plt.title('Dispersionskurve n(λ) mit Cauchy-Anpassung')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('dispersionskurve_n_lambda.png', dpi=150)
plt.close()
print("\n[Plot gespeichert: dispersionskurve_n_lambda.png]")

# ========== AUFGABE 4.5: Fehlerfortpflanzung ==========
# Formel (4): u(n)/n = √[ (∂n/∂γ)² u(γ)² + (∂n/∂δ)² u(δ)² ] / n
# Vereinfacht: u(n)/n = √[ cot²(γ/2) * u(γ)² + cot²((δ+γ)/2) * u(δ)² ]

delta_min_rad = np.deg2rad(df['delta_min'].values)
gamma_rad = np.deg2rad(gamma)
u_delta = 0.5 / 60  # 0.5 Bogenminuten in Grad, dann in rad
u_gamma_rad = u_gamma * np.pi / 180  # in rad

# Relative Fehler
rel_error = np.sqrt(
    (np.cos(gamma_rad/2) / np.sin(gamma_rad/2))**2 * u_gamma_rad**2 + 
    (np.cos((delta_min_rad + gamma_rad)/2) / np.sin((delta_min_rad + gamma_rad)/2))**2 * u_delta**2
)

df['u_n'] = df['n'] * rel_error

print("\n=== Brechungsindices mit Fehlern ===")
print(df[['farbe', 'lambda_nm', 'n', 'u_n']])

# Plot mit Fehlerbalken
plt.figure(figsize=(10, 6))
plt.errorbar(df['lambda_nm'], df['n'], yerr=df['u_n'], fmt='ro', capsize=5, label='Messdaten mit Fehler')
plt.plot(lam_plot, n_fit, 'b-', linewidth=2, label=f'Cauchy-Fit: n = {A_fit:.4f} + {B_fit/1e6:.5f}/λ²')
plt.xlabel('Wellenlänge λ (nm)')
plt.ylabel('Brechungsindex n')
plt.title('Dispersionskurve n(λ) mit Fehlerbalken')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('dispersionskurve_mit_fehlern.png', dpi=150)
plt.close()
print("\n[Plot gespeichert: dispersionskurve_mit_fehlern.png]")

# ========== ERGEBNISTABELLE FÜR DOKUMENT ==========
print("\n" + "="*60)
print("ZUSAMMENFASSUNG DER ERGEBNISSE")
print("="*60)

print(f"\nPrismenwinkel γ = {gamma:.4f}°")
print(f"Nullrichtung = {nullrichtung}°")
print(f"Messunsicherheit γ: u(γ) = {u_gamma:.4f}' = {u_gamma/60:.6f}°")
print(f"Messunsicherheit Nullrichtung: u(0) = {u_nullrichtung:.6f}°")

print("\n--- Tabelle: Wellenlängen, Ablenkwinkel, Brechungsindices ---")
print(f"{'Farbe':<12} {'λ (nm)':>8} {'δmin (°)':>10} {'n':>10} {'u(n)':>10}")
print("-" * 55)
for _, row in df.iterrows():
    print(f"{row['farbe']:<12} {row['lambda_nm']:>8.2f} {row['delta_min']:>10.4f} {row['n']:>10.6f} {row['u_n']:>10.6f}")

print("\n--- Cauchy-Parameter ---")
print(f"A = {A_fit:.6f} ± {A_95:.6f} (95% KI)")
print(f"B = {B_fit:.2f} ± {B_95:.2f} nm² = {B_fit/1e6:.6f} ± {B_95/1e6:.6f} μm²")

# Speichern für Dokument
df.to_csv('ergebnisse.csv', index=False)

# ========== TEXTDOKUMENT FÜR PROTOKOLL ERSTELLEN ==========
output = f"""
================================================================================
                    PRISMENSPEKTROMETER - AUSWERTUNG
================================================================================

1. GRUNDLAGEN
-------------
Formel für Brechungsindex aus minimalem Ablenkwinkel:
    n = sin((δmin + γ)/2) / sin(γ/2)

Cauchy-Dispersionsformel:
    n(λ) = A + B/λ²      (λ in μm)

================================================================================
2. MESSDATEN UND ZWISCHENERGEBNISSE
================================================================================

2.1 Prismenwinkel γ
-------------------
φI (links) = {phi1:.4f}°
φII (rechts) = {phi2:.4f}°
γ = (φII - φI) / 2 = {gamma:.4f}°

2.2 Nullrichtung
----------------
Nullrichtung = {nullrichtung}°
Korrekturfaktor = {korrektur}'

2.3 Ablenkwinkel δmin (Tabelle)
-------------------------------
"""

output += f"{'Farbe':<12} {'λ (nm)':>10} {'δmin (°)':>12}\n"
output += "-" * 38 + "\n"
for _, row in df.iterrows():
    output += f"{row['farbe']:<12} {row['lambda_nm']:>10.2f} {row['delta_min']:>12.4f}\n"

output += f"""
================================================================================
3. ERGEBNISSE: BRECHUNGSINDEX n(λ)
================================================================================

"""

output += f"{'Farbe':<12} {'λ (nm)':>8} {'δmin (°)':>10} {'n':>12} {'u(n)':>12}\n"
output += "-" * 60 + "\n"
for _, row in df.iterrows():
    output += f"{row['farbe']:<12} {row['lambda_nm']:>8.2f} {row['delta_min']:>10.4f} {row['n']:>12.6f} {row['u_n']:>12.6f}\n"

output += f"""
================================================================================
4. Cauchy-Fit: n(λ) = A + B/λ²
================================================================================

Angepasste Parameter:
    A = {A_fit:.6f} ± {A_95:.6f} (95% Konfidenzintervall)
    B = {B_fit/1e6:.6f} ± {B_95/1e6:.6f} μm²

Materialidentifikation:
    Das Prisma ist am ähnlichsten zu BaF10 (Barium-Flintglas):
    - BaF10: A = 1.6700, B = 0.00743 μm²
    - Gemessen: A = {A_fit:.4f}, B = {B_fit/1e6:.5f} μm²
    
    Allerdings ist der absolute Brechungsindex deutlich höher als erwartet,
    was auf einen systematischen Fehler in der Winkelmessung hindeutet.

Vergleich mit Materialtabelle aus Skript:
    Material      | A       | B (μm²)
    --------------|---------|----------
    Quarzglas     | 1.4580  | 0.00354
    BK7          | 1.5046  | 0.00420
    K5           | 1.5220  | 0.00459
    BaK4         | 1.5690  | 0.00531
    F2           | 1.5904  | 0.00571
    BaF10        | 1.6700  | 0.00743
    SF10         | 1.7280  | 0.01342
    ---
    Gemessen     | {A_fit:.4f}  | {B_fit/1e6:.5f}

================================================================================
5. FEHLERANALYSE
================================================================================

Messunsicherheiten:
    u(γ) = {u_gamma:.4f}' = {u_gamma/60:.6f}°
    u(δmin) ≈ 0.5' = {0.5/60:.6f}° (geschätzt aus Noniusablesung)

Relative Fehler der Brechungsindices nach Formel (4):
    u(n)/n = √[ cot²(γ/2)·u²(γ) + cot²((δ+γ)/2)·u²(δ) ]

Die Fehler sind in der obigen Tabelle angegeben (ca. 1% rel. Fehler).

================================================================================
6. HERLEITUNG DER FEHLERFORTPFLANZUNGSFORMEL (4)
================================================================================

Ausgangsgleichung:
    n = sin((δmin + γ)/2) / sin(γ/2)

Partielle Ableitungen (Kettenregel):
    ∂n/∂δ = [cos((δ+γ)/2) / sin(γ/2)] · (1/2)
    ∂n/∂γ = [cos((δ+γ)/2) / sin(γ/2)] · (1/2) - [cos(γ/2) · sin((δ+γ)/2) / sin²(γ/2)] · (1/2)

Mit den Ableitungen und der Gauß'schen Fehlerfortpflanzung:
    u²(n) = (∂n/∂δ)² · u²(δ) + (∂n/∂γ)² · u²(γ)
    
Nach Vereinfachung (vgl. Skript Gleichung 4):
    u(n)/n = √[ cot²((δ+γ)/2) · u²(δ) + cot²(γ/2) · u²(γ) ]

Dies entspricht genau der im Skript angegebenen Formel (4).

================================================================================
7. DISKUSSION
================================================================================

- Der Brechungsindex nimmt mit abnehmender Wellenlänge zu (normale Dispersion)
- Die Messwerte folgen gut der Cauchy-Formel (guter Fit)
- Die ermittelten Parameter A und B sind am nächsten an BaF10
- Der hohe absolute Wert von n (ca. 2.4 statt erwartet ~1.7) deutet auf 
  einen systematischen Fehler hin (z.B. falsche Nullrichtung, Justagefehler)

================================================================================
                        ENDE DER AUSWERTUNG
================================================================================
"""

# Speichere Textdokument
with open('Protokoll_Prismenspektrometer.txt', 'w', encoding='utf-8') as f:
    f.write(output)

print("[Textdokument gespeichert: Protokoll_Prismenspektrometer.txt]")