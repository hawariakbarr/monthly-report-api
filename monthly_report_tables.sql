
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` tinyint(1) NOT NULL,
  `phoneNumber` varchar(200) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `master_bandwith`;
CREATE TABLE `master_bandwith` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bandwith` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `master_isp`;
CREATE TABLE `master_isp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `master_opd`;
CREATE TABLE `master_opd` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(500) NOT NULL,
  `address` varchar(500) NOT NULL,
  `pic` varchar(200) NOT NULL,
  `phone_number` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `master_uptd`;
CREATE TABLE `master_uptd` (
  `id` int NOT NULL AUTO_INCREMENT,
  `opd_id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `address` varchar(500) NOT NULL,
  `pic` varchar(200) NOT NULL,
  `phone_number` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `opd_link`;
CREATE TABLE `opd_link` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prtg_id` int DEFAULT NULL,
  `opd_id` int NOT NULL,
  `isp_id` int NOT NULL,
  `band_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `opd_id` (`opd_id`),
  KEY `isp_id` (`isp_id`),
  KEY `band_id` (`band_id`),
  KEY `id` (`id`),
  CONSTRAINT `opd_link_ibfk_1` FOREIGN KEY (`opd_id`) REFERENCES `master_opd` (`id`),
  CONSTRAINT `opd_link_ibfk_2` FOREIGN KEY (`isp_id`) REFERENCES `master_isp` (`id`),
  CONSTRAINT `opd_link_ibfk_3` FOREIGN KEY (`band_id`) REFERENCES `master_bandwith` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS `uptd_link`;
CREATE TABLE `uptd_link` (
  `id` int NOT NULL AUTO_INCREMENT,
  `prtg_id` int DEFAULT NULL,
  `uptd_id` int NOT NULL,
  `isp_id` int NOT NULL,
  `band_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uptd_id` (`uptd_id`),
  KEY `isp_id` (`isp_id`),
  KEY `band_id` (`band_id`),
  KEY `id` (`id`),
  CONSTRAINT `uptd_link_ibfk_1` FOREIGN KEY (`uptd_id`) REFERENCES `master_uptd` (`id`),
  CONSTRAINT `uptd_link_ibfk_2` FOREIGN KEY (`isp_id`) REFERENCES `master_isp` (`id`),
  CONSTRAINT `uptd_link_ibfk_3` FOREIGN KEY (`band_id`) REFERENCES `master_bandwith` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
------------------------------------------------------------------------------------------------