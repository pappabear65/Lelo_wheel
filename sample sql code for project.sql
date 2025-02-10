/* to start a multi line comment
   then use this to end the multi line comment */
   
-- typically used when you want a quick note or after a piece of code.  a new line terminates the double dash.

-- manualy create a table with a primary key:

CREATE TABLE Lelo (
	id MEDIUMINT NOT NULL AUTO_INCREMENT, -- sets a column named id to auto increment when new data added
	entryDate CHAR(30) NOT NULL, -- sets a new column with the name 'todaysDate'
	entryTime CHAR(30) NOT NULL,
	temperature INTEGER NOT NULL,
	PRIMARY KEY (id) -- sets the column 'id' as the primary key
); -- end of table creation, comma is a end of line indication, the semicolon is the end of the action.

-- manualy add data to table

INSERT INTO Lelo (entryDate, entryTime, temperature) VALUES -- identifies which row 'id' and which columns data will be inserted
		('2025/01/21', '08:30:00', 23.9), -- first line of data, note that the data is in the same order as used in the insert line
		('2025/01/21', '12:30:00', 29.9),
		('2025/01/21', '20:30:00', 23.9),
		('2025/01/22', '08:30:00', 23.9),
		('2025/01/22', '12:30:00', 29.9),
		('2025/01/22', '20:30:00', 23.9); -- has inserted 18 pieces of data into six rows
		

###### build table for lelo wheel		
CREATE TABLE wheelData (
	id MEDIUMINT NOT NULL AUTO_INCREMENT, -- sets a column named id to auto increment when new data added
    reedIdForFileWrite CHAR(30),
	entryDate DATE,
	entryTime TIME,
	systemStatusForFileWrite CHAR(30),
	sessionCounter INTEGER(12) NOT NULL,
	reed1SessionRotationCounter INTEGER(12) NOT NULL,
	reed2SessionRotationCounter INTEGER(12) NOT NULL,
	sessionRotationDirection  CHAR(30),
	reed1TriggerTime INTEGER(12) NOT NULL,
	reed1TriggerTimeLast INTEGER(12) NOT NULL,
	reed1TriggerTimeDifference INTEGER(12) NOT NULL,
	reed2TriggerTime INTEGER(12) NOT NULL,
	reed2TriggerTimeLast INTEGER(12) NOT NULL,
	speedMetersPerSecond DECIMAL(5,3),
	distanceRunInSession DECIMAL(5,3),
	PRIMARY KEY (id) -- sets the column 'id' as the primary key	
);	
	
INSERT INTO wheelData (reedIdForFileWrite, entryDate, entryTime, systemStatusForFileWrite, sessionCounter, reed1SessionRotationCounter, reed2SessionRotationCounter, sessionRotationDirection, reed1TriggerTime, reed1TriggerTimeLast, reed1TriggerTimeDifference, reed2TriggerTime, reed2TriggerTimeLast, speedMetersPerSecond, distanceRunInSession) VALUES
	("reed 2", "2025/01/14", "10:58:46", "in session", "6", "16", "18", "cw", "65774017", "65773585", "432", "65774366", "65773938", "1.991", "13.76"),
	("reed 1", "2025/01/14", "10:58:46", "in session", "6", "17", "18", "cw", "65774445", "65774017", "432", "65774366", "65773938", "1.991", "13.76");
	
	
###### JSON export from sql database

[
{"type":"header","version":"5.2.1","comment":"Export to JSON plugin for PHPMyAdmin"},
{"type":"database","name":"Lelo"},
{"type":"table","name":"wheelData","database":"Lelo","data":
[
{"id":"1","reedIdForFileWrite":"reed 2","entryDate":"2025-01-14","entryTime":"10:58:46","systemStatusForFileWrite":"in session","sessionCounter":"6","reed1SessionRotationCounter":"16","reed2SessionRotationCounter":"18","sessionRotationDirection":"cw","reed1TriggerTime":"65774017","reed1TriggerTimeLast":"65773585","reed1TriggerTimeDifference":"432","reed2TriggerTime":"65774366","reed2TriggerTimeLast":"65773938","speedMetersPerSecond":"1.991","distanceRunInSession":"13.760"},
{"id":"2","reedIdForFileWrite":"reed 1","entryDate":"2025-01-14","entryTime":"10:58:46","systemStatusForFileWrite":"in session","sessionCounter":"6","reed1SessionRotationCounter":"17","reed2SessionRotationCounter":"18","sessionRotationDirection":"cw","reed1TriggerTime":"65774445","reed1TriggerTimeLast":"65774017","reed1TriggerTimeDifference":"432","reed2TriggerTime":"65774366","reed2TriggerTimeLast":"65773938","speedMetersPerSecond":"1.991","distanceRunInSession":"13.760"}
]
}
]
	
	