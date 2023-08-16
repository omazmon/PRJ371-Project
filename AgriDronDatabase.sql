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

-- Field Table
CREATE TABLE Field (
    Field_ID INT PRIMARY KEY,
    Field_Name VARCHAR(255),
    Crop_Type VARCHAR(100),
    GPS_Coordinates VARCHAR(50)
);

-- Flight Log Table
CREATE TABLE FlightLog (
    Flight_ID INT PRIMARY KEY,
    Field_ID INT,
    Flight_Date DATE,
    Flight_Duration TIME,
    Purpose VARCHAR(100),
    FOREIGN KEY (Field_ID) REFERENCES Field(Field_ID)
);

-- Image Table
CREATE TABLE Image (
    Image_ID INT PRIMARY KEY,
    Flight_ID INT,
    Image_File_Path VARCHAR(255),
    Capture_Date DATE,
    Sensor_Type VARCHAR(50),
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
);

-- Orthomosaic Table
CREATE TABLE Orthomosaic (
    Orthomosaic_ID INT PRIMARY KEY,
    Flight_ID INT,
    Mosaic_File_Path VARCHAR(255),
    Processing_Date DATE,
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
);



-- Elevation Data Table
CREATE TABLE ElevationData (
    Elevation_ID INT PRIMARY KEY,
    Field_ID INT,
    Image_ID INT,
    Elevation_Values TEXT, -- Store elevation data as needed
    FOREIGN KEY (Field_ID) REFERENCES Field(Field_ID),
    FOREIGN KEY (Image_ID) REFERENCES Image(Image_ID)
);

-- Pest Monitoring Table
CREATE TABLE PestMonitoring (
    Pest_ID INT PRIMARY KEY,
    Pest_Name VARCHAR(100),
    Description TEXT,
    Treatment_Methods TEXT
);

-- Pest Detection Table
CREATE TABLE PestDetection (
    Detection_ID INT PRIMARY KEY,
    Field_ID INT,
    Image_ID INT,
    Pest_ID INT,
    Pest_Count INT,
    Pest_Location VARCHAR(255),
    FOREIGN KEY (Field_ID) REFERENCES Field(Field_ID),
    FOREIGN KEY (Image_ID) REFERENCES Image(Image_ID),
    FOREIGN KEY (Pest_ID) REFERENCES PestMonitoring(Pest_ID)
);

-- User Table
CREATE TABLE User (
    User_ID INT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Username VARCHAR(50),
    Password VARCHAR(100),
    Role VARCHAR(50)
);








