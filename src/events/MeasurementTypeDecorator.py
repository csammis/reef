from sqlalchemy.types import TypeDecorator, Enum
from events import MeasurementType

class Enum3(TypeDecorator):

    impl = Enum

    def process_bind_param(self, value, dialect):
        if type(value) is MeasurementType.MeasurementType:
            value = value.name
        return value

    def process_literal_value(self, value, dialect): #pragma: no cover
        if type(value) is MeasurementType.MeasurementType:
            value = value.name
        return value

    def process_result_value(self, value, dialect):
        return MeasurementType.MeasurementType[value]
