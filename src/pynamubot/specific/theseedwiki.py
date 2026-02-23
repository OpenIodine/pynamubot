import enum


class NamespaceType(enum.Enum):
    CATEGORY = "분류"
    DOCUMENT = "문서"
    FRAME = "틀"
    FILE = "파일"
    TEMPLATE = "템플릿"
    USER = "사용자"
    META = "더시드위키"
    TRASH = "휴지통"
    SYSTEM = "시스템"
    FILE_TRASH = "파일휴지통"


class BacklinkType(enum.IntEnum):
    ANY = 0
    LINK = 1
    FILE = 2
    INCLUDE = 4
    REDIRECT = 8
