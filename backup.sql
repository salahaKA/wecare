-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: palliative1
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `apid` int NOT NULL AUTO_INCREMENT,
  `did` int NOT NULL,
  `lid` int NOT NULL,
  `status` varchar(30) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`apid`),
  KEY `did_idx` (`did`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`did`) REFERENCES `login` (`lid`),
  CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (3,23,24,'booking','2022-02-19 12:35:38'),(9,23,14,'booking','2022-02-23 12:57:29'),(10,23,24,'pending','2022-02-24 10:53:27'),(11,23,24,'pending','2022-04-08 12:54:17'),(12,23,24,'pending','2022-04-08 12:54:20');
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointment_status`
--

DROP TABLE IF EXISTS `appointment_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment_status` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `apid` int NOT NULL,
  `tid` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `apid_idx` (`apid`),
  KEY `tid_idx` (`tid`),
  CONSTRAINT `apid` FOREIGN KEY (`apid`) REFERENCES `appointment` (`apid`),
  CONSTRAINT `tid` FOREIGN KEY (`tid`) REFERENCES `doctor_time` (`tid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment_status`
--

LOCK TABLES `appointment_status` WRITE;
/*!40000 ALTER TABLE `appointment_status` DISABLE KEYS */;
INSERT INTO `appointment_status` VALUES (8,9,25,'2022-02-23 12:58:24'),(9,3,25,'2022-02-23 12:58:28');
/*!40000 ALTER TABLE `appointment_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blood_donation`
--

DROP TABLE IF EXISTS `blood_donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_donation` (
  `bid` int NOT NULL AUTO_INCREMENT,
  `hid` int NOT NULL,
  `blood_group` varchar(20) NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`bid`),
  KEY `hid_idx` (`hid`),
  CONSTRAINT `blood_donation_ibfk_1` FOREIGN KEY (`hid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_donation`
--

LOCK TABLES `blood_donation` WRITE;
/*!40000 ALTER TABLE `blood_donation` DISABLE KEYS */;
INSERT INTO `blood_donation` VALUES (1,2,'A-','accept','2022-02-21 12:14:37');
/*!40000 ALTER TABLE `blood_donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint`
--

DROP TABLE IF EXISTS `complaint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `dvid` int NOT NULL,
  `subject` varchar(45) NOT NULL,
  `complaint` varchar(45) NOT NULL,
  `reply` varchar(45) DEFAULT NULL,
  `reply_date` date DEFAULT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `lid_idx` (`lid`),
  KEY `dvid_idx` (`dvid`),
  CONSTRAINT `complaint_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`),
  CONSTRAINT `complaint_ibfk_2` FOREIGN KEY (`dvid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint`
--

LOCK TABLES `complaint` WRITE;
/*!40000 ALTER TABLE `complaint` DISABLE KEYS */;
INSERT INTO `complaint` VALUES (1,24,23,'subject','complaint','yrtyrtyrh','2022-04-08','2022-02-23 15:10:17'),(2,24,23,'iyuiy','uyiyui','','2022-04-08','2022-04-08 12:54:27');
/*!40000 ALTER TABLE `complaint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_reg`
--

DROP TABLE IF EXISTS `doctor_reg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_reg` (
  `did` int NOT NULL AUTO_INCREMENT,
  `rid` int NOT NULL,
  `hid` int NOT NULL,
  `specialization` varchar(45) NOT NULL,
  `exeperience` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`did`),
  KEY `rid_idx` (`rid`),
  KEY `hid_idx` (`hid`),
  CONSTRAINT `hid` FOREIGN KEY (`hid`) REFERENCES `hospital` (`hid`) ON DELETE CASCADE,
  CONSTRAINT `rid` FOREIGN KEY (`rid`) REFERENCES `registration` (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_reg`
--

LOCK TABLES `doctor_reg` WRITE;
/*!40000 ALTER TABLE `doctor_reg` DISABLE KEYS */;
INSERT INTO `doctor_reg` VALUES (1,6,2,'general medicine','5 Yrs','2022-02-16 14:05:24');
/*!40000 ALTER TABLE `doctor_reg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_time`
--

DROP TABLE IF EXISTS `doctor_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_time` (
  `tid` int NOT NULL AUTO_INCREMENT,
  `did` int NOT NULL,
  `day` varchar(45) NOT NULL,
  `from_time` datetime NOT NULL,
  `created_on` datetime NOT NULL,
  `to_time` datetime NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`tid`),
  KEY `did_idx` (`did`),
  CONSTRAINT `did` FOREIGN KEY (`did`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_time`
--

LOCK TABLES `doctor_time` WRITE;
/*!40000 ALTER TABLE `doctor_time` DISABLE KEYS */;
INSERT INTO `doctor_time` VALUES (25,23,'wednesday','2022-02-23 11:04:00','2022-02-23 11:04:33','2022-02-23 15:04:00','2022-02-23');
/*!40000 ALTER TABLE `doctor_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation`
--

DROP TABLE IF EXISTS `donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation` (
  `donation_id` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `description` text NOT NULL,
  `file` text NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  `nid` int NOT NULL,
  PRIMARY KEY (`donation_id`),
  KEY `nid_idx` (`nid`),
  CONSTRAINT `nid` FOREIGN KEY (`nid`) REFERENCES `needy_request` (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation`
--

LOCK TABLES `donation` WRITE;
/*!40000 ALTER TABLE `donation` DISABLE KEYS */;
INSERT INTO `donation` VALUES (8,1,'water bed','We are capable of handling both automated inbound and outbound consignments, we have excellent warehousing solutions available','waterbed.jpeg','accept','2022-02-19 20:05:40',2),(9,1,'wheel chair','wheel chair details','weelchair.jpg','accept','2022-02-23 13:33:47',3);
/*!40000 ALTER TABLE `donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation_assign`
--

DROP TABLE IF EXISTS `donation_assign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation_assign` (
  `did` int NOT NULL AUTO_INCREMENT,
  `drid` int NOT NULL,
  `vid` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`did`),
  KEY `drid_idx` (`drid`),
  KEY `vid_idx` (`vid`),
  CONSTRAINT `drid` FOREIGN KEY (`drid`) REFERENCES `donation_request` (`drid`),
  CONSTRAINT `vid` FOREIGN KEY (`vid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation_assign`
--

LOCK TABLES `donation_assign` WRITE;
/*!40000 ALTER TABLE `donation_assign` DISABLE KEYS */;
INSERT INTO `donation_assign` VALUES (2,2,13,'2022-02-19 21:50:13'),(3,4,13,'2022-02-23 13:40:24');
/*!40000 ALTER TABLE `donation_assign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation_request`
--

DROP TABLE IF EXISTS `donation_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation_request` (
  `drid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `did` int NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`drid`),
  KEY `lid_idx` (`lid`),
  KEY `did_idx` (`did`),
  CONSTRAINT `donation_request_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`),
  CONSTRAINT `donation_request_ibfk_2` FOREIGN KEY (`did`) REFERENCES `donation` (`donation_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation_request`
--

LOCK TABLES `donation_request` WRITE;
/*!40000 ALTER TABLE `donation_request` DISABLE KEYS */;
INSERT INTO `donation_request` VALUES (2,2,8,'accept','2022-02-19 20:27:12'),(3,24,8,'pending','2022-02-23 13:17:07'),(4,2,9,'accept','2022-02-23 13:38:45');
/*!40000 ALTER TABLE `donation_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `fid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `subject` varchar(45) NOT NULL,
  `feedback` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`fid`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,14,'feedback','something','2022-02-19 15:24:16'),(2,13,'subject','volunteer feedback','2022-02-21 10:40:00'),(3,23,'something','something','2022-02-23 15:34:09'),(4,2,'donor','feedback','2022-02-23 17:11:13'),(5,24,'edrftghyjk','iukuyui','2022-04-08 12:53:27');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital`
--

DROP TABLE IF EXISTS `hospital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospital` (
  `hid` int NOT NULL AUTO_INCREMENT,
  `hospital` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  `phone` varchar(45) NOT NULL,
  `landline` varchar(45) NOT NULL,
  `district` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `pincode` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `file` text NOT NULL,
  `lid` int NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`hid`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `hospital_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital`
--

LOCK TABLES `hospital` WRITE;
/*!40000 ALTER TABLE `hospital` DISABLE KEYS */;
INSERT INTO `hospital` VALUES (2,'hospital','test','8978767876','2356798','Kozhikode','thamarasseri','test','2354567','hospital@gmail.com','41miUcgrLL.jpg',11,'2022-02-14 10:38:31');
/*!40000 ALTER TABLE `hospital` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `lid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  `provisionized` tinyint NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'admin@gmail.com','admin','admin','2022-02-12 11:32:27',1),(2,'shyam@gmail.com','fETUMgFx9L','donor','2022-02-12 11:35:32',1),(11,'hospital@gmail.com','WWczPmeNX3','hospital','2022-02-14 10:38:31',1),(13,'volunteer@gmail.com','0zyS4f4Sxp','volunteer','2022-02-14 11:57:47',1),(14,'anjali@gmail.com','BpVpYKOVkT','patient','2022-02-14 12:29:09',1),(21,'doctor@gmail.com','qiZ70VFxHt','pending','2022-02-15 14:47:11',1),(22,'arjun@gmail.com','GIv16PqLWv','pending','2022-02-15 16:39:48',1),(23,'doctor@gmail.com','3jr18FuopM','doctor','2022-02-16 14:05:24',1),(24,'ajmal@gmail.com','OWD2f8iWQa','patient','2022-02-17 13:01:47',1);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `needy_request`
--

DROP TABLE IF EXISTS `needy_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `needy_request` (
  `nid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `description` varchar(100) NOT NULL,
  `status` varchar(45) NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`nid`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `needy_request_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `needy_request`
--

LOCK TABLES `needy_request` WRITE;
/*!40000 ALTER TABLE `needy_request` DISABLE KEYS */;
INSERT INTO `needy_request` VALUES (2,14,'water bed','A bed having a liquid-filled rubber or plastic mattress in a rigid, often heated, waterproof frame.','accept','2022-02-15 12:35:37'),(3,24,'wheel chair','something','accept','2022-02-23 13:16:00'),(4,14,'walk stick','walk stick','pending','2022-02-23 13:41:49'),(5,24,'wheel chair','hjhkhjk','pending','2022-04-08 12:53:16');
/*!40000 ALTER TABLE `needy_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `nid` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(45) NOT NULL,
  `content` varchar(45) NOT NULL,
  `date` date NOT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`nid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (2,'notification','notification','2022-02-21','2022-02-21 11:33:22');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `qid` int NOT NULL AUTO_INCREMENT,
  `lid` int NOT NULL,
  `did` int NOT NULL,
  `question` varchar(45) NOT NULL,
  `reply` varchar(45) DEFAULT NULL,
  `rdate` date DEFAULT NULL,
  `created_on` datetime NOT NULL,
  PRIMARY KEY (`qid`),
  KEY `lid_idx` (`lid`),
  KEY `did_idx` (`did`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`),
  CONSTRAINT `question_ibfk_2` FOREIGN KEY (`did`) REFERENCES `login` (`lid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (3,24,23,'question ','question reply','2022-02-23','2022-02-23 10:49:11'),(4,24,23,'klklkj','','2022-04-08','2022-04-08 12:54:15');
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `dob` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `blood_group` varchar(15) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `district` varchar(45) DEFAULT NULL,
  `pincode` varchar(45) DEFAULT NULL,
  `other_phone` varchar(45) DEFAULT NULL,
  `file` text,
  `lid` int NOT NULL,
  `created_on` datetime DEFAULT NULL,
  PRIMARY KEY (`rid`),
  KEY `lid_idx` (`lid`),
  CONSTRAINT `lid` FOREIGN KEY (`lid`) REFERENCES `login` (`lid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (1,'admin','admin@gmail.com','8978767876','02/03/1993','male','A+','address','kallayi','Kozhikode','673010','8967898765','41miUcgrLL.jpg',1,'2022-02-12 11:32:27'),(2,'shyam','shyam@gmail.com','8978677876','02/04/1980','male','B+','address','kanhangad','Kasaragod','672398','8967898762','download.jfif',2,'2022-02-12 11:35:32'),(4,'volunteer','csreeshma9@gmail.com','8978767777','02/06/1980','male','A-','test','thamarasseri','Kozhikode','654534','8967898762','profile.jpg',13,'2022-02-14 11:57:47'),(5,'anjali','anjali@gmail.com','9567564567','02/12/1993','female','AB+','test','thirur','Malappuram','674567','9234560978','41miUcgrLL.jpg',14,'2022-02-14 12:29:09'),(6,'doctor','sreeshmac200@gmail.com','8978677876','02/03/1993','female','A-','test','test','Ernakulam','675434','8967668762','41miUcgrLL.jpg',23,'2022-02-16 14:05:24'),(7,'ajmal','ajmal@gmail.com','8978677876','02/02/1992','male','O+','test','test','Kottayam','672345','8967898765','profile.jpg',24,'2022-02-17 13:01:47');
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-25 15:14:30
