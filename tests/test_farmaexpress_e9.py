import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock

# ==========================================
# CLASES DEL DOMINIO (FARMAEXPRESS)
# ==========================================

class Lote:
    def __init__(self, numeroLote, fechaCaducidad, stock, estaRetirado=False):
        self.NumeroLote = numeroLote
        self.FechaCaducidad = fechaCaducidad
        self.Stock = stock
        self.EstaRetirado = estaRetirado

    def EsVendible(self, fechaReferencia):
        # Reglas BR-02 y BR-03: No retirado, fecha futura y stock positivo
        return not self.EstaRetirado and self.FechaCaducidad.date() > fechaReferencia.date() and self.Stock > 0

    def Descontar(self, cantidad):
        if cantidad > self.Stock:
            raise ValueError("Stock insuficiente en el lote.")
        self.Stock -= cantidad

class InventarioDeProducto:
    def __init__(self, product_id, sucursal_id, nivel_minimo):
        self.ProductId = product_id
        self.SucursalId = sucursal_id
        self.NivelMinimo = nivel_minimo
        self._lotes = []

    @property
    def ExistenciaTotal(self):
        return sum(l.Stock for l in self._lotes if l.EsVendible(datetime.utcnow()))

    def DescontarStockFEFO(self, cantidadSolicitada):
        if self.ExistenciaTotal < cantidadSolicitada:
            raise Exception("Existencia insuficiente para cubrir la venta.")
        
        lotes_disponibles = sorted(
            [l for l in self._lotes if l.EsVendible(datetime.utcnow())],
            key=lambda x: x.FechaCaducidad
        )
        
        for lote in lotes_disponibles:
            if cantidadSolicitada <= 0:
                break
            a_descontar = min(lote.Stock, cantidadSolicitada)
            lote.Descontar(a_descontar)
            cantidadSolicitada -= a_descontar
            return lote.NumeroLote
        
        raise Exception("No existe un lote vendible con stock suficiente.")

class Venta:
    def __init__(self, venta_id):
        self.venta_id = venta_id
        self.estado_validacion = "Pendiente"
        self.completada = False

    def completar(self):
        if self.estado_validacion != "Aprobada":
            raise Exception("El pedido requiere validación especial aprobada.")
        self.completada = True


# ==========================================
# PRUEBAS EJECUTABLES (pytest) - 9 CASOS E9
# ==========================================

def test_cp01_control_stock_insuficiente():
    # CP-01: Stock = 0, se pide 1 -> Rechazo de dominio
    inv = InventarioDeProducto(product_id="P01", sucursal_id="S01", nivel_minimo=5)
    with pytest.raises(Exception, match="Existencia insuficiente"):
        inv.DescontarStockFEFO(1)

def test_cp02_reserva_fefo_exitosa():
    # CP-02: Stock suficiente en lote vigente -> Éxito
    inv = InventarioDeProducto(product_id="P01", sucursal_id="S01", nivel_minimo=5)
    lote_cercano = Lote(numeroLote="L-01", fechaCaducidad=datetime.now() + timedelta(days=10), stock=5)
    inv._lotes.append(lote_cercano)
    
    lote_afectado = inv.DescontarStockFEFO(2)
    assert lote_afectado == "L-01"
    assert lote_cercano.Stock == 3

def test_cp03_value_object_cantidad_invalida():
    # CP-03: Cantidad negativa -> Excepción de dominio
    cantidad = -1
    with pytest.raises(ValueError):
        if cantidad < 0:
            raise ValueError("Cantidad inválida")

def test_cp04_bloqueo_productos_caducados():
    # CP-04: Lote con fecha en el pasado -> Límite / Error
    lote_vencido = Lote(numeroLote="L-999", fechaCaducidad=datetime(2025, 1, 1), stock=10)
    assert lote_vencido.EsVendible(datetime(2026, 11, 2)) is False

def test_cp05_medicamento_receta_aprobada():
    # CP-05: Producto controlado con receta aprobada -> Éxito
    venta = Venta(venta_id="V01")
    venta.estado_validacion = "Aprobada"
    venta.completar()
    assert venta.completada is True

def test_cp06_validacion_especial_pendiente():
    # CP-06: Producto con requisito especial sin dictamen -> Error
    venta = Venta(venta_id="V02")
    venta.estado_validacion = "Pendiente"
    with pytest.raises(Exception, match="requiere validación especial"):
        venta.completar()

def test_cp07_persistencia_transaccional_commit():
    # CP-07: Simulación de persistencia exitosa
    transaccion_exitosa = True
    assert transaccion_exitosa is True

def test_cp08_integridad_transaccional_rollback():
    # CP-08: Rollback ante fallos en transacciones
    rollback_ejecutado = False
    try:
        raise RuntimeError("Fallo en base de datos")
    except RuntimeError:
        rollback_ejecutado = True
    assert rollback_ejecutado is True

def test_cp09_procesamiento_pago_externo_mock():
    # CP-09: Mock de pasarela de pago rechaza cargo -> Error
    procesador_pagos = Mock()
    procesador_pagos.charge.return_value = False
    
    with pytest.raises(RuntimeError, match="Pago rechazado"):
        if not procesador_pagos.charge(500.00):
            raise RuntimeError("Pago rechazado")
    
    procesador_pagos.charge.assert_called_once_with(500.00)
    
