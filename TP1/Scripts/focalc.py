"""
=============================================================
  MEDICIÓN DE Co y fo  –  Método de dos frecuencias
=============================================================
  Basado en ecuaciones 57 a 65:
    fo1 = 1 / (2π·√(L·(CT+Co)))        SIN CF
    fo2 = 1 / (2π·√(L·(CT+Co+CF)))     CON CF
    Co  = [CT·(fo2²−fo1²) + CF·fo2²] / (fo1²−fo2²)
    fo  = 1 / (2π·√(L·CT))

  CT se calcula a partir de C1, C2, C3, C4:
    C1·C2/(C1+C2) = CT/2   (lado Rg)
    C3·C4/(C3+C4) = CT/2   (lado RL)
=============================================================
"""

import numpy as np
from rich.console import Console

console = Console()

# ─────────────────────────────────────────────
#  Utilidades
# ─────────────────────────────────────────────

def titulo(texto, ancho=62):
    console.print("\n" + "═" * ancho)
    console.print(f"  [bold cyan]{texto}[/bold cyan]")
    console.print("═" * ancho)

def subtitulo(texto, ancho=62):
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

# ─────────────────────────────────────────────
#  ENCABEZADO
# ─────────────────────────────────────────────

titulo("CÁLCULO DE Co y fo  –  Método de dos frecuencias")
console.print("""
  Se toman [bold]dos mediciones[/bold] de resonancia:
    [cyan]fo1[/cyan]  →  resonancia [bold]SIN[/bold] capacitor CF   →  circuito L·(CT+Co)
    [cyan]fo2[/cyan]  →  resonancia [bold]CON[/bold] capacitor CF   →  circuito L·(CT+Co+CF)

  [dim]fo2 debe ser menor que fo1 (agregar CF baja la frecuencia)[/dim]
""")

# ─────────────────────────────────────────────
#  CÁLCULO DE CT  a partir de C1, C2, C3, C4
# ─────────────────────────────────────────────

subtitulo("PASO 1 – Cálculo de CT desde los capacitores del circuito")
console.print("""  [dim]Red divisora: dos pares en serie
    C1·C2 / (C1+C2) = CT/2   →  lado Rg
    C3·C4 / (C3+C4) = CT/2   →  lado RL
    CT = 2 · C1·C2/(C1+C2)   (ambos pares deben coincidir)[/dim]
""")

C1_pF = input_float("  Ingrese C1 [pF]: ", 0.001, 1e7)
C2_pF = input_float("  Ingrese C2 [pF]: ", 0.001, 1e7)
C3_pF = input_float("  Ingrese C3 [pF]: ", 0.001, 1e7)
C4_pF = input_float("  Ingrese C4 [pF]: ", 0.001, 1e7)

CT_desde_12 = 2 * (C1_pF * C2_pF) / (C1_pF + C2_pF)
CT_desde_34 = 2 * (C3_pF * C4_pF) / (C3_pF + C4_pF)
CT_prom     = (CT_desde_12 + CT_desde_34) / 2
diferencia  = abs(CT_desde_12 - CT_desde_34)
tolerancia  = 0.01 * CT_prom   # 1%

console.print(f"""
  [dim]Verificación:[/dim]
    C1‖C2  →  CT = [bold]{CT_desde_12:.4f}[/bold] pF
    C3‖C4  →  CT = [bold]{CT_desde_34:.4f}[/bold] pF
""")

if diferencia > tolerancia:
    console.print(f"  [yellow]⚠  Los pares difieren en {diferencia:.4f} pF (>1%). Se usará el promedio.[/yellow]")
else:
    console.print(f"  [green]✔  Ambos pares coinciden.[/green]")

CT_pF = CT_prom
console.print(f"  [bold]CT = {CT_pF:.4f} pF[/bold]\n")

# ─────────────────────────────────────────────
#  DATOS DE ENTRADA RESTANTES
# ─────────────────────────────────────────────

subtitulo("PASO 2 – Inductancia, CF y frecuencias medidas")

L_uH    = input_float("  Ingrese L   – inductancia             [µH]: ", 1e-6, 1e6)
CF_pF   = input_float("  Ingrese CF  – capacitor externo       [pF]: ", 0.001, 1e6)

console.print()
fo1_MHz = input_float("  Ingrese fo1 [MHz]  (resonancia SIN CF): ", 0.001, 10000.0)
fo2_MHz = input_float("  Ingrese fo2 [MHz]  (resonancia CON CF): ", 0.001, 10000.0)

# ─────────────────────────────────────────────
#  VALIDACIÓN
# ─────────────────────────────────────────────

if fo1_MHz <= fo2_MHz:
    console.print("""
  [bold red]✗  Error:[/bold red] fo1 debe ser [bold]mayor[/bold] que fo2.
     Agregar CF incrementa la capacitancia total y reduce la frecuencia.
     Verificá que no hayas invertido los valores.
""")
else:
    # ─────────────────────────────────────────────
    #  CÁLCULOS
    # ─────────────────────────────────────────────

    L_H    = L_uH  * 1e-6
    CT_F   = CT_pF * 1e-12
    CF_F   = CF_pF * 1e-12
    fo1_Hz = fo1_MHz * 1e6
    fo2_Hz = fo2_MHz * 1e6
    fo1_sq = fo1_Hz ** 2
    fo2_sq = fo2_Hz ** 2

    # Co  (ec. 60)
    Co_F  = (CT_F * (fo2_sq - fo1_sq) + CF_F * fo2_sq) / (fo1_sq - fo2_sq)
    Co_pF = Co_F * 1e12

    # fo  (ec. 64)
    fo_Hz  = 1.0 / (2 * np.pi * np.sqrt(L_H * CT_F))
    fo_MHz = fo_Hz / 1e6

    # ─────────────────────────────────────────────
    #  RESULTADOS
    # ─────────────────────────────────────────────

    subtitulo("Resultados")

    console.print(f"""
  [dim]Fórmulas aplicadas:[/dim]
    CT  = 2 · C1·C2/(C1+C2)  =  2 · C3·C4/(C3+C4)
    Co  = [ CT·(fo2²−fo1²) + CF·fo2² ] / (fo1²−fo2²)   [bold](ec. 60)[/bold]
    fo  = 1 / (2π · √(L·CT))                             [bold](ec. 64)[/bold]

  ┌──────────────────────────────────────────────────┐
  │  [bold white]── Datos ingresados ──[/bold white]                        │
  │  C1  = [bold white]{C1_pF:>10.4f}[/bold white]  pF                      │
  │  C2  = [bold white]{C2_pF:>10.4f}[/bold white]  pF                      │
  │  C3  = [bold white]{C3_pF:>10.4f}[/bold white]  pF                      │
  │  C4  = [bold white]{C4_pF:>10.4f}[/bold white]  pF                      │
  │  CT  = [bold white]{CT_pF:>10.4f}[/bold white]  pF  (calculado)         │
  │  L   = [bold white]{L_uH:>10.4f}[/bold white]  µH                      │
  │  CF  = [bold white]{CF_pF:>10.4f}[/bold white]  pF                      │
  │  fo1 = [bold cyan]{fo1_MHz:>10.4f}[/bold cyan]  MHz  (sin CF)        │
  │  fo2 = [bold cyan]{fo2_MHz:>10.4f}[/bold cyan]  MHz  (con CF)        │
  ├──────────────────────────────────────────────────┤
  │  [bold white]── Resultados ──[/bold white]                               │
  │  Co  = [bold magenta]{Co_pF:>10.4f}[/bold magenta]  pF                      │
  │  fo  = [bold green]{fo_MHz:>10.4f}[/bold green]  MHz                     │
  └──────────────────────────────────────────────────┘
""")

    titulo("Cálculo finalizado.")
