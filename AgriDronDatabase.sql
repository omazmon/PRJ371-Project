use master 
create database AgriDrone;
go
use AgriDrones;
GO
CREATE TABLE CropHealthData (
    DataID INT PRIMARY KEY,
    CropID INT,
    Timestamp DATETIME,
    NDVI FLOAT,
    Temperature FLOAT,
    Humidity FLOAT,
    PestStatus VARCHAR(50),
    DiseaseStatus VARCHAR(50),
    IrrigationStatus VARCHAR(50),
    GPSLatitude DECIMAL(10, 6),
    GPSLongitude DECIMAL(10, 6),
);
