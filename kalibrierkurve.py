import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. MESSDATEN
# =============================================================================

# Wellenlängen der He-Linien in nm
lambda_nm = np.array([706.54, 667.82, 587.56, 501.57, 492.19, 447.15, 438.79])

# Gemessene Ablenkwinkel (bereits gemittelt aus Links/Rechts)
delta_min = np.array([46.8542, 47.0375, 47.5875, 48.5167, 48.6583, 48.9958, 49.4917])


# =============================================================================
# 3. PLOT DER KALIBRIERKUUVE
# =============================================================================

plt.figure(figsize=(10, 6))

# Messpunkte
plt.scatter(lambda_nm, delta_min, color='blue', s=100, zorder=5, label='Messdaten')

# Verbindunglinie
plt.plot(lambda_nm, delta_min, 'b--', alpha=0.5)

# Achsenbeschriftung
plt.xlabel('Wellenlänge λ (nm)', fontsize=12)
plt.ylabel('Ablenkwinkel δmin (°)', fontsize=12)
plt.title('Kalibrierkurve: Ablenkwinkel gegen Wellenlänge', fontsize=14)

# Raster (0.5° Beschriftung, 10° Gitterlinien)
plt.grid(True, alpha=0.3, which='major')
plt.yticks(np.arange(46.5, 50.5, 0.5))
ax = plt.gca()
ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
ax.grid(True, which='minor', alpha=0.15)

# Legende
plt.legend()

# Tight layout
plt.tight_layout()

# Speichern
plt.savefig('kalibrierkurve_delta_lambda.png', dpi=300)
print("\nBild gespeichert: kalibrierkurve_delta_lambda.png")
