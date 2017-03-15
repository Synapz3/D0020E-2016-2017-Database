INSERT INTO d0020e.users (firstName, lastName, socialSecurityNr, userPassword) VALUES ("Testnamn", "TestEfternamn", 1111111111,
"testPassword");

INSERT INTO d0020e.checklist (type) VALUES ("handskar");

INSERT INTO d0020e.area (x, y, z, width, depth, height, checklistID) VALUES (1,1,1,1000,1000,1000,1);

INSERT INTO d0020e.task (checklistID, description, userID, title, areaID) VALUES (1, "Exempelbeskrivning", 1, "Exempeltitel", 1);

INSERT INTO d0020e.equipment (macAddress, serialNumber, type, visualNumber) VALUES ("here", "spelar ingen roll", "handskar", 1);

INSERT INTO d0020e.subtasks (taskID, subtasktitle, subtaskdescription) VALUES (1, "Deluppdrag 1", "Exempeltext");

INSERT INTO d0020e.subtasks (taskID, subtasktitle, subtaskdescription) VALUES (1, "Deluppdrag 2", "Exempeltext");