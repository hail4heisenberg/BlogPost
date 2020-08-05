-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: blog_db
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

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
-- Table structure for table `blog_comments`
--

DROP TABLE IF EXISTS `blog_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_comments` (
  `comment_id` varchar(10) NOT NULL,
  `comment_title` text NOT NULL,
  `comment_body` varchar(80) NOT NULL,
  `comment_by` text NOT NULL,
  `comment_blogid` tinytext NOT NULL,
  `comment_time` datetime NOT NULL,
  `comment_by_name` text NOT NULL,
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `comment_id_UNIQUE` (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_comments`
--

LOCK TABLES `blog_comments` WRITE;
/*!40000 ALTER TABLE `blog_comments` DISABLE KEYS */;
INSERT INTO `blog_comments` VALUES ('DFkBvpDzwJ','tesed','fdghghk,hiliyyttfvbnhtm,iouyut','beta@beta.com','DDagQnVThL','2019-09-23 15:30:46','beta'),('eoaRQkLEjd','klnkllnknk','mlm;lm;;lm','beta@beta.com','DDagQnVThL','2019-09-23 15:57:09','beta'),('hlEFcGRCdk','','','beta@beta.com','DDagQnVThL','2019-09-23 15:31:06','beta'),('HxuFrWIOsU','bubjk','njknlknlm;lk;ml;ml;kn','beta@beta.com','DDagQnVThL','2019-09-23 20:20:27','beta'),('ibeznASpMG','testing','nfjkdsnflkbmf;ls,m fdm,fdmdslkvmfd;l','beta@beta.com','DDagQnVThL','2019-09-23 15:24:30','beta'),('jXzUBXdlOV','klmnlk;m','ml;m;lml;','beta@beta.com','DDagQnVThL','2019-09-23 15:57:20','beta'),('NuPuhzRlOq','fgdssdv','dsbfbffdn','beta@beta.com','baZUpcgkFo','2019-09-24 21:07:20','beta'),('qDoDqctyob','hello','How are u ji?','beta@beta.com','EvZTCgvDHu','2019-09-24 10:07:45','beta'),('TNcsDjfugh','','','beta@beta.com','DDagQnVThL','2019-09-23 15:31:22','beta'),('YNeBhZekMm','hi','comment stored','beta@beta.com','DDagQnVThL','2019-09-23 15:15:39','beta'),('ZbkLAgiqjS','hkjln','jkn , l;mpon','beta@beta.com','DDagQnVThL','2019-09-23 15:36:34','beta');
/*!40000 ALTER TABLE `blog_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_details`
--

DROP TABLE IF EXISTS `blog_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_details` (
  `blog_id` varchar(10) NOT NULL,
  `blog_title` varchar(45) NOT NULL,
  `blog_desc` text NOT NULL,
  `blog_image` varchar(45) DEFAULT NULL,
  `blog_owner_email` varchar(45) NOT NULL,
  `blog_owner_name` tinytext NOT NULL,
  `blog_likes` int(11) DEFAULT '0',
  `button_config` text,
  `blog_dislikes` int(11) DEFAULT '0',
  `blog_category` text NOT NULL,
  `blog_publish_time` datetime DEFAULT NULL,
  `blog_last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`blog_id`),
  UNIQUE KEY `blog_id_UNIQUE` (`blog_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_details`
--

LOCK TABLES `blog_details` WRITE;
/*!40000 ALTER TABLE `blog_details` DISABLE KEYS */;
INSERT INTO `blog_details` VALUES ('baZUpcgkFo','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'political','2019-09-24 15:17:33','2019-09-24 15:54:17'),('DDagQnVThL','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'lMLLCFHCjp','priya@mail.com',0,'btn btn-primary btn-lg',1,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('EvZTCgvDHu','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-primary btn-lg',0,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('hHHMWLyWhy','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'priya@mail.com','priya',0,'btn btn-primary btn-lg',0,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('IcXkXEsgBf','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'test@mail.com','random',0,'btn btn-primary btn-lg',0,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('IvomeguWcq','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'priya@mail.com','priya',0,'btn btn-primary btn-lg',2,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('jVlzmVwUJv','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'test@mail.com','random',0,'btn btn-primary btn-lg',0,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('JYOvkxlKGq','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'test@mail.com','random',0,'btn btn-light btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17'),('ohgyONBcan','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('PjStzDvDfw','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17'),('sNQmaTPixa','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'priya@mail.com','priya',0,'btn btn-light btn-lg',0,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('sybAFmSbBe','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'test@mail.com','random',0,'btn btn-light btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17'),('tlTAaYPLMz','titile','tnkjnflkmfvldm,fd kj',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'entertainment','2019-09-24 16:07:47',NULL),('uugIXNlrlI','i3 Lab',' sadsafdsdsdsvdsf ',NULL,'test@mail.com','random',0,'btn btn-light btn-lg',0,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('VVngyPcmeY','titile','tnkjnflkmfvldm,fd kj',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'entertainment','2019-09-24 16:08:32',NULL),('VZtUBUktzy','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'lMLLCFHCjp','priya@mail.com',0,'btn btn-primary btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17'),('wKmtrHXqwG','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-primary btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17'),('WqYKSUUfGY','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('WzuQmINKnc','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'science','2019-09-23 10:21:17','2019-09-24 15:54:17'),('XXLfPwMdOc','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'beta@beta.com','beta',0,'btn btn-light btn-lg',0,'political','2019-09-23 10:21:17','2019-09-24 15:54:17'),('ygitxGpggR','I3 Lab TINJR','It is situated in Techno INdia NJr Institute Of technology\r\nUdaipur Rajasthan',NULL,'priya@mail.com','priya',0,'btn btn-light btn-lg',0,'entertainment','2019-09-23 10:21:17','2019-09-24 15:54:17');
/*!40000 ALTER TABLE `blog_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blog_reviews`
--

DROP TABLE IF EXISTS `blog_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog_reviews` (
  `action_id` varchar(10) NOT NULL,
  `blog_r_id` varchar(10) NOT NULL,
  `action_like` text,
  `action_dislike` text,
  PRIMARY KEY (`action_id`),
  UNIQUE KEY `action_id_UNIQUE` (`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog_reviews`
--

LOCK TABLES `blog_reviews` WRITE;
/*!40000 ALTER TABLE `blog_reviews` DISABLE KEYS */;
INSERT INTO `blog_reviews` VALUES ('CgzWQoyfTc','IvomeguWcq',NULL,'beta@beta.com'),('deptgLZlNT','DDagQnVThL',NULL,'beta@beta.com'),('ELrikDcKJf','IvomeguWcq',NULL,'success@mail.com');
/*!40000 ALTER TABLE `blog_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_details`
--

DROP TABLE IF EXISTS `user_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_details` (
  `user_id` varchar(10) NOT NULL,
  `user_name` varchar(45) NOT NULL,
  `user_password` varchar(45) NOT NULL,
  `user_last_login` varchar(45) DEFAULT NULL,
  `user_email` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `user_email_UNIQUE` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_details`
--

LOCK TABLES `user_details` WRITE;
/*!40000 ALTER TABLE `user_details` DISABLE KEYS */;
INSERT INTO `user_details` VALUES ('1001','garvit','solanki','','garvitsolanki5@gmail.com'),('DSOweDDiLA','success','#41724A72A7516CFBCEB1DA6B763D52AC0B93095D',NULL,'success@mail.com'),('gZfvrpsnUY','hima','ji',NULL,'nshu'),('lMLLCFHCjp','priya','ahuja',NULL,'priya@mail.com'),('RDOLfekkZv','random','bhf',NULL,'test@mail.com'),('rUIamasnvL','beta','#BD66B1F6FB23D3DBC4E5DDF5B5FF1A4473950D95',NULL,'beta@beta.com'),('tgNDuqlEak','final','#D97F0A69ABBE1A798C59B374FB08C4A31FEA3815',NULL,'final@test.com'),('tKrPIIFnHb','vidit','temp',NULL,'vidit@gmail.com');
/*!40000 ALTER TABLE `user_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-29 10:44:58
