from typing import Generic, TypeVar, List, Optional, Union, Annotated, Any, Dict
from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time,datetime


class dataLogs(BaseModel):
    startTime: datetime
    app: str
    platform: str
    browser: str
    path: str
    path_params: Union[str, None] = None
    method: str
    ipaddress: str
    username: Union[str, None] = None
    status_code: Union[int, None] = None
    process_time: Union[float, None] = None
