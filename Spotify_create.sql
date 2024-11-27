-- Drop existing database if it exists and create a new one
CREATE DATABASE IF NOT EXISTS Spotify;
USE Spotify;

-- Drop tables if they exist
DROP TABLE IF EXISTS compositor_song;
DROP TABLE IF EXISTS compositor_album;
DROP TABLE IF EXISTS playlist_item;
DROP TABLE IF EXISTS song;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS compositor;
DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS file_provider;
DROP TABLE IF EXISTS label;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS subscribition;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS album_log;

-- Drop triggers
DROP TRIGGER IF EXISTS before_album_insert;
DROP TRIGGER IF EXISTS before_genre_delete;
DROP TRIGGER IF EXISTS block_genre_insert;
DROP TRIGGER IF EXISTS restrict_genre_deletion;
DROP TRIGGER IF EXISTS logging_on_album_insertion;

-- Drop procedures
DROP PROCEDURE IF EXISTS insert_into_table;
DROP PROCEDURE IF EXISTS insert_compositor_album;
DROP PROCEDURE IF EXISTS insert_noname;
DROP PROCEDURE IF EXISTS column_aggregate_procedure;
DROP PROCEDURE IF EXISTS split_table_dynamic;


-- Create tables
CREATE TABLE album (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE file_provider (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(75) NOT NULL,
    is_trusted BOOL NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE file (
    id INT NOT NULL AUTO_INCREMENT,
    file_provider_id INT NOT NULL,
    stream VARCHAR(125) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (file_provider_id) REFERENCES file_provider(id)
);

CREATE TABLE song (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    duration TIME NOT NULL,
    likes_count INT NOT NULL,
    listen_count INT NOT NULL,
    album_id INT NOT NULL,
    file_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    genre VARCHAR(100) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (album_id) REFERENCES album(id),
    FOREIGN KEY (file_id) REFERENCES file(id)
);

CREATE TABLE label (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(75) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE compositor (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    label_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (label_id) REFERENCES label(id)
);

CREATE TABLE compositor_album (
    compositor_id INT NOT NULL,
    album_id INT NOT NULL,
    PRIMARY KEY (compositor_id, album_id),
    FOREIGN KEY (album_id) REFERENCES album(id),
    FOREIGN KEY (compositor_id) REFERENCES compositor(id)
);

CREATE TABLE compositor_song (
    compositor_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (compositor_id, song_id),
    FOREIGN KEY (compositor_id) REFERENCES compositor(id),
    FOREIGN KEY (song_id) REFERENCES song(id)
);

CREATE TABLE subscribition (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    price_for_month INT NOT NULL,
    price_for_year INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(250),
    phone_number VARCHAR(15) NOT NULL,
    subscribition INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (phone_number),
    FOREIGN KEY (subscribition) REFERENCES subscribition(id)
);

CREATE TABLE playlist_item (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    order_in_playlist INT NOT NULL,
    is_playing_now BOOL NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (song_id) REFERENCES song(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create indexes
CREATE INDEX idx_compositor_name ON compositor(name);
CREATE INDEX idx_album_name ON album(name);
CREATE INDEX idx_song_name ON song(name);
-- 2 more indexes to 2 lab
CREATE INDEX idx_playlist_user ON playlist_item(user_id);
CREATE INDEX idx_user_phone_number ON user(phone_number);

-- Create the new table
CREATE TABLE genre (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    PRIMARY KEY (id)
);

-- Update the album table to include a genre_id column
ALTER TABLE album
ADD COLUMN genre_id INT;

-- Create a trigger to ensure genre_id exists in the genre table before album insertion
DELIMITER $$
CREATE TRIGGER before_album_insert
BEFORE INSERT ON album
FOR EACH ROW
BEGIN
    DECLARE genre_exists INT;
    SELECT COUNT(*) INTO genre_exists FROM genre WHERE id = NEW.genre_id;
    IF genre_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid genre_id. Genre does not exist.';
    END IF;
END$$
DELIMITER ;

-- Create a trigger to prevent deletion of a genre if it is referenced by any album
DELIMITER $$
CREATE TRIGGER before_genre_delete
BEFORE DELETE ON genre
FOR EACH ROW
BEGIN
    DECLARE album_count INT;
    SELECT COUNT(*) INTO album_count FROM album WHERE genre_id = OLD.id;
    IF album_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete genre. Albums are associated with this genre.';
    END IF;
END$$
DELIMITER ;


-- TASK 2. PROCEDURES 
-- a) Procedure to insert new values to a table
DELIMITER $$
CREATE PROCEDURE insert_into_table(
	IN table_name VARCHAR(255),
	IN column_list VARCHAR(255),
	IN value_list VARCHAR(255)
)
BEGIN
	SET @sql = CONCAT('INSERT INTO ', table_name, ' (', column_list, ')
		VALUES (', value_list, ')');
	SELECT @sql AS generated_sql;
	PREPARE stmt FROM @sql;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
END $$
DELIMITER ;


-- Procedure to insert into M:M table
DELIMITER $$
CREATE PROCEDURE insert_compositor_album(IN compositor_name VARCHAR(50), IN album_name VARCHAR(50))
BEGIN
    DECLARE compositor_id INT;
    DECLARE album_id INT;

    SELECT id INTO compositor_id FROM compositor WHERE name = compositor_name;
    SELECT id INTO album_id FROM album WHERE name = album_name;

    IF compositor_id IS NULL OR album_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid compositor or song name.';
    ELSE
        INSERT INTO compositor_album (compositor_id, album_id) VALUES (compositor_id, album_id);
    END IF;
END$$
DELIMITER ;


-- Procedure insert 10 nonames
DELIMITER $$
CREATE PROCEDURE insert_noname(IN table_name VARCHAR(255))
BEGIN
    DECLARE i INT DEFAULT 1;

    WHILE i <= 10 DO
        SET @sql = CONCAT('INSERT INTO ', table_name, ' (name) VALUES (''Noname', i, ''')');
        SELECT @sql AS generated_sql; -- Optional: Debugging line to view generated SQL
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

-- Max/min/sum/avarage

DELIMITER $$
CREATE PROCEDURE column_aggregate_procedure(
    IN table_name VARCHAR(50), 
    IN column_name VARCHAR(50), 
    IN operation VARCHAR(10)
)
BEGIN
    SET @query = CONCAT('SELECT ', operation, '(', column_name, ') AS result FROM ', table_name);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$
DELIMITER ;

-- Random copy of album table

DELIMITER $$
CREATE PROCEDURE split_table_dynamic()
BEGIN
    DECLARE row_count INT;
    DECLARE current_id INT;
    DECLARE done INT DEFAULT 0;

    DECLARE cur CURSOR FOR SELECT id FROM album;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    SET @table1 = CONCAT('album_copy_1_', UNIX_TIMESTAMP());
    SET @table2 = CONCAT('album_copy_2_', UNIX_TIMESTAMP());

    SET @create_query = CONCAT('CREATE TABLE ', @table1, ' LIKE album');
    PREPARE stmt FROM @create_query;
    EXECUTE stmt;

    SET @create_query = CONCAT('CREATE TABLE ', @table2, ' LIKE album');
    PREPARE stmt FROM @create_query;
    EXECUTE stmt;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO current_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @random_table = IF(RAND() < 0.5, @table1, @table2);
        SET @insert_query = CONCAT('INSERT INTO ', @random_table, ' SELECT * FROM album WHERE id = ', current_id);
        PREPARE stmt FROM @insert_query;
        EXECUTE stmt;
    END LOOP;

    CLOSE cur;
END$$
DELIMITER ;

-- TRIGGERS. 1) Restrict any insertions on genre table

DELIMITER $$
CREATE TRIGGER block_genre_insert
BEFORE INSERT ON genre
FOR EACH ROW
BEGIN
	SIGNAL SQLSTATE "45000" SET MESSAGE_TEXT = 'Unable to insert to genre directly. Please disable block_genre_insert trigger and try again.';
END$$
DELIMITER ;


-- 2) Restrict deletion in genre table
DELIMITER $$
CREATE TRIGGER restrict_genre_deletion
BEFORE DELETE ON genre
FOR EACH ROW
BEGIN
	SIGNAL SQLSTATE "45000" SET MESSAGE_TEXT = 'Unable to delete in genre. Please disable restrict_genre_deletion trigger and try again.';
END $$
DELIMITER ;

-- 3) Logging on album update
CREATE TABLE IF NOT EXISTS album_log (
	id INT NOT NULL AUTO_INCREMENT,
    action_time TIMESTAMP NOT NULL,
    executed_action VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

DELIMITER $$
CREATE TRIGGER logging_on_album_insertion
AFTER UPDATE ON album
FOR EACH ROW
BEGIN
	DECLARE comment VARCHAR(255);
    
    SET comment = CONCAT("Changed name from ", OLD.name, " to ", NEW.name); 
    
    INSERT album_log(
		executed_action
    ) VALUES (
        comment
    );
END $$
DELIMITER ;









