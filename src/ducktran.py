from typing import Union
import duckdb
from duckdb import InvalidInputException
from src.config import PostgresConnectionParams
from src.constants import DUCKTRAN, DUCKDB_EXT_POSTGRES, DUCKDB_EXT_HTTPFS
from src.lake import Lake
from src.config import ReplicationConfig
from src.pg import Table
from src.sql import Sql


class Ducktran:
    def __init__(self, sourceConnectionParams: PostgresConnectionParams, lake: Lake):
        self.connection_params = sourceConnectionParams
        self.lake = lake
        self.connection = duckdb.connect(DUCKTRAN, read_only=False)
        # Install and Load DuckDB Extensions
        for extension in [DUCKDB_EXT_HTTPFS, DUCKDB_EXT_POSTGRES]:
            self.connection.install_extension(extension)
            try:
                self.connection.load_extension(extension)
            except InvalidInputException:
                # If an extension has already been loaded this err is thrown.
                # Ignore it for now.
                pass

    def _init_httpfs(self) -> None:
        self.connection.execute(
            f"""
            SET s3_region = '{self.lake.region}';
            SET s3_access_key_id='{self.lake.access_key_id}';
            SET s3_secret_access_key='{self.lake.secret_access_key}';
        """
        )

    def _get_replication_config(self) -> ReplicationConfig:
        get_structure_sql = Sql(
            stmt=(
                "select json_structure(json) "
                f"from read_json_objects('{self.lake.uri}/config.json');"
            )
        )
        json_structure = self.connection.execute(get_structure_sql.stmt).fetchone()[0]
        get_config_sql = Sql(
            stmt=(
                f"select json_transform(json, '{json_structure}') "
                f"from read_json_objects('{self.lake.uri}/config.json');"
            )
        )
        return ReplicationConfig(
            **self.connection.execute(get_config_sql.stmt).fetchone()[0]
        )

    def _get_lake_highwater(self, table: Table):
        get_highwater_sql = Sql(
            stmt=(f"select highwater from read_csv_auto('{table.path}');")
        )

    def _set_lake_highwater(self, table: Table):
        pass

    def sync_table_full(self, table: Table):
        pass

    def sync_table_incremental(self):
        pass

    # def sync_logical_replication(self):
    # pass
