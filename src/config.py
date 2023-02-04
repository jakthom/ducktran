from typing import List
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from src.pg import Table


@dataclass
class ReplicationConfig:
    tables: List[Table]
    batch_size: int = 25000


class LibpqConnectionString(BaseModel):
    connectionString: str

    def __str__(self) -> str:
        return self.connectionString


class LibpqConnectionUri(BaseModel):
    connectionUri: str

    def __str__(self) -> str:
        return self.connectionUri


class PostgresConnectionParams(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str

    @property
    def connection_string(self) -> LibpqConnectionString:
        return LibpqConnectionString(
            connectionString=(
                f"host={self.host} port={self.port} "
                f"user={self.user} password={self.password} "
                f"dbname={self.dbname}"
            )
        )

    @property
    def connection_uri(self) -> LibpqConnectionUri:
        return LibpqConnectionUri(
            connectionUri=f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        )
