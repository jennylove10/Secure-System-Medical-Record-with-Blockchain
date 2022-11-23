from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Transaction(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class diagnosis2Request(_message.Message):
    __slots__ = ["doctorname", "fee", "patientname", "prescription"]
    DOCTORNAME_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    PATIENTNAME_FIELD_NUMBER: _ClassVar[int]
    PRESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    doctorname: str
    fee: float
    patientname: str
    prescription: str
    def __init__(self, doctorname: _Optional[str] = ..., patientname: _Optional[str] = ..., prescription: _Optional[str] = ..., fee: _Optional[float] = ...) -> None: ...

class diagnosis2Response(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class diagnosisRequest(_message.Message):
    __slots__ = ["doctorname", "fee", "patientname", "prescription"]
    DOCTORNAME_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    PATIENTNAME_FIELD_NUMBER: _ClassVar[int]
    PRESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    doctorname: str
    fee: float
    patientname: str
    prescription: str
    def __init__(self, doctorname: _Optional[str] = ..., patientname: _Optional[str] = ..., prescription: _Optional[str] = ..., fee: _Optional[float] = ...) -> None: ...

class diagnosisResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: int
    def __init__(self, result: _Optional[int] = ...) -> None: ...

class startMiningRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class startMiningResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...
