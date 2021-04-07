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
-- Database: `preorder`
--
CREATE DATABASE IF NOT EXISTS `preorder` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `preorder`;

-- --------------------------------------------------------

--
-- Table structure for table `preorder`
--

DROP TABLE IF EXISTS `preorder`;
CREATE TABLE IF NOT EXISTS `preorder` (
  `POID` int(3) NOT NULL AUTO_INCREMENT,
  `AID` int(3) NOT NULL,
  `product_name` varchar(64) NOT NULL,
  `quantity` int(3) NOT NULL,
  `payment_status` varchar(64) NOT NULL,
  `total_price` int(3) NOT NULL,
  `address` varchar(64) NOT NULL,
  `datetime` datetime NOT NULL ,
  PRIMARY KEY (`POID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `preorder`
--

-- INSERT INTO `preorder` (`AID`, `product_name`, `quantity`, `payment_status`, `total_price`, `address`, `datetime`) VALUES
-- (001, "Nike Free RN Flyknit","10", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (002, "Nike Airmax","4", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (003, "Nike Free RN Flyknit","6", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (004, "Nike Airmax","1", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (005, "Nike Free RN Flyknit","2", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (006, "Nike Airmax","1", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (007, "Nike Free RN Flyknit","8", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (008, "Nike Airforce 1 Low Carhartt WIP Ale Brown","1", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (009, "Nike Free RN Flyknit","6", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (010, "Nike Airforce 1 Low Carhartt WIP Ale Brown","1", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (011, "Nike Free RN Flyknit","3", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (012, "Nike Airforce 1 Low Carhartt WIP Ale Brown","1", 'Paid', 50, '123 lala land', "2020-01-13"),
-- (013, "Nike Free RN Flyknit","2", 'Paid', 50, '123 lala land', "2020-01-13")
-- ;

-- --------------------------------------------------------


-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
