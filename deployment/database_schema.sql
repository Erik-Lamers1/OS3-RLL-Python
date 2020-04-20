-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: os3rl
-- ------------------------------------------------------
-- Server version       5.7.29-0ubuntu0.18.04.1

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
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `challenges` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL COMMENT 'Challenge creation date',
  `p1` varchar(255) NOT NULL COMMENT 'ID of player 1 (challenger)',
  `p2` varchar(255) NOT NULL COMMENT 'ID of player 2 (challenged)',
  `p1_wins` int(11) DEFAULT NULL COMMENT 'How many games were won by p1',
  `p2_wins` int(11) DEFAULT NULL COMMENT 'How many games were won by p2',
  `p1_score` int(11) DEFAULT NULL COMMENT 'The total amount of goals by p1',
  `p2_score` int(11) DEFAULT NULL COMMENT 'The total amount of goals by p2',
  `winner` int(11) DEFAULT NULL COMMENT 'ID of the winner',
  PRIMARY KEY (`id`),
  KEY `p1_score` (`p1_score`,`p2_score`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT 'Real name of the user',
  `gamertag` varchar(255) NOT NULL COMMENT 'RL gamertag of the user',
  `discord` varchar(255) NOT NULL COMMENT 'Discord handle of the user (username#1234)',
  `rank` int(11) NOT NULL DEFAULT '0' COMMENT 'Current rank of the user',
  `wins` int(11) NOT NULL DEFAULT '0' COMMENT 'Total amount of wins',
  `losses` int(11) NOT NULL DEFAULT '0' COMMENT 'Total amount of losses',
  `challenged` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'User is currently challenged',
  `timeout` datetime NOT NULL COMMENT 'Current challenger timeout of the user',
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discord` (`discord`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-20 21:32:55
