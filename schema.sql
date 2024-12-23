DROP DATABASE IF EXISTS arbre;
CREATE DATABASE arbre;
USE arbre;

CREATE TABLE Person (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    name VARCHAR(255) NOT NULL,         
    lastname VARCHAR(255) NOT NULL,     
    birthday DATE NULL,            
    deathday DATE NULL,                 
    CHECK (deathday >= birthday OR deathday IS NULL)  -- La date de décès doit venir après la date de naissance
);

CREATE TABLE Relationship (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    type VARCHAR(50) NOT NULL,           
    person_id INT,                      
    parent_id INT,                     
    FOREIGN KEY (person_id) REFERENCES Person(id) ON DELETE CASCADE,  
    FOREIGN KEY (parent_id) REFERENCES Person(id) ON DELETE CASCADE,  
    CHECK (type IN ('biologique', 'adoptif', 'beau-parent'))     
);

-- Trigger
DELIMITER $$

CREATE TRIGGER check_biological_parents
BEFORE INSERT ON Relationship
FOR EACH ROW
BEGIN
    IF NEW.type = 'biologique' THEN
        SET @parent_count = (
            SELECT COUNT(*)
            FROM Relationship
            WHERE person_id = NEW.person_id AND type = 'biologique'
        );
        IF @parent_count >= 2 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Une personne ne peut avoir que 2 parents biologiques maximum.';
        END IF;
    END IF;
END $$

DELIMITER ;


