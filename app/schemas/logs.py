from typing import Generic, TypeVar, List, Optional, Union, Annotated, Any, Dict
from pydantic import BaseModel, Json, Field, EmailStr
from datetime import date, time


class dataLogs(BaseModel):
    create_date: date
    create_time: time
    app: str
    path: str
    method: str
    ipaddress: str
    username: Union[str, None] = None
    useraccess: Union[str, None] = None
    path_params: Union[Json, None] = None
    status_code: Union[int, None] = None
    process_time: Union[float, None] = None
