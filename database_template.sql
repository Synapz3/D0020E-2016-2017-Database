CREATE DATABASE  IF NOT EXISTS `d0020e` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `d0020e`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: d0020e
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.21-MariaDB-1~jessie

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `area` (
  `areaID` int(70) NOT NULL AUTO_INCREMENT,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `z` int(11) NOT NULL,
  `width` int(11) NOT NULL,
  `depth` int(11) NOT NULL,
  `height` int(11) NOT NULL,
  `checklistID` int(70) unsigned DEFAULT NULL,
  PRIMARY KEY (`areaID`),
  KEY `checklistIDarea_idx` (`checklistID`),
  CONSTRAINT `checklistIDarea` FOREIGN KEY (`checklistID`) REFERENCES `checklist` (`checklistID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `checklist`
--

DROP TABLE IF EXISTS `checklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `checklist` (
  `checklistID` int(70) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(512) NOT NULL,
  PRIMARY KEY (`checklistID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipment` (
  `macAddress` varchar(45) NOT NULL,
  `serialNumber` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `visualNumber` int(10) unsigned NOT NULL,
  `takenBy` int(10) unsigned DEFAULT '0',
  `sensorList` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`macAddress`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `position` (
  `currentX` int(11) DEFAULT NULL,
  `currentY` int(11) DEFAULT NULL,
  `currentZ` int(11) DEFAULT NULL,
  `oldX` int(11) DEFAULT NULL,
  `oldY` int(11) DEFAULT NULL,
  `userID` int(70) unsigned NOT NULL,
  `oldZ` int(11) DEFAULT NULL,
  `lastUpdated` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subtasks`
--

DROP TABLE IF EXISTS `subtasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subtasks` (
  `subtaskID` int(11) NOT NULL AUTO_INCREMENT,
  `taskID` int(70) NOT NULL,
  `subtasktitle` varchar(45) NOT NULL,
  `subtaskdescription` varchar(200) NOT NULL,
  `imagesrc` varchar(1000) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`subtaskID`),
  KEY `masterTaskID_idx` (`taskID`),
  CONSTRAINT `masterTaskID` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `taskID` int(70) NOT NULL AUTO_INCREMENT,
  `checklistID` int(70) unsigned zerofill DEFAULT NULL,
  `description` varchar(300) NOT NULL,
  `userID` varchar(140) DEFAULT NULL,
  `title` varchar(45) NOT NULL,
  `areaID` int(70) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`taskID`),
  KEY `AreaID_idx` (`areaID`),
  KEY `checklistIDtask_idx` (`checklistID`),
  CONSTRAINT `AreaID` FOREIGN KEY (`areaID`) REFERENCES `area` (`areaID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `checklistIDtask` FOREIGN KEY (`checklistID`) REFERENCES `checklist` (`checklistID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userID` int(70) unsigned NOT NULL AUTO_INCREMENT,
  `firstName` varchar(45) NOT NULL,
  `lastName` varchar(45) NOT NULL,
  `socialSecurityNr` int(10) NOT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `userPassword` varchar(70) NOT NULL,
  PRIMARY KEY (`userID`,`socialSecurityNr`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-15 17:48:25
