use master

create database AgriDrone;
go
use AgriDrone;
-- Create the Crops table
CREATE TABLE Crops (
    CropID INT PRIMARY KEY,
    CropName VARCHAR(100),
    PlantingDate DATE,
    HarvestDate DATE,
    ExpectedYield FLOAT,
    FarmID INT,
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID)
);
GO

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
	LastUpdate DATETIME
	FOREIGN KEY (CropID) REFERENCES Crops(CropID),
);
GO
-- Create the Farm table
CREATE TABLE Farm (
    FarmID INT PRIMARY KEY,
    FarmName VARCHAR(100),
    Location VARCHAR(200),
    FarmSize FLOAT,
    OwnerName VARCHAR(100),
    ContactNumber VARCHAR(20)
);
GO

-- Create the Soil table
CREATE TABLE Soil (
    SoilID INT PRIMARY KEY,
    FarmID INT,
    SoilType VARCHAR(50),
    pH FLOAT,
    NutrientLevels VARCHAR(100),
    FOREIGN KEY (FarmID) REFERENCES Farm(FarmID)
);
GO

-- Create the Technicians table
CREATE TABLE Technicians (
    TechnicianID INT PRIMARY KEY,
    TechnicianName VARCHAR(100),
    ContactNumber VARCHAR(20),
    Specialization VARCHAR(100),
    Certification VARCHAR(100)
);
GO
CREATE TABLE PestControlData(
    PestID INT PRIMARY KEY,
    Datetime DATETIME,
    Image VARCHAR(MAX),
    Coordinates GEOGRAPHY,
    TemperatureDetected FLOAT,
    Object VARCHAR(255),
);
