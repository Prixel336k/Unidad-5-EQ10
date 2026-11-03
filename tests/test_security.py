from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)

def test_admin_can_cancel_other_user_new_order():
    # Un administrador (user_id=99, is_admin=True) cancela el pedido de otro dueño (owner=1)
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 99, True, now, now) is True

def test_owner_cannot_cancel_after_24_hours():
    # El propietario (user_id=1, owner=1) intenta cancelar un pedido de hace 24 horas
    now = datetime.now(UTC)
    old_date = now - timedelta(hours=24)
    assert not can_cancel("NEW", 1, 1, False, old_date, now)