from pydantic.dataclasses import dataclass
from typing import Literal


@dataclass
class Lake:
    type: Literal["s3", "gcp", "minio"]
    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str

    @property
    def uri(self) -> str:
        return f"{self.type}://{self.bucket}"
