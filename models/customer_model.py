from dataclasses import dataclass

@dataclass(slots=True)
class CustomerModel:
    id: int
    name: str
    amount: int

    def from_tuple(tuple: tuple) -> "CustomerModel":
        customer_model: CustomerModel = CustomerModel(
            id=tuple[0],
            name=tuple[1],
            amount=tuple[2])
        return customer_model
