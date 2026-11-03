from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain import Order
from src.repository import OrderRow, SqlOrderRepository, make_engine


def test_repository_commit():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.commit()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)).total == 120

def test_repository_rollback():
    engine = make_engine()
    with Session(engine) as session:
        SqlOrderRepository(session).save(1, Order(120))
        session.rollback()
        assert session.scalar(select(OrderRow).where(OrderRow.id == 1)) is None

def test_repository_save_order_250():
    engine = make_engine()
    with Session(engine) as session:
        # Guarda un pedido con id=2 y total=250
        SqlOrderRepository(session).save(2, Order(250))
        session.commit()
        
        # Se consulta
        row = session.scalar(select(OrderRow).where(OrderRow.id == 2))
        
        # Verificamos id, total y estado
        assert row is not None
        assert row.id == 2
        assert row.total == 250
        assert row.status == "NEW" 