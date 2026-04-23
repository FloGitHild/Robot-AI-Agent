import numpy as np

# =============================================================================
# 1. GEgebene Werte
# =============================================================================

# Prismenwinkel
gamma = 29.9917  # Grad

# Messunsicherheiten (geschätzt aus Noniusablesung)
u_gamma_grad = 1 / 60    # 1 Bogenminute in Grad
u_delta_grad = 1 / 60    # 1 Bogenminute in Grad

# Umrechnung in Bogenmaß (Radiant)
u_gamma_rad = np.deg2rad(u_gamma_grad)
u_delta_rad = np.deg2rad(u_delta_grad)

print("=" * 70)
print("AUFGABE 4.5: Fehlerfortpflanzung für n")
print("=" * 70)


# =============================================================================
# 2. Messdaten
# =============================================================================

# Wellenlängen und Brechungsindices aus Aufgabe 4.2
lambda_nm = np.array([706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79])
farben = ['Dunkelrot', 'Rot', 'Gelb', 'Grün', 'Blaugrün', 'Blau', 'Violett']
n = np.array([2.4018, 2.4066, 2.4211, 2.4455, 2.4492, 2.4580, 2.4708])
delta_min = np.array([46.8542, 47.0375, 47.5875, 48.5167, 48.6583, 48.9958, 49.4917])

# =============================================================================
# 3. Fehlerfortpflanzung berechnen
# =============================================================================

# Umrechnung in Bogenmaß
gamma_rad = np.deg2rad(gamma)
delta_rad = np.deg2rad(delta_min)

# Formel (4): u(n)/n = √[ cot²((δ+γ)/2)·u²(δ) + cot²(γ/2)·u²(γ) ]
# Berechnung von cot(x) = cos(x)/sin(x)

# cot(γ/2) - konstant für alle Messungen
cot_gamma_2 = np.cos(gamma_rad / 2) / np.sin(gamma_rad / 2)

# cot((δ+γ)/2) - für jede Messung unterschiedlich
cot_delta_gamma_2 = np.cos((delta_rad + gamma_rad) / 2) / np.sin((delta_rad + gamma_rad) / 2)

# Relative Unsicherheit
rel_error = np.sqrt(
    cot_delta_gamma_2**2 * u_delta_rad**2 + 
    cot_gamma_2**2 * u_gamma_rad**2
)

# Absolute Unsicherheit
u_n = n * rel_error

print(f"""
--- Berechnung der cot-Werte ---
cot(γ/2) = cot({gamma/2:.2f}°) = {cot_gamma_2:.4f}

--- Tabelle: Brechungsindices mit Unsicherheiten ---
{farben[0]:<12} {lambda_nm[0]:>8.2f} {delta_min[0]:>10.4f} {n[0]:>12.6f} {u_n[0]:>12.6f} {rel_error[0]*100:>8.4f}%
{farben[1]:<12} {lambda_nm[1]:>8.2f} {delta_min[1]:>10.4f} {n[1]:>12.6f} {u_n[1]:>12.6f} {rel_error[1]*100:>8.4f}%
{farben[2]:<12} {lambda_nm[2]:>8.2f} {delta_min[2]:>10.4f} {n[2]:>12.6f} {u_n[2]:>12.6f} {rel_error[2]*100:>8.4f}%
{farben[3]:<12} {lambda_nm[3]:>8.2f} {delta_min[3]:>10.4f} {n[3]:>12.6f} {u_n[3]:>12.6f} {rel_error[3]*100:>8.4f}%
{farben[4]:<12} {lambda_nm[4]:>8.2f} {delta_min[4]:>10.4f} {n[4]:>12.6f} {u_n[4]:>12.6f} {rel_error[4]*100:>8.4f}%
{farben[5]:<12} {lambda_nm[5]:>8.2f} {delta_min[5]:>10.4f} {n[5]:>12.6f} {u_n[5]:>12.6f} {rel_error[5]*100:>8.4f}%
{farben[6]:<12} {lambda_nm[6]:>8.2f} {delta_min[6]:>10.4f} {n[6]:>12.6f} {u_n[6]:>12.6f} {rel_error[6]*100:>8.4f}%
""")

# =============================================================================
# 4. Beispielrechnung für eine Farbe (Dunkelrot)
# =============================================================================

print("=" * 70)
print("BEISPIELRECHNUNG: Dunkelrot (706,54 nm)")
print("=" * 70)

i = 0  # Dunkelrot
print(f"""

Farbe       | λ (nm)  | n         | u(n)       | u(n)/n (%)
-------------------------------------------------------------""")

for i in range(len(farben)):
    print(f"{farben[i]:<10} | {lambda_nm[i]:>7.2f} | {n[i]:>9.6f} | {u_n[i]:>10.6f} | {rel_error[i]*100:>8.4f}%")

print(f"""
-------------------------------------------------------------

Die relative Unsicherheit beträgt ca. {np.mean(rel_error)*100:.4f}%
Die absolute Unsicherheit beträgt ca. {np.mean(u_n):.4f}
""")