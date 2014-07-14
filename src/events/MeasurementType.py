from enum import Enum, unique

@unique
class MeasurementType(Enum):
    Phosphate = 1
    Magnesium = 2
    Calcium = 3
    KH = 4
    PH = 5
    SpecificGravity = 6
    Temperature = 7
    Nitrate = 8
    Nitrite = 9
    Ammonia = 10
