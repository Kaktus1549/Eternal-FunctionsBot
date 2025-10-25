CREATE DATABASE IF NOT EXISTS EternalGaming;
USE EternalGaming;

-- Main db stuff
CREATE TABLE Role (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  FullName VARCHAR(100) NOT NULL,
  ShortName VARCHAR(50) NOT NULL UNIQUE,
  LogActivity BIT NOT NULL DEFAULT TRUE
);

CREATE TABLE Player (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  RoleId INT NULL,
  Username VARCHAR(50) NOT NULL UNIQUE,
  UserId VARCHAR(100) NOT NULL UNIQUE,
  DiscordId BIGINT UNSIGNED NULL DEFAULT(NULL),
  FOREIGN KEY (RoleId) REFERENCES Role(Id),
  CHECK (UserId REGEXP '.+@.+')
);

CREATE TABLE ModerationLog (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  PlayerId INT NOT NULL,
  IssuerId INT NOT NULL,
  ModerationType ENUM('kick','warn','ban','mute') NOT NULL,
  Reason VARCHAR(255) NOT NULL,
  StartDate DATETIME NOT NULL,
  EndDate DATETIME NULL,
  Data VARCHAR(50) NOT NULL,
  Revoked BIT NOT NULL DEFAULT FALSE,
  FOREIGN KEY (PlayerId) REFERENCES Player(Id),
  FOREIGN KEY (IssuerId) REFERENCES Player(Id)
);

CREATE TABLE Activity (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  PlayerId INT NOT NULL,
  TimeOnServerSeconds INT NOT NULL DEFAULT 0,
  FOREIGN KEY (PlayerId) REFERENCES Player(Id)
);

-- Vip stuff
CREATE TABLE VipRole (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  Role_Id INT NOT NULL,
  Name VARCHAR(50) NOT NULL UNIQUE, 
  DefaultHumanSpawns INT NOT NULL,         
  DefaultScpSpawns INT NOT NULL,
  FOREIGN KEY(Role_Id) REFERENCES Role(Id)
);

CREATE TABLE VipAssignment (
  Id INT AUTO_INCREMENT PRIMARY KEY,
  PlayerId INT NOT NULL,
  VipRoleId INT NOT NULL,
  SpawnHumanCount INT NULL,           
  SpawnScpCount INT NULL,       
  AssignedAt  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (PlayerId)  REFERENCES Player(Id),
  FOREIGN KEY (VipRoleId) REFERENCES VipRole(Id)
);

-- Reset default assignments
DELIMITER $$
CREATE TRIGGER trg_VipAssignment_SetDefaults
BEFORE INSERT ON VipAssignment
FOR EACH ROW
BEGIN
  IF NEW.SpawnHumanCount IS NULL THEN
    SET NEW.SpawnHumanCount = (
      SELECT DefaultHumanSpawns
        FROM VipRole
       WHERE Id = NEW.VipRoleId
    );
  END IF;

  IF NEW.SpawnScpCount IS NULL THEN
    SET NEW.SpawnScpCount = (
      SELECT DefaultScpSpawns
        FROM VipRole
       WHERE Id = NEW.VipRoleId
    );
  END IF;
END$$
DELIMITER ;

INSERT INTO Role(FullName,ShortName,LogActivity) VALUES
('Plugin QA', 'qa', 0),
('Discord Booster', 'db', 0),
('Kontributor', 'ko', 0),
('Donátor', 'do', 0),
('Sponzor', 'sp', 0),
('Zkušební RP host', 'zrph', 1),
('Junior RP host', 'jrph', 1),
('RP host', 'rph', 1),
('Starší RP host', 'srph', 1),
('Hlavní RP host', 'hrph', 1),
('Zkušební Moderátor', 'zm', 1),
('Moderátor', 'm', 1),
('Administrátor', 'a', 1),
('Starší Administrátor', 'sa', 1),
('Hlavní Administrátor', 'ha', 1),
('Development', 'd', 1),
('Správce', 's', 1),
('Rada', 'r', 1),
('Komunitní Majitel', 'km', 1);

INSERT INTO VipRole (Name, DefaultHumanSpawns, DefaultScpSpawns, Role_Id) VALUES
  ('Kontributor', 1, 1, (SELECT Id FROM Role WHERE ShortName = 'ko')), 
  ('Donátor', 3, 1, (SELECT Id FROM Role WHERE ShortName = 'do')),  
  ('Sponzor', 5, 3, (SELECT Id FROM Role WHERE ShortName = 'sp')); 
  
  -- Procedures
  DELIMITER $$
CREATE PROCEDURE AddPlayerIfNotExists(
  IN in_username VARCHAR(50),
  IN in_userid VARCHAR(100),
  OUT out_playerId INT
)
BEGIN
  SELECT Id
    INTO out_playerId
    FROM Player
   WHERE Username = in_username
      OR UserId = in_userid
   LIMIT 1;

  IF out_playerId IS NULL THEN
    INSERT INTO Player (Username, UserId)
         VALUES (in_username, in_userid);
    SET out_playerId = LAST_INSERT_ID();
  END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddActivityTime(
  IN in_userid VARCHAR(100),
  IN in_toadd_seconds INT
)
BEGIN
  DECLARE v_playerId INT;
  DECLARE v_count INT;

  -- look up the player
  SELECT Id
    INTO v_playerId
    FROM Player
   WHERE UserId = in_userid
   LIMIT 1;

  -- if no such player, abort
  IF v_playerId IS NULL THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Player not found';
  END IF;

  -- see if an Activity row already exists
  SELECT COUNT(*)
    INTO v_count
    FROM Activity
   WHERE PlayerId = v_playerId;

  IF v_count > 0 THEN
    -- already have activity then increment it
    UPDATE Activity
       SET TimeOnServerSeconds = TimeOnServerSeconds + in_toadd_seconds
     WHERE PlayerId = v_playerId;
  ELSE
    -- no activity row yet then create one
    INSERT INTO Activity (PlayerId, TimeOnServerSeconds)
         VALUES (v_playerId, in_toadd_seconds);
  END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE AddModerationLog(
  IN in_playerUserId VARCHAR(64),
  IN in_issuerUserId VARCHAR(64),
  IN in_modType ENUM('kick','warn','ban','mute'),
  IN in_reason VARCHAR(255),
  IN in_startDate DATETIME,
  IN in_endDate DATETIME,
  IN in_data VARCHAR(50)
)
BEGIN
  DECLARE v_playerId INT;
  DECLARE v_issuerId INT;

  -- Resolve PlayerId
  SELECT Id INTO v_playerId FROM Player WHERE UserId = in_playerUserId LIMIT 1;
  IF v_playerId IS NULL THEN 
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Target player not found';
  END IF;

  -- Resolve IssuerId
  SELECT Id INTO v_issuerId FROM Player WHERE UserId = in_issuerUserId LIMIT 1;
  IF v_issuerId IS NULL THEN 
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Issuer player not found';
  END IF;

  INSERT INTO ModerationLog (PlayerId, IssuerId, ModerationType, Reason, StartDate, EndDate, Data)
  VALUES (v_playerId, v_issuerId, in_modType, in_reason, in_startDate, in_endDate, in_data);
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE GetModerationLogsByUserId(
  IN in_userid VARCHAR(100)
)
BEGIN
  DECLARE v_playerId INT;

  -- look up the player
  SELECT Id
    INTO v_playerId
    FROM Player
   WHERE UserId = in_userid
   LIMIT 1;

  -- if no such player, signal an error
  IF v_playerId IS NULL THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Player not found';
  END IF;

  -- return all moderation logs for that player
  SELECT
    Id,
    ModerationType,
    Reason,
    StartDate,
    EndDate,
    Data,
    Revoked
  FROM ModerationLog
  WHERE PlayerId = v_playerId;
END$$
DELIMITER ;

SET GLOBAL event_scheduler = ON;

DELIMITER $$

-- Reset all VIP advantages daily at 00:00
CREATE EVENT IF NOT EXISTS ResetVipAdvantages
ON SCHEDULE
  EVERY 1 DAY
  STARTS CONCAT(CURDATE() + INTERVAL 1 DAY, ' 00:00:00')
DO
BEGIN
  UPDATE VipAssignment AS va
  JOIN VipRole       AS vr ON va.VipRoleId = vr.Id
  SET
    va.SpawnHumanCount = vr.DefaultHumanSpawns,
    va.SpawnScpCount   = vr.DefaultScpSpawns;
END$$

DELIMITER ;


CREATE USER 'ServerAccessLogin'@'%' IDENTIFIED BY 'EternalGaming1!';

GRANT 
    CREATE, ALTER, DROP,
    SELECT, INSERT, UPDATE, DELETE,
    EXECUTE,
    TRIGGER,
    CREATE ROUTINE, ALTER ROUTINE
  ON `EternalGaming`.* 
  TO 'ServerAccessLogin'@'%';

FLUSH PRIVILEGES;