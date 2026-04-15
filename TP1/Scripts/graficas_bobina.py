"""
=============================================================
  GRÁFICAS PARA PAPER  –  Bobina EA3
=============================================================
  Parámetros fijos del diseño:
    dc = 0.20 cm  |  Do = 1.90 cm  |  fo = 15 MHz
  Rango de frecuencias: 10 – 20 MHz
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ─────────────────────────────────────────────
#  CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────

# Parámetros del diseño elegido
DC_ELEGIDO = 0.20       # cm
DO         = 1.90       # cm
FO_DISENO  = 15.0       # MHz

# Arrays (idénticos al script original)
dc_array  = np.round(np.arange(0.08, 0.24, 0.01), 4)   # 16 valores
rel_array = np.round(np.arange(0.5,  2.05, 0.1),  4)   # 16 relaciones l/D

# Carpeta de salida
OUT = Path("graficas_paper")
OUT.mkdir(exist_ok=True)

# Estilo académico global
plt.rcParams.update({
    "figure.dpi"       : 150,
    "savefig.dpi"      : 300,
    "font.family"      : "serif",
    "font.size"        : 11,
    "axes.titlesize"   : 13,
    "axes.labelsize"   : 12,
    "legend.fontsize"  : 9,
    "axes.grid"        : True,
    "grid.alpha"       : 0.35,
    "grid.linestyle"   : "--",
    "axes.spines.top"  : False,
    "axes.spines.right": False,
    "lines.linewidth"  : 1.5,
})

CMAP    = plt.cm.tab20
N_DC    = len(dc_array)

def color_dc(i):
    return CMAP(i / N_DC)

def guardar(fig, nombre):
    ruta = OUT / nombre
    fig.savefig(ruta, bbox_inches="tight", facecolor="white")
    print(f"  ✔  Guardada: {ruta}")
    plt.close(fig)

# ─────────────────────────────────────────────
#  RECONSTRUCCIÓN DE DATOS (Tabla 4)
# ─────────────────────────────────────────────

datos = {dc: {"rel": [], "l": [], "N": [], "K": [], "k": [], "L": []} for dc in dc_array}

for dc in dc_array:
    D  = DO + dc
    Ns = 1.0 / (2.0 * dc)
    for rel in rel_array:
        l     = rel * D
        N     = Ns * l
        ratio = D / (2.0 * l)
        K     = 1.0 / (1.0 + 0.9 * ratio - 2e-2 * ratio**2)
        k     = K * (np.pi**2) * rel
        L_uH  = (D**3) * (Ns**2) * k * 1e-3
        datos[dc]["rel"].append(rel)
        datos[dc]["l"  ].append(l)
        datos[dc]["N"  ].append(N)
        datos[dc]["K"  ].append(K)
        datos[dc]["k"  ].append(k)
        datos[dc]["L"  ].append(L_uH)

# ─────────────────────────────────────────────
#  GRÁFICA 1 – N vs l/D
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

for i, dc in enumerate(dc_array):
    lw    = 2.5 if abs(dc - DC_ELEGIDO) < 1e-9 else 1.0
    alpha = 1.0 if abs(dc - DC_ELEGIDO) < 1e-9 else 0.45
    zord  = 5   if abs(dc - DC_ELEGIDO) < 1e-9 else 2
    lbl   = f"dc={dc:.2f}*" if abs(dc - DC_ELEGIDO) < 1e-9 else f"dc={dc:.2f}"
    ax.plot(datos[dc]["rel"], datos[dc]["N"],
            color=color_dc(i), lw=lw, alpha=alpha, zorder=zord, label=lbl)

# Líneas de referencia
ax.axhline(10, color="red",    lw=0.8, ls=":", alpha=0.7, label="N=10 (mín recom.)")
ax.axhline(15, color="orange", lw=0.8, ls=":", alpha=0.7, label="N=15")
ax.axhline(20, color="green",  lw=0.8, ls=":", alpha=0.7, label="N=20")
ax.axvline(1.0, color="gray",  lw=0.8, ls="--", alpha=0.6, label="l/D=1 (cuadrada)")

ax.set_xlabel("Relación de forma  l/D")
ax.set_ylabel("N  (número de vueltas)")
ax.set_title(f"Número de vueltas N en función de l/D\n(Do = {DO} cm, todas las secciones dc)")
ax.legend(loc="upper left", ncol=2, fontsize=7.5, framealpha=0.85)
ax.set_xlim(rel_array[0], rel_array[-1])
ax.set_ylim(0)
fig.tight_layout()
guardar(fig, "01_N_vs_lD.png")

# ─────────────────────────────────────────────
#  GRÁFICA 2 – L vs l/D
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

for i, dc in enumerate(dc_array):
    lw    = 2.5 if abs(dc - DC_ELEGIDO) < 1e-9 else 1.0
    alpha = 1.0 if abs(dc - DC_ELEGIDO) < 1e-9 else 0.45
    zord  = 5   if abs(dc - DC_ELEGIDO) < 1e-9 else 2
    lbl   = f"dc={dc:.2f}*" if abs(dc - DC_ELEGIDO) < 1e-9 else f"dc={dc:.2f}"
    ax.plot(datos[dc]["rel"], datos[dc]["L"],
            color=color_dc(i), lw=lw, alpha=alpha, zorder=zord, label=lbl)

ax.axvline(1.0, color="gray", lw=0.8, ls="--", alpha=0.6, label="l/D=1 (cuadrada)")
ax.set_xlabel("Relación de forma  l/D")
ax.set_ylabel("L  (µH)")
ax.set_title(f"Inductancia L en función de l/D\n(Do = {DO} cm, todas las secciones dc)")
ax.legend(loc="upper left", ncol=2, fontsize=7.5, framealpha=0.85)
ax.set_xlim(rel_array[0], rel_array[-1])
ax.set_ylim(0)
fig.tight_layout()
guardar(fig, "02_L_vs_lD.png")

# ─────────────────────────────────────────────
#  GRÁFICA 3 – K vs l/D
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

# K solo depende de ratio = D/(2l) = 1/(2·rel)  →  igual para todos los dc con mismo Do
# Pero Do es fijo, así que K varía levemente con dc (por D = Do+dc). Graficamos todas.
for i, dc in enumerate(dc_array):
    lw    = 2.5 if abs(dc - DC_ELEGIDO) < 1e-9 else 1.0
    alpha = 1.0 if abs(dc - DC_ELEGIDO) < 1e-9 else 0.40
    zord  = 5   if abs(dc - DC_ELEGIDO) < 1e-9 else 2
    lbl   = f"dc={dc:.2f}*" if abs(dc - DC_ELEGIDO) < 1e-9 else f"dc={dc:.2f}"
    ax.plot(datos[dc]["rel"], datos[dc]["K"],
            color=color_dc(i), lw=lw, alpha=alpha, zorder=zord, label=lbl)

ax.axvline(1.0, color="gray", lw=0.8, ls="--", alpha=0.6, label="l/D=1 (cuadrada)")
ax.axhline(1.0, color="navy", lw=0.8, ls=":",  alpha=0.5, label="K→1 (solenoide ideal)")
ax.set_xlabel("Relación de forma  l/D")
ax.set_ylabel("K  (factor de Nagaoka)")
ax.set_title(f"Factor de corrección K (Nagaoka) vs l/D\n(Do = {DO} cm)")
ax.legend(loc="lower right", ncol=2, fontsize=7.5, framealpha=0.85)
ax.set_xlim(rel_array[0], rel_array[-1])
fig.tight_layout()
guardar(fig, "03_K_vs_lD.png")

# ─────────────────────────────────────────────
#  GRÁFICA 4 – L vs N
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 5))

for i, dc in enumerate(dc_array):
    lw    = 2.5 if abs(dc - DC_ELEGIDO) < 1e-9 else 1.0
    alpha = 1.0 if abs(dc - DC_ELEGIDO) < 1e-9 else 0.45
    zord  = 5   if abs(dc - DC_ELEGIDO) < 1e-9 else 2
    lbl   = f"dc={dc:.2f}*" if abs(dc - DC_ELEGIDO) < 1e-9 else f"dc={dc:.2f}"
    ax.plot(datos[dc]["N"], datos[dc]["L"],
            color=color_dc(i), lw=lw, alpha=alpha, zorder=zord, label=lbl)

ax.set_xlabel("N  (número de vueltas)")
ax.set_ylabel("L  (µH)")
ax.set_title(f"Inductancia L en función del número de vueltas N\n(Do = {DO} cm)")
ax.legend(loc="upper left", ncol=2, fontsize=7.5, framealpha=0.85)
ax.set_xlim(0)
ax.set_ylim(0)
fig.tight_layout()
guardar(fig, "04_L_vs_N.png")

# ─────────────────────────────────────────────
#  DATOS DEL DISEÑO ELEGIDO  (dc=0.20, Do=1.90)
#  para las gráficas de Qd y Rp
# ─────────────────────────────────────────────

dc_e  = DC_ELEGIDO
D_e   = DO + dc_e               # cm
Ns_e  = 1.0 / (2.0 * dc_e)     # v/cm

# Usar l/D = 1.0 (bobina cuadrada, caso representativo)
rel_e = 1.0
l_e   = rel_e * D_e
ratio_e = D_e / (2.0 * l_e)
K_e   = 1.0 / (1.0 + 0.9 * ratio_e - 2e-2 * ratio_e**2)
k_e   = K_e * (np.pi**2) * rel_e
L_e   = (D_e**3) * (Ns_e**2) * k_e * 1e-3   # µH
L_e_H = L_e * 1e-6

# Rango de frecuencia 10–20 MHz
f_MHz = np.linspace(10, 20, 500)
f_Hz  = f_MHz * 1e6

# ─────────────────────────────────────────────
#  GRÁFICA 5 – Qd vs f0
# ─────────────────────────────────────────────

Qd = 8850 * (D_e * l_e / (102 * l_e + 45 * D_e)) * np.sqrt(f_MHz)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(f_MHz, Qd, color="steelblue", lw=2.5, label=f"dc={dc_e:.2f} cm, l/D={rel_e:.1f}")
ax.axvline(FO_DISENO, color="crimson", lw=1.5, ls="--",
           label=f"fo diseño = {FO_DISENO} MHz  (Qd≈{np.interp(FO_DISENO, f_MHz, Qd):.1f})")
ax.scatter([FO_DISENO], [np.interp(FO_DISENO, f_MHz, Qd)],
           color="crimson", zorder=5, s=60)

ax.set_xlabel("Frecuencia  f₀  (MHz)")
ax.set_ylabel("Factor de calidad  Qd")
ax.set_title(f"Factor de calidad Qd vs frecuencia\n(D={D_e:.2f} cm, l={l_e:.2f} cm)")
ax.legend(framealpha=0.85)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
fig.tight_layout()
guardar(fig, "05_Qd_vs_f0.png")

# ─────────────────────────────────────────────
#  GRÁFICA 6 – Rp vs f0
# ─────────────────────────────────────────────

XL = 2 * np.pi * f_Hz * L_e_H
Rp = Qd * XL / 1e3   # kΩ

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(f_MHz, Rp, color="darkorange", lw=2.5, label=f"dc={dc_e:.2f} cm, l/D={rel_e:.1f}")
ax.axvline(FO_DISENO, color="crimson", lw=1.5, ls="--",
           label=f"fo diseño = {FO_DISENO} MHz  (Rp≈{np.interp(FO_DISENO, f_MHz, Rp):.2f} kΩ)")
ax.scatter([FO_DISENO], [np.interp(FO_DISENO, f_MHz, Rp)],
           color="crimson", zorder=5, s=60)

ax.set_xlabel("Frecuencia  f₀  (MHz)")
ax.set_ylabel("Resistencia paralela  Rp  (kΩ)")
ax.set_title(f"Resistencia paralela Rp vs frecuencia\n(D={D_e:.2f} cm, l={l_e:.2f} cm,  L={L_e:.4f} µH)")
ax.legend(framealpha=0.85)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
fig.tight_layout()
guardar(fig, "06_Rp_vs_f0.png")

# ─────────────────────────────────────────────
#  GRÁFICA 7 – N vs l/D  (solo dc elegido, estilo paper limpio)
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(datos[DC_ELEGIDO]["rel"], datos[DC_ELEGIDO]["N"],
        color="steelblue", lw=2.5, marker="o", ms=4, label=f"dc={DC_ELEGIDO:.2f} cm")
ax.axhline(10, color="red",    lw=0.9, ls=":", alpha=0.8, label="N = 10")
ax.axhline(15, color="orange", lw=0.9, ls=":", alpha=0.8, label="N = 15")
ax.axhline(20, color="green",  lw=0.9, ls=":", alpha=0.8, label="N = 20")
ax.axvline(1.0, color="gray",  lw=0.9, ls="--", alpha=0.7, label="l/D = 1 (cuadrada)")
ax.set_xlabel("Relación de forma  l/D")
ax.set_ylabel("N  (número de vueltas)")
ax.set_title(f"N vs l/D  —  dc = {DC_ELEGIDO} cm,  Do = {DO} cm")
ax.legend(framealpha=0.9)
ax.set_xlim(rel_array[0], rel_array[-1])
ax.set_ylim(0)
fig.tight_layout()
guardar(fig, "07_N_vs_lD_elegido.png")

# ─────────────────────────────────────────────
#  GRÁFICA 8 – L vs l/D  (solo dc elegido, estilo paper limpio)
# ─────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(datos[DC_ELEGIDO]["rel"], datos[DC_ELEGIDO]["L"],
        color="darkorange", lw=2.5, marker="o", ms=4, label=f"dc={DC_ELEGIDO:.2f} cm")
ax.axvline(1.0, color="gray", lw=0.9, ls="--", alpha=0.7, label="l/D = 1 (cuadrada)")
ax.set_xlabel("Relación de forma  l/D")
ax.set_ylabel("L  (µH)")
ax.set_title(f"Inductancia L vs l/D  —  dc = {DC_ELEGIDO} cm,  Do = {DO} cm")
ax.legend(framealpha=0.9)
ax.set_xlim(rel_array[0], rel_array[-1])
ax.set_ylim(0)
fig.tight_layout()
guardar(fig, "08_L_vs_lD_elegido.png")

# ─────────────────────────────────────────────
#  RESUMEN EN CONSOLA
# ─────────────────────────────────────────────

print(f"""
══════════════════════════════════════════════════════
  PARÁMETROS DEL DISEÑO ELEGIDO
══════════════════════════════════════════════════════
  dc   = {dc_e:.2f} cm   |  Do  = {DO:.2f} cm
  D    = {D_e:.2f} cm   |  Ns  = {Ns_e:.2f} v/cm
  l/D  = {rel_e:.1f}       |  l   = {l_e:.2f} cm
  N    = {datos[DC_ELEGIDO]['N'][list(rel_array).index(rel_e)]:.2f} vueltas
  K    = {datos[DC_ELEGIDO]['K'][list(rel_array).index(rel_e)]:.4f}
  L    = {L_e:.4f} µH

  @ fo = {FO_DISENO} MHz:
  Qd   = {np.interp(FO_DISENO, f_MHz, Qd):.2f}
  Rp   = {np.interp(FO_DISENO, f_MHz, Rp):.4f} kΩ

  8 gráficas guardadas en: graficas_paper/
══════════════════════════════════════════════════════
""")
