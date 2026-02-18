-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `accounts_catalogitem`
--

DROP TABLE IF EXISTS `accounts_catalogitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_catalogitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_catalogitem`
--

LOCK TABLES `accounts_catalogitem` WRITE;
/*!40000 ALTER TABLE `accounts_catalogitem` DISABLE KEYS */;
INSERT INTO `accounts_catalogitem` VALUES (1,'Тестовый товар','Тестовое описание',1000.00),(2,'1','',1.00),(3,'2','',2.00),(4,'3','',3.00),(5,'4','',4.00),(6,'5','',5.00),(7,'6','',6.00),(8,'7','',7.00);
/*!40000 ALTER TABLE `accounts_catalogitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_order`
--

DROP TABLE IF EXISTS `accounts_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fio` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` varchar(255) NOT NULL,
  `payment_type` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `item_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_order_item_id_c7f2099e_fk_accounts_catalogitem_id` (`item_id`),
  KEY `accounts_order_user_id_ec204867_fk_auth_user_id` (`user_id`),
  CONSTRAINT `accounts_order_item_id_c7f2099e_fk_accounts_catalogitem_id` FOREIGN KEY (`item_id`) REFERENCES `accounts_catalogitem` (`id`),
  CONSTRAINT `accounts_order_user_id_ec204867_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_order`
--

LOCK TABLES `accounts_order` WRITE;
/*!40000 ALTER TABLE `accounts_order` DISABLE KEYS */;
INSERT INTO `accounts_order` VALUES (1,'АБС','8888','1@1.ru','pupupu','cash','2025-03-28 18:10:48.289849',7,4),(2,'bbb','111','b@b.com','b b bbbbb','card','2025-03-28 19:56:45.765256',2,5);
/*!40000 ALTER TABLE `accounts_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fio` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `consent` tinyint(1) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (3,'a a a','88888888',1,4),(4,'bbb','111',1,5);
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_review`
--

DROP TABLE IF EXISTS `accounts_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_review_user_id_5846d9c4_fk_auth_user_id` (`user_id`),
  CONSTRAINT `accounts_review_user_id_5846d9c4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_review`
--

LOCK TABLES `accounts_review` WRITE;
/*!40000 ALTER TABLE `accounts_review` DISABLE KEYS */;
INSERT INTO `accounts_review` VALUES (1,'123','2025-03-27 21:02:48.035905',4),(2,'123','2025-03-27 21:02:52.481627',4),(3,'Тестовое сообщение','2025-03-27 21:03:04.384578',4),(4,'123','2025-03-27 21:05:23.930078',4),(5,'?','2025-03-28 19:56:57.441578',5);
/*!40000 ALTER TABLE `accounts_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add profile',7,'add_profile'),(26,'Can change profile',7,'change_profile'),(27,'Can delete profile',7,'delete_profile'),(28,'Can view profile',7,'view_profile'),(29,'Can add review',8,'add_review'),(30,'Can change review',8,'change_review'),(31,'Can delete review',8,'delete_review'),(32,'Can view review',8,'view_review'),(33,'Can add catalog item',9,'add_catalogitem'),(34,'Can change catalog item',9,'change_catalogitem'),(35,'Can delete catalog item',9,'delete_catalogitem'),(36,'Can view catalog item',9,'view_catalogitem'),(37,'Can add order',10,'add_order'),(38,'Can change order',10,'change_order'),(39,'Can delete order',10,'delete_order'),(40,'Can view order',10,'view_order');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$afOZ91CiLIBlmPvbJmZi1X$Hv2KknYOdY+PGrXiVrbJbBXfeIy6iSV1ho99e5CfV2o=','2025-03-27 20:42:05.216380',1,'test','','','test@test.com',1,1,'2025-03-27 17:37:17.565468'),(4,'pbkdf2_sha256$870000$AsQln68e9uK51psMGzr9Mu$sbwmjDjqzO3MAPIN0YqKqoP5yUxP9PrWOcUQKavwznU=','2025-03-28 17:51:46.756135',0,'aaa','','','a@a.ru',0,1,'2025-03-27 19:39:28.143816'),(5,'pbkdf2_sha256$870000$WpnPgT2mkLKp9Nc8h1fdIk$0bUXCVYV5VgdnvwAxEw895xJrrwYo9k1jMiDwGDGw84=','2025-03-28 19:56:21.708127',0,'bbb','','','b@b.com',0,1,'2025-03-28 19:56:10.072209');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-03-27 19:38:44.254319','3','aaa',3,'',4,1),(2,'2025-03-27 19:38:49.068137','2','a',3,'',4,1),(3,'2025-03-28 17:50:06.159844','1','1',1,'[{\"added\": {}}]',9,1),(4,'2025-03-28 17:50:07.738349','2','2',1,'[{\"added\": {}}]',9,1),(5,'2025-03-28 17:50:09.671446','3','3',1,'[{\"added\": {}}]',9,1),(6,'2025-03-28 17:59:15.599998','1','Тестовый товар',1,'[{\"added\": {}}]',9,1),(7,'2025-03-28 17:59:28.403864','2','1',1,'[{\"added\": {}}]',9,1),(8,'2025-03-28 17:59:33.798157','3','2',1,'[{\"added\": {}}]',9,1),(9,'2025-03-28 17:59:37.933596','4','3',1,'[{\"added\": {}}]',9,1),(10,'2025-03-28 17:59:56.482682','5','4',1,'[{\"added\": {}}]',9,1),(11,'2025-03-28 17:59:59.168061','6','5',1,'[{\"added\": {}}]',9,1),(12,'2025-03-28 18:00:06.252294','7','6',1,'[{\"added\": {}}]',9,1),(13,'2025-03-28 18:00:09.803949','8','7',1,'[{\"added\": {}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','catalogitem'),(10,'accounts','order'),(7,'accounts','profile'),(8,'accounts','review'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-27 17:24:46.888926'),(2,'auth','0001_initial','2025-03-27 17:24:47.157212'),(3,'accounts','0001_initial','2025-03-27 17:24:47.174828'),(4,'admin','0001_initial','2025-03-27 17:24:47.204644'),(5,'admin','0002_logentry_remove_auto_add','2025-03-27 17:24:47.207647'),(6,'admin','0003_logentry_add_action_flag_choices','2025-03-27 17:24:47.210528'),(7,'contenttypes','0002_remove_content_type_name','2025-03-27 17:24:47.232400'),(8,'auth','0002_alter_permission_name_max_length','2025-03-27 17:24:47.245215'),(9,'auth','0003_alter_user_email_max_length','2025-03-27 17:24:47.254526'),(10,'auth','0004_alter_user_username_opts','2025-03-27 17:24:47.258546'),(11,'auth','0005_alter_user_last_login_null','2025-03-27 17:24:47.271876'),(12,'auth','0006_require_contenttypes_0002','2025-03-27 17:24:47.272475'),(13,'auth','0007_alter_validators_add_error_messages','2025-03-27 17:24:47.276017'),(14,'auth','0008_alter_user_username_max_length','2025-03-27 17:24:47.292381'),(15,'auth','0009_alter_user_last_name_max_length','2025-03-27 17:24:47.307892'),(16,'auth','0010_alter_group_name_max_length','2025-03-27 17:24:47.314309'),(17,'auth','0011_update_proxy_permissions','2025-03-27 17:24:47.317538'),(18,'auth','0012_alter_user_first_name_max_length','2025-03-27 17:24:47.333119'),(19,'sessions','0001_initial','2025-03-27 17:24:47.339536'),(20,'accounts','0002_review','2025-03-27 20:37:31.125988'),(21,'accounts','0003_alter_review_created_at_alter_review_text_and_more','2025-03-27 20:58:40.830646'),(22,'accounts','0004_catalogitem','2025-03-28 17:47:40.271784'),(23,'accounts','0005_delete_catalogitem','2025-03-28 17:52:58.194237'),(24,'accounts','0006_catalogitem','2025-03-28 17:56:49.916390'),(25,'accounts','0007_order','2025-03-28 18:04:40.202722');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('7n6vn6h3dra8r3psdjx6g8a66dpcb0zc','.eJxVjEsOwjAMBe-SNYriNHEalux7hsqOXVpArdTPCnF3FKkL2L6ZeW_T07GP_bHp2k9irgbM5XdjKk-dK5AHzffFlmXe14ltVexJN9stoq_b6f4djLSNtZbiIhb2iJJBmzgoe8i-IOXUJKWhzSrcpDJIAmxjIMbWBRB2HoKYzxf7Yzg1:1txu3B:8iIyEQPD16qg_78jw-3rEaqMLL2WcyIjKUKU4lUGwak','2025-04-10 20:42:05.218452'),('ay0gsi33xm3gfawxwxo9xif89ooyyrvz','.eJxVjDsOwjAQBe_iGlnr-E9JnzNYu_aCA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTEWdhxOl3I8wPbjsod2y3Wea5rctEclfkQbsc58LPy-H-HVTs9VtrayMWYO0BidWAlP0A0ViAbNgqjDrE4o1zkQlIIQYkp3xR9qqDBfH-ANWON18:1txtfq:anUb_Fut_D7hxtycdYG-RsaqaMhcTVjT1AJFjX0wKzo','2025-04-10 20:17:58.333992'),('gyhozef8c1ovo6ykyg9j6yy32tk9ajae','.eJxVjMsOwiAQRf-FtSEDQym4dO83kBkeUjU0Ke3K-O_apAvd3nPOfYlA21rD1vMSpiTOYhCn340pPnLbQbpTu80yzm1dJpa7Ig_a5XVO-Xk53L-DSr1-a6OVBcuUyQEksoionGZG9NphtKSH4nIhP2pWYCiDV2wARlIaHBbx_gDFFjbq:1tyFoT:bpfDkwHp8yTscKxbFRQ8RAb9LVPL_P86MJLVGd4ZYM8','2025-04-11 19:56:21.709834'),('hg7gsyvfgzqxth81giue7entf1y4bvfb','.eJxVjDsOwjAQBe_iGlnr-E9JnzNYu_aCA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTEWdhxOl3I8wPbjsod2y3Wea5rctEclfkQbsc58LPy-H-HVTs9VtrayMWYO0BidWAlP0A0ViAbNgqjDrE4o1zkQlIIQYkp3xR9qqDBfH-ANWON18:1txtOU:BUW2JyAn0djh1UeFHFqBI2i9mIi-Gs0cbGW61xNbNB0','2025-04-10 20:00:02.003044'),('l8f9u9e3ic2glwrza2w9lghllim1onuk','.eJxVjDsOwjAQBe_iGlnr-E9JnzNYu_aCA8iR4qRC3B0ipYD2zcx7iYTbWtPWeUlTEWdhxOl3I8wPbjsod2y3Wea5rctEclfkQbsc58LPy-H-HVTs9VtrayMWYO0BidWAlP0A0ViAbNgqjDrE4o1zkQlIIQYkp3xR9qqDBfH-ANWON18:1txtjL:9CVOgw8YaDzXH4uvCEggAtYJBOgUpOMIllRIXLBhVYs','2025-04-10 20:21:35.969562');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-28 23:01:10
