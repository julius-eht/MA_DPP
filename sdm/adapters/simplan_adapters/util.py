from typing import Optional, TypeVar

A = TypeVar("A")


def assure_defined(value: Optional[A], message: Optional[str] = None) -> A:
    if value is None:
        raise ValueError(message or f"expected {A}")
    else:
        return value
