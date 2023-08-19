use master
Create database AgriDrone;
go
use AgriDrone;
CREATE TABLE Farm(
    FarmID INT PRIMARY KEY,
    FarmName VARCHAR(100),
    Location VARCHAR(200),
    FarmSize FLOAT,
    OwnerName VARCHAR(100),
    ContactNumber VARCHAR(20)
);
GO
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
CREATE TABLE CropHealthData (
    DataID INT PRIMARY KEY,
    CropID INT,
	Field_ID INT,
    Timestamp DATETIME,
    NDVI FLOAT,
    Temperature FLOAT,
    Humidity FLOAT,
    PestStatus VARCHAR(50),
    DiseaseStatus VARCHAR(50),
    IrrigationStatus VARCHAR(50),
    Field_Name VARCHAR(255),
    Crop_Type VARCHAR(100),
    GPS_Coordinates VARCHAR(50),
	LastUpdate DATETIME
	FOREIGN KEY (CropID) REFERENCES Crops(CropID),
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
);
GO
CREATE TABLE IrrigationSchedule (
    ScheduleID INT PRIMARY KEY,
    FieldID INT, -- Foreign key to link to Fields table
    CropID INT, -- Foreign key to link to Crops table
    Date DATE NOT NULL,
    AmountToIrrigate DECIMAL(5, 2) NOT NULL,
);
CREATE TABLE PestControlData(
    PestID INT PRIMARY KEY,
    Datetime DATETIME,
    Image VARCHAR(MAX),
    Coordinates GEOGRAPHY,
    TemperatureDetected FLOAT,
    Object VARCHAR(255),
);

-- Flight Log Table
CREATE TABLE FlightLog (
    Flight_ID INT PRIMARY KEY,
    Field_ID INT,
    Flight_Date DATE,
    Flight_Duration TIME,
    Purpose VARCHAR(100),
    FOREIGN KEY (Field_ID) REFERENCES CropHealth(Field_ID)
);

-- Image Table
CREATE TABLE Image (
    Image_ID INT PRIMARY KEY,
    Flight_ID INT,
    Image_File_Path VARCHAR(255),
    Capture_Date DATE,
    Sensor_Type VARCHAR(50),
	Datetime DATETIME,
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
);

-- Orthomosaic Table maybe change the name of the table to heat map table
CREATE TABLE Orthomosaic (
    Orthomosaic_ID INT PRIMARY KEY,
    Flight_ID INT,
    Mosaic_File_Path VARCHAR(255),
    Processing_Date DATE,
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
); --remember i did aeriel surveying and mapping, this table is about the images collected to make a bigger image.
  --meaning the images taken by the dron would be relatively small, this combines those images to make a bigger picture.
--e.g surveying one large area.

-- Elevation Data Table
CREATE TABLE ElevationData (
    Elevation_ID INT PRIMARY KEY,
    Field_ID INT,
    Image_ID INT,
    Elevation_Values TEXT, -- Store elevation data as needed
    FOREIGN KEY (Field_ID) REFERENCES Field(Field_ID),
    FOREIGN KEY (Image_ID) REFERENCES Image(Image_ID)
);--Dont think this table is neccessary remember the drone already has the built-in function 
-- This is about ground elevation not drone elevation hence the field ID and image ID. unless we're assuming that the farm is on leveled ground?



-- User Table
CREATE TABLE Users(
    User_ID INT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Username VARCHAR(50),
    Password VARCHAR(100),
    Role VARCHAR(50)
);
