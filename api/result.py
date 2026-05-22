from pydantic import BaseModel
from typing import Optional, Union
import time
from fastapi.responses import JSONResponse

class ResultJson(BaseModel):
    msg: str = 'ok'
    data: Optional[Union[dict, list]] = None
    status: int = 200
    timestamp: int

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(i) for i in obj]

    if isinstance(obj, dict):
        return {key: to_dict(obj[key]) for key in obj}

    return obj

def ok(data: Optional[Union[dict, list]] = None, msg: str = 'ok'):
    return ResultJson(
        msg=msg,
        data=to_dict(data) if data is not None else None,
        status=200,
        timestamp=int(time.time() * 1000)
    )

def err(msg: str, code = 500):
    return JSONResponse(status_code=code, content=ResultJson(
        msg=msg,
        status=code,
        timestamp=int(time.time() * 1000)
    ).__dict__)