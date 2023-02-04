from duckdb import DuckDBPyConnection
from pydantic import BaseModel


class Sql(BaseModel):
    stmt: str
