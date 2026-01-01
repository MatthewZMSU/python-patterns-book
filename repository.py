import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.execute(
            "INSERT INTO batches (reference, sku, _purchased_quantity, eta) VALUES (:r, :s, :p, :e)",
            {
                "r": batch.reference,
                "s": batch.sku,
                "p": batch._purchased_quantity,
                "e": batch.eta,
            },
        )

    def get(self, reference) -> model.Batch:
        res = self.session.execute("SELECT sku, _purchased_quantity, eta FROM batches WHERE reference = :r", {"r": reference})[0]
        return model.Batch(
            ref=reference,
            sku=res[0],
            qty=res[1],
            eta=res[2],
        )
