from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")


class Result(Generic[T, E]):
    def __init__(self, ok: T = None, err: E = None):
        self.ok = ok
        self.err = err

    @classmethod
    def Ok(cls, value: T) -> "Result[T, E]":
        return cls(ok=value)

    @classmethod
    def Err(cls, error: E) -> "Result[T, E]":
        return cls(err=error)

    def is_ok(self) -> bool:
        return self.err is None

    def is_err(self) -> bool:
        return self.ok is None

    def unwrap(self) -> T:
        if self.is_err():
            raise ValueError(f"Called unwrap on an Err value: {self.err}")
        return self.ok

    def unwrap_err(self) -> E:
        if self.is_ok():
            raise ValueError(f"Called unwrap_err on an Ok value: {self.ok}")
        return self.err
