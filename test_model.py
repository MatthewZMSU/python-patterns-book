from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
    line = OrderLine("order-ref", "SMALL-TABLE", qty=2)

    batch.allocate(line)

    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
    line = OrderLine("order-ref", "SMALL-TABLE", qty=2)

    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch("batch-001", "SMALL-TABLE", qty=2, eta=today)
    line = OrderLine("order-ref", "SMALL-TABLE", qty=3)

    assert batch.can_allocate(line)


def test_can_allocate_if_available_equal_to_required():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=today)
    line = OrderLine("order-ref", "SMALL-TABLE", qty=20)

    assert batch.can_allocate(line)


def test_prefers_warehouse_batches_to_shipments():
    warehouse_batch = Batch("warehouse-batch-001", "SMALL-TABLE", qty=2, eta=today)
    shipment_batch = Batch("shipment-batch-01", "SMALL-TABLE", qty=4, eta=tomorrow)

    line = OrderLine("order-ref", "SMALL-TABLE", qty=1)

    allocate(line, [warehouse_batch, shipment_batch])


def test_prefers_earlier_batches():
    shipment_batch_1 = Batch("shipment-batch-01", "SMALL-TABLE", qty=2, eta=tomorrow)
    shipment_batch_2 = Batch("shipment-batch-02", "SMALL-TABLE", qty=4, eta=later)

    line = OrderLine("order-ref", "SMALL-TABLE", qty=1)

    assert allocate(line, [shipment_batch_1, shipment_batch_2]) == "shipment-batch-01"
