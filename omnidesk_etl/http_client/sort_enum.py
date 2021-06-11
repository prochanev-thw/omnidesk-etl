import enum

class Sort(str, enum.Enum):
    pass

class CaseSort(Sort):
    BY_CREATED_ASC = 'created_at_desc'
