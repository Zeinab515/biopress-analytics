from pydantic import BaseModel


class Summary(BaseModel):
    opportunities: int
    actions: int
    compliance_rate: float | None
    ci_low: float
    ci_high: float


class GroupRow(BaseModel):
    group: str
    n: int
    complied: int
    rate: float
    ci_low: float
    ci_high: float


class GroupTest(BaseModel):
    name: str
    chi2: float
    dof: int
    p_value: float
    min_expected_count: float


class GroupAnalysis(BaseModel):
    dimension: str
    rows: list[GroupRow]
    test: GroupTest
    note: str
