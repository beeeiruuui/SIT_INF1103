from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        raise NotImplementedError


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        return total - self.amount if total >= self.threshold else total


class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95
