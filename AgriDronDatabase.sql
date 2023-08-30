Use master
create database AgriDrone;
Go
USE AgriDrone;
go
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

-- Create the CropHealthData table
CREATE TABLE CropHealthData (
    DataID INT PRIMARY KEY, -- Assumed primary key
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
    ContactNumber VARCHAR(20)
);
GO

-- Create the IrrigationSchedule table
CREATE TABLE IrrigationSchedule (
    ScheduleID INT PRIMARY KEY,
    FieldID INT,
    CropID INT,
    Date DATE NOT NULL,
    AmountToIrrigate DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (FieldID) REFERENCES CropHealthData(Field_ID),
    FOREIGN KEY (CropID) REFERENCES Crops(CropID)
);
GO

-- Create the PestControlData table
CREATE TABLE PestControlData (
    PestID INT PRIMARY KEY,
    Datetime DATETIME,
    Image VARCHAR(MAX),
    Coordinates GEOGRAPHY,
    TemperatureDetected FLOAT,
    Object VARCHAR(255),
    Field_ID INT,
    CropID INT,
    FOREIGN KEY (Field_ID) REFERENCES CropHealthData(Field_ID),
    FOREIGN KEY (CropID) REFERENCES Crops(CropID)
);
GO

-- Create the FlightLog table
CREATE TABLE FlightLog (
    Flight_ID INT PRIMARY KEY,
    Field_ID INT,
    Flight_Date DATE,
    Flight_Duration TIME,
    Purpose VARCHAR(100),
    CropID INT,
    FOREIGN KEY (Field_ID) REFERENCES CropHealthData(Field_ID),
    FOREIGN KEY (CropID) REFERENCES Crops(CropID)
);
GO

-- Create the Image table
CREATE TABLE Image (
    Image_ID INT PRIMARY KEY,
    Flight_ID INT,
    Image_File_Path VARCHAR(255),
    Capture_Date DATE,
    Sensor_Type VARCHAR(50),
    Datetime DATETIME,
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
);
GO

-- Create the Orthomosaic table
CREATE TABLE Orthomosaic (
    Orthomosaic_ID INT PRIMARY KEY,
    Flight_ID INT,
    Mosaic_File_Path VARCHAR(255),
    Processing_Date DATE,
    FOREIGN KEY (Flight_ID) REFERENCES FlightLog(Flight_ID)
);
GO

-- Create the ElevationData table
CREATE TABLE ElevationData (
    Elevation_ID INT PRIMARY KEY,
    Field_ID INT,
    Image_ID INT,
    Elevation_Values TEXT,
    FOREIGN KEY (Field_ID) REFERENCES CropHealthData(Field_ID),
    FOREIGN KEY (Image_ID) REFERENCES Image(Image_ID)
);
GO

-- Create the Users table
CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Username VARCHAR(50),
    Password VARCHAR(100),
    Role VARCHAR(50),
    FOREIGN KEY (Role) REFERENCES CropHealthData(Crop_Type)
);
GO

GO
INSERT INTO Farm(FarmID, FarmName, Location, FarmSize, OwnerName, ContactNumber)
VALUES
    (1, 'Farm 1', 'Location 1', 100.5, 'Owner 1', '123-456-7890'),
    (2, 'Farm 2', 'Location 2', 75.2, 'Owner 2', '987-654-3210'),
    (3, 'Farm 3', 'Location 3', 200.0, 'Owner 3', '555-555-5555'),
    (4, 'Farm 4', 'Location 4', 50.8, 'Owner 4', '777-888-9999'),
    (5, 'Farm 5', 'Location 5', 120.3, 'Owner 5', '111-222-3333');

-- Insert data into the Crops table
INSERT INTO Crops(CropID, CropName, PlantingDate, HarvestDate, ExpectedYield, FarmID)
VALUES
    (1, 'Crop 1', '2023-04-10', '2023-07-15', 500.0, 1),
    (2, 'Crop 2', '2023-05-05', '2023-08-20', 750.0, 2),
    (3, 'Crop 3', '2023-04-15', '2023-07-10', 600.0, 3),
    (4, 'Crop 4', '2023-05-01', '2023-08-25', 480.0, 4),
    (5, 'Crop 5', '2023-04-20', '2023-07-30', 680.0, 5);

-- Insert data into the CropHealthData table
INSERT INTO CropHealthData (DataID, CropID, Field_ID, Timestamp, NDVI, Temperature, Humidity, PestStatus, DiseaseStatus, IrrigationStatus, Field_Name, Crop_Type, GPS_Coordinates, LastUpdate)
VALUES
    (1, 1, 1, '2023-05-10 08:00:00', 0.75, 28.5, 60.0, 'Low', 'None', 'Sufficient', 'Field 1', 'Crop 1', 'GPS1', '2023-05-10 08:30:00'),
    (2, 2, 2, '2023-05-12 09:15:00', 0.68, 29.0, 58.5, 'Moderate', 'None', 'Insufficient', 'Field 2', 'Crop 2', 'GPS2', '2023-05-12 09:45:00'),
    (3, 3, 3, '2023-05-15 07:45:00', 0.82, 27.5, 62.3, 'Low', 'None', 'Sufficient', 'Field 3', 'Crop 3', 'GPS3', '2023-05-15 08:15:00'),
    (4, 4, 4, '2023-05-18 10:30:00', 0.72, 30.2, 57.8, 'High', 'Early Signs', 'Insufficient', 'Field 4', 'Crop 4', 'GPS4', '2023-05-18 11:00:00'),
    (5, 5, 5, '2023-05-20 11:20:00', 0.78, 28.8, 61.0, 'Moderate', 'None', 'Sufficient', 'Field 5', 'Crop 5', 'GPS5', '2023-05-20 11:50:00');

-- Insert data into the Soil table
INSERT INTO Soil (SoilID, FarmID, SoilType, pH, NutrientLevels)
VALUES
    (1, 1, 'Loam', 6.8, 'High Nitrogen, Medium Phosphorus'),
    (2, 2, 'Sandy', 6.2, 'Low Nitrogen, High Potassium'),
    (3, 3, 'Clay', 7.0, 'Medium Nitrogen, Medium Phosphorus'),
    (4, 4, 'Silt', 6.5, 'High Nitrogen, Low Phosphorus'),
    (5, 5, 'Loamy Sand', 6.3, 'Low Nitrogen, Medium Potassium');

-- Insert data into the Technicians table
INSERT INTO Technicians (TechnicianID, TechnicianName, ContactNumber)
VALUES
    (1, 'Technician 1', '111-111-1111'),
    (2, 'Technician 2', '222-222-2222'),
    (3, 'Technician 3', '333-333-3333'),
    (4, 'Technician 4', '444-444-4444'),
    (5, 'Technician 5', '555-555-5555');

-- Insert data into the IrrigationSchedule table
INSERT INTO IrrigationSchedule (ScheduleID, FieldID, CropID, Date, AmountToIrrigate)
VALUES
    (1, 1, 1, '2023-05-12', 25.5),
    (2, 2, 2, '2023-05-14', 30.0),
    (3, 3, 3, '2023-05-16', 22.8),
    (4, 4, 4, '2023-05-18', 28.3),
    (5, 5, 5, '2023-05-20', 35.7);

-- Insert data into the PestControlData table
INSERT INTO PestControlData (PestID, Datetime, Image, Coordinates, TemperatureDetected, Object)
VALUES
    (1, '2023-05-10 10:00:00', 'image1.jpg', 'POINT(35.1234 -120.5678)', 32.5, 'Pest 1'),
    (2, '2023-05-12 11:30:00', 'image2.jpg', 'POINT(35.6789 -120.9876)', 34.0, 'Pest 2'),
    (3, '2023-05-14 09:15:00', 'image3.jpg', 'POINT(35.4321 -120.8765)', 31.8, 'Pest 3'),
    (4, '2023-05-16 13:45:00', 'image4.jpg', 'POINT(35.9876 -120.3456)', 36.2, 'Pest 4'),
    (5, '2023-05-18 12:20:00', 'image5.jpg', 'POINT(35.8765 -120.6543)', 33.5, 'Pest 5');

-- Insert data into the FlightLog table
INSERT INTO FlightLog (Flight_ID, Field_ID, Flight_Date, Flight_Duration, Purpose)
VALUES
    (1, 1, '2023-05-10', '01:30:00', 'Crop Assessment'),
    (2, 2, '2023-05-12', '02:15:00', 'Pest Control'),
    (3, 3, '2023-05-14', '01:45:00', 'Irrigation Check'),
    (4, 4, '2023-05-16', '02:30:00', 'Crop Assessment'),
    (5, 5, '2023-05-18', '02:00:00', 'Pest Control');

-- Insert data into the Image table
INSERT INTO Image (Image_ID, Flight_ID, Image_File_Path, Capture_Date, Sensor_Type, Datetime)
VALUES
    (1, 1, 'image1.jpg', '2023-05-10', 'RGB', '2023-05-10 10:30:00'),
    (2, 2, 'image2.jpg', '2023-05-12', 'RGB', '2023-05-12 11:45:00'),
    (3, 3, 'image3.jpg', '2023-05-14', 'RGB', '2023-05-14 09:30:00'),
    (4, 4, 'image4.jpg', '2023-05-16', 'RGB', '2023-05-16 14:00:00'),
    (5, 5, 'image5.jpg', '2023-05-18', 'RGB', '2023-05-18 12:45:00');

-- Insert data into the Orthomosaic table
INSERT INTO Orthomosaic (Orthomosaic_ID, Flight_ID, Mosaic_File_Path, Processing_Date)
VALUES
    (1, 1, 'mosaic1.jpg', '2023-05-10'),
    (2, 2, 'mosaic2.jpg', '2023-05-12'),
    (3, 3, 'mosaic3.jpg', '2023-05-14'),
    (4, 4, 'mosaic4.jpg', '2023-05-16'),
    (5, 5, 'mosaic5.jpg', '2023-05-18');

-- Insert data into the ElevationData table
INSERT INTO ElevationData (Elevation_ID, Field_ID, Image_ID, Elevation_Values)
VALUES
    (1, 1, 1, 'Elevation data for Field 1, Image 1'),
    (2, 2, 2, 'Elevation data for Field 2, Image 2'),
    (3, 3, 3, 'Elevation data for Field 3, Image 3'),
    (4, 4, 4, 'Elevation data for Field 4, Image 4'),
    (5, 5, 5, 'Elevation data for Field 5, Image 5');

-- Insert data into the Users table
INSERT INTO Users (User_ID, First_Name, Last_Name, Username, Password, Role)
VALUES
    (1, 'John', 'Doe', 'johndoe', 'password1', 'Technician'),
    (2, 'Jane', 'Smith', 'janesmith', 'password2', 'Technician'),
    (3, 'Alice', 'Johnson', 'alicejohnson', 'password3', 'Farmer'),
    (4, 'Bob', 'Williams', 'bobwilliams', 'password4', 'Farmer'),
    (5, 'Admin', 'Adminson', 'admin', 'adminpassword', 'Admin');
go
Create view CropInformation
	AS
SELECT C.CropName,
    C.PlantingDate,
    C.HarvestDate,
    C.ExpectedYield,
    F.FarmName,
    F.Location
FROM Crops C
JOIN Farm F ON C.FarmID = F.FarmID;
go
CREATE VIEW TechnicianFlightLog AS
SELECT
    F.Flight_Date,
    F.Flight_Duration,
    F.Purpose,
    C.CropName,
    F.Field_ID
FROM FlightLog F
JOIN Crops C ON F.CropID = C.CropID;
go
CREATE VIEW FarmSoilInformation AS
SELECT
    F.FarmName,
    F.Location,
    S.SoilType,
    S.pH,
    S.NutrientLevels
FROM Farm F
JOIN Soil S ON F.FarmID = S.FarmID;
go
CREATE VIEW PestControlDataView AS
SELECT
    P.Datetime,
    P.TemperatureDetected,
    P.Object,
    C.CropName
FROM PestControlData P
JOIN Crops C ON P.CropID = C.CropID;
go
CREATE VIEW CropHealthSummary AS
SELECT
    CH.Timestamp,
    CH.NDVI,
    CH.DiseaseStatus,
    CH.PestStatus,
    C.CropName,
    CH.Field_Name
FROM CropHealthData CH
JOIN Crops C ON CH.CropID = C.CropID;