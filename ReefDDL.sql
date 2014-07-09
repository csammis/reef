-- Reef controller / logger DDL

-- Supported events may be:
--  A Measurement (of pH, KH, Calcium, etc.)
--  A LogEntry (noting a water change, new addition, etc.)
--  A HardwareEvent (heater on, topoff pump off, etc.)

CREATE TABLE Measurement
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    MeasurementTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    MeasurementType INTEGER NOT NULL,
    Value REAL
);

CREATE TABLE LogEntry
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    EntryTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    Entry TEXT
);

CREATE TABLE HardwareEvent
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    EventTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    HardwareType INTEGER NOT NULL,
    State INTEGER NOT NULL
);
