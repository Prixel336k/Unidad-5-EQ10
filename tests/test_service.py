from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))

def test_payment_approved_example():
    gateway = Mock()
    gateway.charge.return_value = True
    amount = OrderService(gateway).checkout(Order(100))
    assert amount == 100
    gateway.charge.assert_called_once_with(100)

def test_vip_payment_rejected():
    gateway = Mock()
    gateway.charge.return_value = False  # Simulamos que la pasarela rechaza el pago
    
    # Creacion de pedido VIP de $200 (con 15% de descuento donde el cobro sera de $170)
    order = Order(200, vip=True)
    
    # Verificacion de que se lance el RuntimeError por pago rechazado
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(order)
        
    # Verificacion que el intento de cobro al servicio externo fue exactamente por $170
    gateway.charge.assert_called_once_with(170)