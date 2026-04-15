"""
=============================================================
  CONSTRUCTOR DE BOBINAS - Calculadora de Parámetros
=============================================================
  Tablas generadas con pandas DataFrames.
  Relación de forma: l/D  (1.0 = cuadrada | 0.5 = alargada)
=============================================================
"""

import os
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box

os.chdir(os.path.dirname(os.path.abspath(__file__)))

console = Console()

pd.set_option("display.float_format",  lambda x: f"{x:.3f}")
pd.set_option("display.max_columns",   50)
pd.set_option("display.width",         200)

# ─────────────────────────────────────────────
#  Utilidades
# ─────────────────────────────────────────────

def titulo(texto, ancho=80):
    console.print("\n" + "═" * ancho)
    console.print(f"  [bold cyan]{texto}[/bold cyan]")
    console.print("═" * ancho)

def subtitulo(texto, ancho=80):
    console.print("\n" + "─" * ancho)
    console.print(f"  [bold yellow]{texto}[/bold yellow]")
    console.print("─" * ancho)

def input_float(prompt, minval=None, maxval=None):
    while True:
        try:
            val = float(input(prompt))
            if minval is not None and val < minval:
                console.print(f"  [red]⚠  Mínimo permitido: {minval}[/red]")
                continue
            if maxval is not None and val > maxval:
                console.print(f"  [red]⚠  Máximo permitido: {maxval}[/red]")
                continue
            return val
        except ValueError:
            console.print("  [red]⚠  Ingrese un número válido.[/red]")

def color_N(val):
    """Color por valor de N."""
    if val < 10:
        return "red"
    elif val < 15:
        return "yellow"
    elif val < 20:
        return "green"
    else:
        return "bright_green"

# Paleta de colores para distinguir columnas l/D
PALETA_COLS = [
    "cyan", "magenta", "bright_yellow", "bright_cyan",
    "bright_magenta", "green", "bright_red", "bright_blue",
    "orange3", "violet", "turquoise2", "chartreuse1",
    "deep_pink3", "gold1", "sky_blue1", "pale_green1",
]

def imprimir_tabla_rich(df, titulo_tabla, fmt=".2f", colorear_fn=None, color_cols=False):
    """Imprime un DataFrame como tabla Rich.
    - colorear_fn: colorea cada celda según su valor numérico
    - color_cols:  colorea cada columna con un color distinto de la paleta
    """
    tabla = Table(title=titulo_tabla, box=box.SIMPLE_HEAVY, show_lines=False,
                  header_style="bold white on dark_blue")

    # Asignar color por columna si se pide
    col_colors = {}
    if color_cols:
        for i, col in enumerate(df.columns):
            col_colors[col] = PALETA_COLS[i % len(PALETA_COLS)]

    # Columna índice
    tabla.add_column(str(df.index.name or ""), style="bold white", justify="right")

    # Columnas de datos — header coloreado si color_cols
    for col in df.columns:
        if color_cols:
            c = col_colors[col]
            tabla.add_column(f"[{c}]{col}[/{c}]", justify="right")
        else:
            tabla.add_column(str(col), justify="right")

    # Filas
    for idx, row in df.iterrows():
        celdas = [str(idx)]
        for col, val in zip(df.columns, row):
            if isinstance(val, str):
                texto = val
            else:
                texto = f"{val:{fmt}}"
                # color por valor tiene prioridad sobre color por columna
                if colorear_fn:
                    c = colorear_fn(val)
                    texto = f"[{c}]{texto}[/{c}]"
                elif color_cols:
                    c = col_colors[col]
                    texto = f"[{c}]{texto}[/{c}]"
            celdas.append(texto)
        tabla.add_row(*celdas)

    console.print(tabla)

def imprimir_tabla4_rich(df4, titulo_tabla):
    """Tabla 4 con MultiIndex dc/l/D: solo la columna N se colorea por valor."""
    tabla = Table(title=titulo_tabla, box=box.SIMPLE_HEAVY, show_lines=False,
                  header_style="bold white on dark_blue")

    cols = df4.columns.tolist()
    tabla.add_column("dc [cm]", style="bold white", justify="right")
    tabla.add_column("l/D",     style="bold white", justify="right")
    for col in cols:
        # Header de N resaltado para indicar que tiene color
        if col == "N":
            tabla.add_column("[bold magenta]N[/bold magenta]", justify="right")
        else:
            tabla.add_column(str(col), justify="right")

    for (dc_val, rel_val), row in df4.iterrows():
        celdas = [f"{dc_val:.3f}", f"{rel_val:.2f}"]
        for col, val in zip(cols, row):
            if isinstance(val, str):
                celdas.append(val)
            elif col == "N":
                # Solo esta columna se colorea por valor
                c = color_N(val)
                celdas.append(f"[{c}]{val:.2f}[/{c}]")
            else:
                celdas.append(f"{val:.4f}")
        tabla.add_row(*celdas)

    console.print(tabla)

# ─────────────────────────────────────────────
#  DATOS DE ENTRADA
# ─────────────────────────────────────────────

titulo("CONSTRUCTOR DE BOBINAS  –  Tabla de Parámetros Constructivos")
print("""
  Tablas generadas con pandas.
  l/D = 1.0  →  bobina cuadrada  |  l/D = 0.5  →  alargada  |  l/D > 1.0  →  más larga que ancha
""")

subtitulo("Datos de entrada")
dc_tienda = input_float("  Ingrese el dc disponible en tienda [cm] (ej: 0.10): ", 0.08, 0.23)
Do        = input_float("  Ingrese Do – diámetro del cilindro base [cm] (1.0 a 3.0): ", 1.0, 3.0)

# ─────────────────────────────────────────────
#  ARRAYS
# ─────────────────────────────────────────────

dc_array  = np.round(np.arange(0.08, 0.24, 0.01), 4)   # 16 valores
rel_array = np.round(np.arange(0.5,  2.05, 0.1),  4)   # 16 relaciones l/D (0.5 → 2.0)

# ─────────────────────────────────────────────
#  TABLA 1 – Parámetros base por dc
# ─────────────────────────────────────────────

subtitulo(f"TABLA 1 – Parámetros base para cada dc  (Do = {Do:.2f} cm)")

registros = []
for dc in dc_array:
    Se = dc
    D  = Do + dc
    Ns = 1.0 / (2.0 * dc)
    marca = "◄ TIENDA" if abs(dc - dc_tienda) < 1e-9 else ""
    registros.append({
        "dc [cm]"  : dc,
        "Se [cm]"  : round(Se, 4),
        "D [cm]"   : round(D,  4),
        "Ns [v/cm]": round(Ns, 4),
        "Nota"     : marca,
    })

df1 = pd.DataFrame(registros).set_index("dc [cm]")
imprimir_tabla_rich(df1, f"Parámetros base  (Do = {Do:.2f} cm)", fmt=".3f")

# ─────────────────────────────────────────────
#  TABLA 2 – Largo l [cm]  (DataFrame 2D)
# ─────────────────────────────────────────────

subtitulo("TABLA 2 – Largo total  l [cm]  =  (l/D) · D")
print(f"  Filas: dc [cm]  |  Columnas: relación l/D  |  l/D=1.0 → cuadrada\n")

cols_l = [f"l/D={r:.2f}" for r in rel_array]
data_l = {}
for r, col in zip(rel_array, cols_l):
    data_l[col] = [round((Do + dc) * r, 4) for dc in dc_array]

df2 = pd.DataFrame(data_l, index=pd.Index(dc_array, name="dc [cm]"))
imprimir_tabla_rich(df2, "Largo total  l [cm]  =  (l/D) · D", fmt=".3f")

# ─────────────────────────────────────────────
#  TABLA 3 – N total de vueltas
# ─────────────────────────────────────────────

subtitulo("TABLA 3 – N total de vueltas  =  Ns · l")
print(f"  Filas: dc [cm]  |  Columnas: relación l/D\n")

cols_n = [f"l/D={r:.2f}" for r in rel_array]
data_n = {}
for r, col in zip(rel_array, cols_n):
    data_n[col] = [round((1.0/(2.0*dc)) * (Do + dc) * r, 2) for dc in dc_array]

df3 = pd.DataFrame(data_n, index=pd.Index(dc_array, name="dc [cm]"))
console.print("\n  [dim]Color celda → N: [red]N<10[/red]  [yellow]10≤N<15[/yellow]  [green]15≤N<20[/green]  [bright_green]N≥20[/bright_green]  |  Cada columna l/D tiene su propio color[/dim]")
imprimir_tabla_rich(df3, "N total de vueltas  =  Ns · l", fmt=".2f", colorear_fn=color_N, color_cols=True)

# ─────────────────────────────────────────────
#  TABLA 4 – Completa: dc × l/D con l, N y L
# ─────────────────────────────────────────────

subtitulo("TABLA 4 – Tabla completa:  dc × l/D  →  l [cm] | N [vueltas] | L [µH]")
print("  Cada fila es una combinación única dc / l/D\n")

filas = []
for dc in dc_array:
    D  = Do + dc
    Ns = 1.0 / (2.0 * dc)
    for rel in rel_array:
        l     = rel * D
        N     = Ns * l
        ratio = D / (2.0 * l)
        K     = 1.0 / (1.0 + 0.9 * ratio - 2e-2 * ratio**2)
        k     = K * (np.pi**2) * rel
        L_uH  = (D**3) * (Ns**2) * k * 1e-3
        marca = "◄" if abs(dc - dc_tienda) < 1e-9 else ""
        filas.append({
            "dc [cm]"  : dc,
            "l/D"      : rel,
            "Se [cm]"  : round(dc,    4),
            "D [cm]"   : round(D,     4),
            "Ns [v/cm]": round(Ns,    3),
            "l [cm]"   : round(l,     4),
            "N"        : round(N,     2),
            "K"        : round(K,     4),
            "k"        : round(k,     4),
            "L [µH]"   : round(L_uH,  4),
            "Tienda"   : marca,
        })

df4 = pd.DataFrame(filas).set_index(["dc [cm]", "l/D"])
console.print("\n  [dim]Cada color representa un valor de l/D distinto[/dim]")
imprimir_tabla4_rich(df4, "Tabla completa:  dc × l/D  →  l [cm] | N [vueltas] | L [µH]")

# ─────────────────────────────────────────────
#  CÁLCULO PUNTUAL – selección del usuario
# ─────────────────────────────────────────────

subtitulo("CÁLCULO PUNTUAL  –  Ingrese los valores elegidos de las tablas")
print()
dc_c  = input_float("  Ingrese dc elegido [cm] (0.08 – 0.23): ", 0.08, 0.23)
rel_c = input_float("  Ingrese l/D elegido   (0.50 – 2.00):  ", 0.5,  2.0)

# Buscar la fila más cercana en df4 (MultiIndex no soporta method="nearest")
dc_cercano  = dc_array[np.argmin(np.abs(dc_array  - dc_c))]
rel_cercano = rel_array[np.argmin(np.abs(rel_array - rel_c))]
fila = df4.loc[[(dc_cercano, rel_cercano)]]

subtitulo("RESULTADO")
console.print()
# Mostrar resultado como tabla Rich
res = fila.reset_index().T
res.columns = ["Valor"]
console.print(res.to_string())

L_val = fila['L [µH]'].values[0]
D_val = fila['D [cm]'].values[0]
l_val = fila['l [cm]'].values[0]
N_val = fila['N'].values[0]
color = color_N(N_val)
console.print(f"""
  ┌───────────────────────────────────────┐
  │   N  =  [{color}]{N_val:>8.2f}[/{color}]  vueltas          │
  │   L  =  [bold cyan]{L_val:>8.4f}[/bold cyan]  µH              │
  └───────────────────────────────────────┘
""")

# ─────────────────────────────────────────────
#  CÁLCULO DE Qd, XL y Rp
# ─────────────────────────────────────────────

subtitulo("CÁLCULO DE Qd, XL y Rp")
f0_MHz = input_float("  Ingrese la frecuencia de operación f0 [MHz]: ", 0.1, 1000.0)
f0_Hz  = f0_MHz * 1e6

# Qd = 8850 · (D·l / (102·l + 45·D)) · √f0   con f0 en MHz, D y l en cm
Qd  = 8850 * (D_val * l_val / (102 * l_val + 45 * D_val)) * np.sqrt(f0_MHz)

# XL = 2·π·f0·L   (L en Henrios)
L_H = L_val * 1e-6
XL  = 2 * np.pi * f0_Hz * L_H

# Rp = Qd · XL
Rp  = Qd * XL

console.print(f"""
  [dim]Fórmulas:[/dim]
    Qd  = 8850 · (D·l / (102·l + 45·D)) · √f0   [f0 en MHz, D y l en cm]
    XL  = 2·π·f0·L                               [f0 en Hz, L en H]
    Rp  = Qd · XL

  ┌─────────────────────────────────────────────────┐
  │  PARÁMETROS DE CALIDAD Y RESISTENCIA PARALELA   │
  ├─────────────────────────────────────────────────┤
  │  f0  = [bold cyan]{f0_MHz:>10.3f}[/bold cyan]  MHz                     │
  │  D   = [bold white]{D_val:>10.4f}[/bold white]  cm                      │
  │  l   = [bold white]{l_val:>10.4f}[/bold white]  cm                      │
  │  L   = [bold cyan]{L_val:>10.4f}[/bold cyan]  µH                     │
  │                                                 │
  │  Qd  = [bold green]{Qd:>10.2f}[/bold green]                           │
  │  XL  = [bold yellow]{XL:>10.4f}[/bold yellow]  Ω                      │
  │  Rp  = [bold cyan]{Rp/1e3:>10.4f}[/bold cyan]  kΩ                     │
  └─────────────────────────────────────────────────┘
""")

# ─────────────────────────────────────────────
#  CÁLCULO DE RT, Rg', RL' y CAPACITORES
# ─────────────────────────────────────────────

subtitulo("CÁLCULO DEL CIRCUITO  –  RT, Rg', RL', CT, C1, C2, C3, C4")
console.print("  [dim]Valores fijos: Qc = 10  |  Rg = 50 Ω  |  RL = 1000 Ω[/dim]\n")

Qc = 10.0
Rg = 50.0
RL = 1000.0

# ── RT = Qc · XL   (ec. 9: Qc = RT/XL)
RT = Qc * XL

# ── Rg' = 2·RT  (ec. 9)
Rg_p = 2 * RT

# ── RL' = 2·RT·Rp / (Rp - 2·RT)  (ec. 38 — exacto incluyendo Rp)
RL_p = (2 * RT * Rp) / (Rp - 2 * RT)

# ── CT = 1 / (L · (2π·f0)²)  (ec. 43)
CT_F  = 1.0 / (L_H * (2 * np.pi * f0_Hz)**2)
CT_pF = CT_F * 1e12

# ── Capacitores desde sistema ec.10:
#    Rg' = (1 + C1/C2)² · Rg  →  x_g = sqrt(Rg'/Rg) - 1 = C1/C2... pero C1<C2 en libro
#    C1·C2/(C1+C2) = CT/2
#    Despejando con x = C2/C1 (C2 es el grande):
#      C1 = CT·(x+1)/(2·x)   →  C1 es el pequeño
#      C2 = x · C1            →  C2 es el grande
#    Mismo criterio para C3/C4

x_g  = np.sqrt(Rg_p / Rg) - 1
_Cb_g = CT_F * (x_g + 1) / (2 * x_g)
_Ca_g = x_g * _Cb_g
C2_F  = max(_Ca_g, _Cb_g)   # grande
C1_F  = min(_Ca_g, _Cb_g)   # pequeño
C1_pF = C1_F * 1e12
C2_pF = C2_F * 1e12

x_l  = np.sqrt(RL_p / RL) - 1
_Cb_l = CT_F * (x_l + 1) / (2 * x_l)
_Ca_l = x_l * _Cb_l
C3_F  = max(_Ca_l, _Cb_l)   # grande
C4_F  = min(_Ca_l, _Cb_l)   # pequeño
C3_pF = C3_F * 1e12
C4_pF = C4_F * 1e12

console.print(f"""
  [dim]Fórmulas (ec. 9 y 10):[/dim]
              
    RT   = Qc · XL
    Rg'  = 2·RT
    RL'  = 2·RT·Rp / (Rp − 2·RT)
    CT   = 1 / (L·(2π·f0)²)
    x_g  = √(Rg'/Rg) − 1
    C1   = x_g · C2                 [hacia Rg]
    C2   = CT·(x_g+1)/(2·x_g)      [hacia bobina]
    x_l  = √(RL'/RL) − 1
    C3   = x_l · C4                 [hacia RL]
    C4   = CT·(x_l+1)/(2·x_l)      [hacia bobina]

  ┌──────────────────────────────────────────────────────┐
  │           RESUMEN COMPLETO DEL CIRCUITO              │
  ├──────────────────────────────────────────────────────┤
  │  [bold white]── Parámetros fijos ──[/bold white]                           │
  │  Qc  = [bold green]{Qc:>10.2f}[/bold green]                              │
  │  Rg  = [bold white]{Rg:>10.2f}[/bold white]  Ω                           │
  │  RL  = [bold white]{RL:>10.2f}[/bold white]  Ω                           │
  ├──────────────────────────────────────────────────────┤
  │  [bold white]── Resistencias ──[/bold white]                               │
  │  XL  = [bold yellow]{XL:>10.4f}[/bold yellow]  Ω                         │
  │  Rp  = [bold cyan]{Rp/1e3:>10.4f}[/bold cyan]  kΩ                        │
  │  RT  = [bold yellow]{RT:>10.4f}[/bold yellow]  Ω                         │
  │  Rg' = [bold cyan]{Rg_p:>10.4f}[/bold cyan]  Ω                           │
  │  RL' = [bold cyan]{RL_p:>10.4f}[/bold cyan]  Ω                           │
  ├──────────────────────────────────────────────────────┤
  │  [bold white]── Capacitores ──[/bold white]                                │
  │  CT  = [bold magenta]{CT_pF:>10.4f}[/bold magenta]  pF                        │
  │  C1  = [bold magenta]{C1_pF:>10.4f}[/bold magenta]  pF  (pequeño, lado Rg)    │
  │  C2  = [bold magenta]{C2_pF:>10.4f}[/bold magenta]  pF  (grande,  lado Rg)    │
  │  C3  = [bold magenta]{C3_pF:>10.4f}[/bold magenta]  pF  (grande,  lado RL)    │
  │  C4  = [bold magenta]{C4_pF:>10.4f}[/bold magenta]  pF  (pequeño, lado RL)    │
  └──────────────────────────────────────────────────────┘
""")

# ─────────────────────────────────────────────
#  MEDICIÓN DE Co Y fo  –  Método de dos frecuencias
# ─────────────────────────────────────────────

subtitulo("MEDICIÓN DE Co y fo  –  Método de dos frecuencias (ec. 57 a 65)")
console.print("""  [dim]Se toman dos mediciones de resonancia con y sin capacitor CF:
    fo1 = resonancia SIN CF   →  L·(CT + Co)
    fo2 = resonancia CON CF   →  L·(CT + Co + CF)

  Valores fijos: CT = 177 pF  |  CF = 100 pF[/dim]
""")

CT_med_pF = 177.0   # pF  (fijo según enunciado)
CF_pF     = 100.0   # pF  (fijo según enunciado)

fo1_MHz = input_float("  Ingrese fo1 [MHz]  (resonancia SIN CF):  ", 0.1, 1000.0)
fo2_MHz = input_float("  Ingrese fo2 [MHz]  (resonancia CON CF):  ", 0.1, 1000.0)

if fo1_MHz <= fo2_MHz:
    console.print("  [red]⚠  fo1 debe ser mayor que fo2 (agregar CF baja la frecuencia). Verificá los valores.[/red]")
else:
    fo1_Hz = fo1_MHz * 1e6
    fo2_Hz = fo2_MHz * 1e6

    # ── Co  (ec. 60)
    # Co = [ CT·(fo2² - fo1²) + CF·fo2² ] / (fo1² - fo2²)
    fo1_sq = fo1_Hz ** 2
    fo2_sq = fo2_Hz ** 2
    Co_F   = (CT_med_pF * 1e-12 * (fo2_sq - fo1_sq) + CF_pF * 1e-12 * fo2_sq) / (fo1_sq - fo2_sq)
    Co_pF  = Co_F * 1e12

    # ── L  (ec. 62)
    # L = 1 / [ (2π·fo1)² · (CT + Co) ]
    L_med_H  = 1.0 / ((2 * np.pi * fo1_Hz)**2 * (CT_med_pF * 1e-12 + Co_F))
    L_med_uH = L_med_H * 1e6

    # ── fo  (ec. 64)
    # fo = 1 / (2π · √(L · CT))
    fo_Hz  = 1.0 / (2 * np.pi * np.sqrt(L_med_H * CT_med_pF * 1e-12))
    fo_MHz = fo_Hz / 1e6

    console.print(f"""
  [dim]Fórmulas aplicadas:[/dim]
    Co = [ CT·(fo2²−fo1²) + CF·fo2² ] / (fo1²−fo2²)   (ec. 60)
    L  = 1 / [ (2π·fo1)² · (CT+Co) ]                   (ec. 62)
    fo = 1 / (2π·√(L·CT))                               (ec. 64)

  ┌──────────────────────────────────────────────────────┐
  │       RESULTADOS  –  Co, L medida y fo               │
  ├──────────────────────────────────────────────────────┤
  │  [bold white]── Datos de entrada ──[/bold white]                           │
  │  CT  = [bold white]{CT_med_pF:>10.1f}[/bold white]  pF  (fijo)               │
  │  CF  = [bold white]{CF_pF:>10.1f}[/bold white]  pF  (fijo)               │
  │  fo1 = [bold cyan]{fo1_MHz:>10.4f}[/bold cyan]  MHz (sin CF)           │
  │  fo2 = [bold cyan]{fo2_MHz:>10.4f}[/bold cyan]  MHz (con CF)           │
  ├──────────────────────────────────────────────────────┤
  │  [bold white]── Resultados ──[/bold white]                                  │
  │  Co  = [bold magenta]{Co_pF:>10.4f}[/bold magenta]  pF                        │
  │  L   = [bold magenta]{L_med_uH:>10.4f}[/bold magenta]  µH                        │
  │  fo  = [bold green]{fo_MHz:>10.4f}[/bold green]  MHz                       │
  └──────────────────────────────────────────────────────┘
""")

titulo("Cálculo finalizado. ¡Éxito en la construcción de tu bobina!")
