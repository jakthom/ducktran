from pydantic.dataclasses import dataclass
from typing import Literal, List


@dataclass
class Table:
    table_catalog: str
    table_schema: str
    table_name: str
    load_type: Literal["full", "incremental"]
    highwater_column: str
    hash_columns: List[str]
    exclude_columns: List[str]

    @property
    def fqn(self) -> str:
        return f"{self.table_catalog}.{self.table_schema}.{self.table_name}"
