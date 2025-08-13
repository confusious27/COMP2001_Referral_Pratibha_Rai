CREATE SCHEMA CW2;

/*Trail Table*/
CREATE TABLE CW2.[Trail] (
    Trail_ID INT IDENTITY(1,1) PRIMARY KEY,
    TrailName VARCHAR(255) NOT NULL,
    Rating DECIMAL(2,1) CHECK (Rating >= 0.0 AND Rating <= 5.0),
    Difficulty VARCHAR(10) NOT NULL CHECK (Difficulty IN ('Easy', 'Moderate', 'Hard')),
    Location VARCHAR(255) NOT NULL,
    Distance DECIMAL(5,1) CHECK (Distance > 0),
    EstimatedTime VARCHAR(20),
    ElevationGain INT,
    TrailType VARCHAR(15) CHECK (TrailType IN ('Loop', 'Out and Back', 'Point to Point')),
    Description VARCHAR(500)
);

/*Data*/
INSERT INTO CW2.[Trail] (TrailName, Rating, Difficulty, Location, Distance, EstimatedTime, ElevationGain, TrailType, Description) VALUES
('Plymbridge Circular', 4.7, 'Easy', 'Plymouth, Devon, England', 5, '1h 23m', 147, 'Loop', 'This is a gentle circular walk through ancient oak woodlands, beside the beautiful River Plym. Within the woods are remains of the area’s industrial past and there are breathtaking views across the valley from the viaduct. Along the way you may see kingfishers, sea trout, dippers, peregrine falcon, deer and other wildlife.'),
('Wembury to Heybrook Bay via the South West Coast Path', 4.1, 'Moderate', 'South Devon National Landscape (AONB)', 7.1, '1h 29m', 69, 'Out and Back', 'This is a great walk along the coastline between Wembury and Heybrook Bay via the South West Coast Path, offering varied scenery along the way and gorgeous views of the sea crashing and lapping on the many types of rock formations.'),
('South West Coast Path: Lynmouth to Combe Martin', 4.7, 'Hard', 'Exmoor National Park', 22, '7h 44m', 1103, 'Point to Point', 'This section of the route involves a couple of challenging climbs and a visit to the highest point along the South West Coast Path, where you’re rewarded for the effort with spectacular views all around. You will have stunning ocean views throughout your journey and may even see a variety of wildlife.');

SELECT * FROM CW2.Trail;

/*User Table*/
CREATE TABLE CW2.[User] (
    User_ID INT IDENTITY(1,1) PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Role VARCHAR(5) CHECK (Role IN ('User', 'Admin'))
);

/*Data*/
INSERT INTO CW2.[User] (Email, Role) VALUES
('grace@plymouth.ac.uk', 'Admin'),
('tim@plymouth.ac.uk', 'User'),
('ada@plymouth.ac.uk', 'User');

-- SELECT * FROM CW2.[User];

/*Comment Table*/
CREATE TABLE CW2.[Comment] (
Comment_ID INT IDENTITY(1,1) PRIMARY KEY,
Trail_ID INT FOREIGN KEY REFERENCES CW2.[Trail](Trail_ID),
User_ID INT FOREIGN KEY REFERENCES CW2.[User](User_ID),
Content VARCHAR(500),
CreatedOn DATETIME DEFAULT DATETIME(), --so I don't need to keep making time and date for new comments apart from sample data
IsArchived BIT
);

/*Data*/
INSERT INTO CW2.[Comment] (Trail_ID, User_ID, Content, CreatedOn, IsArchived) VALUES
(1, 2, 'Great trail, lovely views!', '2025-08-01 13:00:00', 0),
(1, 3, 'Nice and easy. Good for a Sunday walk.', '2025-07-31 17:04:42', 0),
(2, 2, 'Stunning views of the sea!', '2024-06-30 16:45:02', 0),
(3, 1, 'Very challenging! Make sure to bring water!', '2025-04-29 19:23:32', 1);

-- SELECT * FROM CW2.Comment;



/*Trail Details with Comments View*/
CREATE VIEW CW2.TrailWithCommentsView AS
SELECT
    T.Trail_ID,
    T.TrailName,
    T.Rating,
    T.Difficulty,
    T.Location,
    T.Distance,
    T.EstimatedTime,
    T.ElevationGain,
    T.TrailType,
    T.Description,
    C.Comment_ID,
    C.Content AS CommentContent,
    C.CreatedOn,
    U.Email AS CommenterEmail,
    C.IsArchived
FROM CW2.[Trail] T
LEFT JOIN CW2.[Comment] C ON T.Trail_ID = C.Trail_ID AND C.IsArchived = 0 /*to ensure that only unarchived comments can be seen*/
LEFT JOIN CW2.[User] U ON C.USER_ID = U.USER_ID;

-- SELECT * FROM CW2.TrailWithCommentsView;



--CREATE
CREATE PROCEDURE CW2.InsertComment
    @Trail_ID INT,
    @User_ID INT,
    @Content VARCHAR(500),
    @CreatedOn DATETIME,
    @IsArchived BIT
AS
BEGIN
    --checks if the trail ID or the user ID exists
    IF EXISTS (SELECT 1 FROM CW2.[User] WHERE USER_ID = @User_ID)
        AND EXISTS (SELECT 1 FROM CW2.[Trail] WHERE Trail_ID = @Trail_ID)
    BEGIN
        INSERT INTO CW2.[Comment] (Trail_ID, User_ID, Content, CreatedOn, IsArchived)
        VALUES (@Trail_ID, @User_ID, @Content, @CreatedOn, @IsArchived);
    END
    ELSE
    BEGIN
        RAISERROR ('Invalid Trail ID or User ID', 16, 1);
    END
END;

/*Data*/
-- EXEC CW2.InsertComment '3', '2', 'Make sure to research thoroughly and familiarise yourself with the route before you attempt.', '2024-12-04 23:04:49', '0';


--READ
CREATE PROCEDURE CW2.GetActiveComments
AS
BEGIN
    --get only unarchived comments
    SELECT * FROM CW2.[Comment]
    WHERE IsArchived = 0;
END;

-- EXEC CW2.GetActiveComments;


--UPDATE
CREATE PROCEDURE CW2.UpdateComment
    @Comment_ID INT,
    @User_ID INT,
    @Content VARCHAR(500),
    @IsArchived BIT
AS
BEGIN
    --checking the comment exists and is being updated by the user who wrote the comment
    IF EXISTS (
        SELECT 1 FROM CW2.[Comment]
        WHERE Comment_ID = @Comment_ID AND User_ID = @User_ID
    )
    BEGIN
        UPDATE CW2.[Comment]
        SET Content = @Content,
            IsArchived = @IsArchived
     WHERE Comment_ID = @Comment_ID;
    END;
    ELSE
    BEGIN
     RAISERROR ('Comment does not exist or you are not the owner.', 16, 1);
    END
END;

-- EXEC CW2.UpdateComment '2', '3', 'Nice and easy. Good for an evening stroll.', '0';

--DELETE (Archive)
CREATE PROCEDURE CW2.ArchiveComment(@Comment_ID INT, @User_ID INT)
AS
BEGIN
    --To check user's role
    IF EXISTS (
        SELECT 1
        FROM CW2.[User]
        WHERE User_ID = @User_ID AND Role = 'Admin'
    )
    BEGIN
        UPDATE CW2.[Comment]
        SET IsArchived = 1
        WHERE Comment_ID = @Comment_ID;
    END;
    --If user isn't admin
    ELSE
    BEGIN
        RAISERROR ('Only an admin can delete comments', 16, 1);
    END
END;

--non-admin
-- EXEC CW2.ArchiveComment '2', '2';
--admin
-- EXEC CW2.ArchiveComment '2', '1';


/*Trigger Exercise*/
CREATE TABLE CW2.AddNewTrail (
    Log_ID INT IDENTITY(1,1) PRIMARY KEY,
    Trail_ID INT FOREIGN KEY REFERENCES CW2.[Trail](Trail_ID),
    User_ID INT FOREIGN KEY REFERENCES CW2.[User](User_ID),
    CreatedOn DATETIME DEFAULT GETDATE()
);

--need to modify to know who added the trail for this
ALTER TABLE CW2.Trail
ADD AddedBy INT FOREIGN KEY REFERENCES CW2.[User](User_ID);


CREATE TRIGGER CW2.LogNewTrail
ON CW2.Trail
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON; /*so no row affected pops up for this trigger*/

    INSERT INTO CW2.AddNewTrail (Trail_ID, User_ID, CreatedOn)
    SELECT i.Trail_ID, i.AddedBy, GETDATE()
    FROM INSERTED i;
END;


--testing
-- INSERT INTO CW2.Trail (TrailName, Rating, Difficulty, Location, Distance, EstimatedTime, ElevationGain, TrailType, Description, AddedBy) VALUES
-- ('Cadover Bridge to Shaugh Bridge Circular', 4.7, 'Moderate', 'Dartmoor National Park', 7.2, '2h 3m', 222, 'Loop', 'This is a wonderful trail in Dartmoor National Park that takes you through the woodland valley and up Dewerstone Rock.', 1);

-- SELECT * FROM CW2.AddNewTrail;
