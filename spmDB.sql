-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 27, 2021 at 08:33 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


CREATE DATABASE IF NOT EXISTS `spmDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `spmDB`;

-- --------------------------------------------------------

--
-- Table structure for table `skill`
--

DROP TABLE IF EXISTS `skill`;
CREATE TABLE `skill` (
  `id` int(11) NOT NULL,
  `skill_desc` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `skill`
--

INSERT INTO `skill` (`id`, `skill_desc`) VALUES
(111, 'sales'),
(222, 'marketing'),
(333, 'project management');

-- --------------------------------------------------------

--
-- Table structure for table `desired_position`
--

DROP TABLE IF EXISTS `desired_position`;
CREATE TABLE `desired_position` (
  `id` int(11) NOT NULL,
  `position_name` varchar(50) DEFAULT NULL,
  `position_desc` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `desired_position`
--

INSERT INTO `desired_position` (`id`, `position_name`, `position_desc`) VALUES
(8764, 'Account Manager', 'sell sell sell'),
(2983, 'Marketing Assistant', 'market to the market');


-- --------------------------------------------------------
--
-- Table structure for table `dposition_skill`
--

DROP TABLE IF EXISTS `dposition_skill`;
CREATE TABLE `dposition_skill` (
  `position_id` int(11) DEFAULT NULL,
  `skill_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dposition_skill`
--

INSERT INTO `dposition_skill` (`position_id`, `skill_id`) VALUES
(8764, 111),
(8764, 222),
(2983, 222);

-- --------------------------------------------------------

--
-- Indexes for dumped tables
--

--
-- Indexes for table `skill`
--
ALTER TABLE `skill`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `desired_position`
--
ALTER TABLE `desired_position`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `skill`
--
ALTER TABLE `skill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `desired_position`
--
ALTER TABLE `desired_position`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dposition_skill`
--

ALTER TABLE `dposition_skill`
  ADD CONSTRAINT `dposition_skill_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skill` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `dposition_skill_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `desired_position` (`id`) ON DELETE CASCADE
