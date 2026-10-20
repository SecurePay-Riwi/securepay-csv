"""Precisión de cada moneda.

Es una copia mínima de money.py del repo securepay-generator: los extractos
no importan nada del generador. Los decimales por moneda sí vienen de la
librería común securepay-shared.
"""

from decimal import ROUND_HALF_UP, Decimal

from securepay_shared.config import MONEDA_DECIMALES


def paso(moneda):
    """La unidad más pequeña de la moneda: 0.01, o 1 para el yen."""
    return Decimal(1).scaleb(-MONEDA_DECIMALES[moneda])


def redondear(monto, moneda):
    """Deja el monto con los decimales que admite su moneda."""
    return Decimal(monto).quantize(paso(moneda), rounding=ROUND_HALF_UP)
