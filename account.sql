-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jun 12, 2020 at 02:17 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- START TRANSACTION;
-- SET time_zone = "+00:00";


-- /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
-- /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
-- /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
-- /*!40101 SET NAMES utf8mb4 */;

--
-- Database: `account`
--
CREATE DATABASE IF NOT EXISTS `account` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `account`;

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `AID` int(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` int(8) NOT NULL,
  `email` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`AID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`name`, `password`, `phone`, `email`, `address`) VALUES
('Winnie', 'ILOVEHONEY', 999, "winnie@gmail.com", "81 Victoria St, Singapore 188065"),
('Mary', 'WHERESMYLAMB', 911, "mary@gmail.com", "81 Victoria St, Singapore 188065"),
('Luke', 'NOTMYFATHER', 995, "luke@gmail.com", "81 Victoria St, Singapore 188065"),
('Tom', 'GETMEJERRY', 118, "tom@gmail.com", "81 Victoria St, Singapore 188065"),
('Jerry', 'TOMISSTUPID', 110, "jerry@gmail.com", "81 Victoria St, Singapore 188065"),
('John', 'AVERAGEJOE', 123, "esmg4t5@gmail.com", "81 Victoria St, Singapore 188065"),
('Alice', 'ILOVEWONDERLAND', 456, "alice@gmail.com", "81 Victoria St, Singapore 188065"),
('Bob', 'ESM', 789, "bob@gmail.com", "81 Victoria St, Singapore 188065"),
('Beth', 'ESM', 101, "beth@gmail.com", "81 Victoria St, Singapore 188065"),
('Nelson', 'AVERAGEJOE', 111, "nelson@gmail.com", "81 Victoria St, Singapore 188065")
;

-- --------------------------------------------------------


-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
