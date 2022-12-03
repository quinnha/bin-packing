from typing import TypedDict


class BinPackMetrics(TypedDict):
    """Model the metrics of bin packing application"""

    data_access: float
    comparisons: int
    operations: int
    results: list[list[int]]
