CREATE SCHEMA IF NOT EXISTS `panels`;
USE `panels` ;

DROP TABLE IF EXISTS `supermarket`;
DROP TABLE IF EXISTS `section`;
DROP TABLE IF EXISTS `advertisement_panel`;
DROP TABLE IF EXISTS `sensor`;

CREATE TABLE `supermarket` (
    `id` INT NOT NULL AUTO_INCREMENT,
  `supermarket_name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE = InnoDB;

CREATE TABLE `section` (
    `id` INT NOT NULL AUTO_INCREMENT,
  `supermarket_id` INT NOT NULL,
  `section_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE = InnoDB;

CREATE TABLE `advertisement_panel` (
    `id` INT NOT NULL AUTO_INCREMENT,
  `section_id` INT NOT NULL,
  `producer_name` VARCHAR(90) NOT NULL,
  `height` INT NOT NULL,
  `width` INT NOT NULL,
  `material_name` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE = InnoDB;

CREATE TABLE `sensor` (
    `id` INT NOT NULL AUTO_INCREMENT,
  `sensor_type` VARCHAR(90) NOT NULL,
  `report_time` VARCHAR(90) NOT NULL,
  `people_walked` FLOAT NOT NULL,
  `avg_time_near_panel` FLOAT NOT NULL,
  PRIMARY KEY (`id`)
  ) ENGINE = InnoDB;

INSERT INTO `sensor`(sensor_type, report_time, people_walked, avg_time_near_panel) VALUES
  ('rest', '2021-11-23 24:04:58', 6, 0.5),
  ('rest', '2021-11-23 24:04:59', 3, 0.4),
  ('mqtt', '2021-11-23 24:04:53', 12, 0.1),
  ('mqtt', '2021-11-23 24:04:52', 9, 1);

INSERT INTO `supermarket`(supermarket_name, address) VALUES
	('Silpo', 'Soborna Square, 15, Lviv, Lviv Oblast, 79000'),
    ('ATB', 'Oleksandra Polia Ave, 7, Dnipro, Dnipropetrovsk Oblast, 49000'),
    ('Rukavichka', 'Horodotska St, 76, Lviv, Lviv Oblast, 79016'),
    ('Novus', 'Druzhby Narodiv Blvd, 16А, Kyiv, 02000');

INSERT INTO `section`(supermarket_id, section_name) VALUES
    (1, 'Grocery Section'),
    (1, 'Meat Section'),
    (1, 'Bakery Section'),
    (2, 'Home Utilities Section'),
    (2, 'Clothes Section'),
    (2, 'Bakery Section'),
    (3, 'Grocery Section'),
    (3, 'Meat Section'),
    (3, 'Clothes Section'),
    (4, 'Grocery Section'),
    (4, 'Home Utilities Section'),
    (4, 'Kid Games Section');

INSERT INTO `advertisement_panel`(section_id, producer_name, height, width, material_name) VALUES
	(1, 'BestPanels', 9, 15, 'Steel'),
    (2, 'PanelOff', 8, 12, 'Plastic'),
    (3, 'MyAdvertisement', 6, 13, 'Steel'),
    (4, 'BestPanels', 9, 15, 'Plastic'),
    (5, 'PanelOff', 7, 10, 'Steel'),
    (6, 'MyAdvertisement', 5, 9, 'Plastic'),
    (7, 'PanelOff', 8, 12, 'Steel'),
    (8, 'MyAdvertisement', 18, 30, 'Plastic'),
    (9, 'BestPanels', 10, 15, 'Steel'),
    (10, 'MyAdvertisement', 9, 13, 'Plastic'),
    (11, 'PanelOff', 7, 12, 'Steel'),
    (12, 'BestPanels', 8, 14, 'Plastic');

