from typing import Union
from pydantic import BaseModel
from datetime import datetime


class dataLogs(BaseModel):
    startTime: datetime
    app: str
    client_id: Union[str, None] = None
    platform: str
    browser: str
    path: str
    path_params: Union[str, None] = None
    method: str
    ipaddress: str
    username: Union[str, None] = None
    status_code: Union[int, None] = None
    process_time: Union[float, None] = None
