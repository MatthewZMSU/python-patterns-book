from __future__ import annotations

import model
from model import OrderLine
from repository import AbstractRepository


class InvalidSku(Exception):
    pass


class NotAllocatedError(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref: str, sku: str, qty: int, eta, repo: AbstractRepository, session):
    batch = model.Batch(ref, sku, qty, eta)
    repo.add(batch)
    session.commit()


def deallocate(line: OrderLine, repo: AbstractRepository, session):
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    for batch in batches:
        if batch.deallocate(line):
            session.commit()
            return
    raise NotAllocatedError
