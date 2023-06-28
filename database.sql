-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2058_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book` int(11) DEFAULT NULL,
  `genre` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `book_genre_ibfk_1` (`book`),
  KEY `book_genre_ibfk_2` (`genre`),
  CONSTRAINT `book_genre_ibfk_1` FOREIGN KEY (`book`) REFERENCES `books` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `book_genre_ibfk_2` FOREIGN KEY (`genre`) REFERENCES `genres` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (1,1,3),(2,3,1),(3,2,2),(4,4,3),(5,4,4),(6,7,3),(17,NULL,2),(18,NULL,4),(19,NULL,2),(20,NULL,4),(21,21,2),(22,21,4),(23,22,2),(24,22,4),(25,23,4),(30,NULL,2),(31,NULL,4),(32,NULL,2),(33,NULL,4),(34,NULL,2),(35,NULL,4),(36,NULL,2),(37,NULL,4),(61,36,2),(62,36,4),(63,34,2),(65,NULL,1),(66,NULL,1),(69,NULL,2),(70,43,2),(78,41,4),(79,39,3),(80,42,4),(81,37,4);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `short_desc` text NOT NULL,
  `year` year(4) NOT NULL,
  `publ_house` varchar(50) NOT NULL,
  `author` varchar(50) NOT NULL,
  `volume` int(11) NOT NULL,
  `cover` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `books_ibfk_1` (`cover`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`cover`) REFERENCES `covers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'Гранатовый браслет','Бедный чиновник влюбился в замужнюю даму, много лет писал ей письма, но понял, что всё напрасно, и застрелился. Заплаканная княгиня поняла: «любовь, о которой мечтает каждая женщина, прошла мимо неё».',1910,'Азбука','А. И. Куприн',400,0),(2,'Ревизор','В городе узнали о приезде ревизора и приняли за него случайного чиновника. Того всячески ублажали, давали взятки. Выручив хорошую сумму, чиновник спешно уехал. И тут в город приехал настоящий ревизор.',1935,'АСТ','Н. В. Гоголь',288,0),(3,'Повесть о жизни','Автобиографическое литературное произведение Константина Паустовского, которое он писал в течение 18 лет. Состоит из шести книг: «Далёкие годы», «Беспокойная юность», «Начало неведомого века», «Время больших ожиданий», «Бросок на юг», «Книга скитаний».',1948,'Азбука','К. Г. Паустовский',1184,0),(4,'Три мушкитера','«Три мушкетера» — величайший авантюрно-приключенческий роман, самая знаменитая книга блистательного французского романиста Александра Дюма. Несчетное число раз экранизированная история дерзких похождений гасконца д’Артаньяна, несмотря на почти двухсотлетний возраст, живет, вопреки законам времени и забвения, с прежней неувядаемой силой.',1944,'Иностранка','А. Дюма',736,0),(7,'test','test',2000,'test','test',200,0),(10,'test','book_form.short_desc',1999,'book_form.publ_house','book_form.author',1000,0),(11,'test','csasc',1999,'test','test',1000,0),(12,'test1','res',1999,'test','test',1000,0),(13,'test1','test',1999,'test','test',1000,0),(14,'test1','dwa',1999,'test','test',1000,0),(15,'test1','dwa',1999,'test','test',1000,0),(16,'test1','dwa',1999,'test','test',1000,0),(17,'test1','dwa',1999,'test','test',1000,0),(18,'test1','fwafwa',1999,'test','test',1000,0),(19,'test1','dwadwa',1999,'test','test',1000,0),(20,'test1','dwa',1999,'test','test',1000,0),(21,'test1','dwada',1999,'test','test',1000,0),(22,'проверка','dwa',1999,'test','test',1000,0),(23,'mardown','**dwada**\n*kyrsiv*\n# zagolovok',1999,'test','test',1000,0),(34,'del1','dwa',2001,'ОбложкаTest','test',1000,9),(36,'rrrrrrrrrrrrrrrrrrrr','rrrrrrrrrrrrrrrrr',1999,'test','test',10000,10),(37,'ff','nnnnnnnnn',2003,'aa','ff',55,11),(38,'zz','zzzz',2002,'zz','zz',3,11),(39,'hh','hhhhhcvas',2004,'hh','zz',9,11),(41,'Nonenn','ddd',2001,'None','Nonebb',5,11),(42,'mm','dwa',2007,'zz','tt',7,11),(43,'uuuu','cccc',2000,'ttt','uuu',1,11);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `mime_type` varchar(50) NOT NULL,
  `md5_hash` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (0,'gg','gg','gg'),(9,'22_3.jpg','jpg','4dde6ca5c2a3c5f86797b2e3966895ed'),(10,'1011059592.jpg','jpg','b60fa7b87958b0daab3134bb7880e4b5'),(11,'cover_test.jpg','jpg','ea68ffbed3fbc88a5cb236bb55d0b4ae');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'автобиография'),(2,'комедия'),(3,'повесть'),(4,'историческая');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `grade` int(11) DEFAULT NULL,
  `text_rew` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `statuses` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `book` (`book`),
  KEY `user` (`user`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`book`) REFERENCES `books` (`id`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`user`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,7,1,4,'aaaaa','2023-06-22 12:00:27',1),(2,7,3,5,'wwww','2023-06-22 12:01:00',2),(3,7,1,3,'ttttt','2023-06-22 13:08:09',2),(4,7,1,4,'ttttttttt','2023-06-22 13:08:42',2),(5,7,2,3,'rtyujidfghsdfgsdfghj','2023-06-22 13:22:03',3),(6,42,3,5,'','2023-06-22 13:50:10',2),(7,42,3,5,'wdwa','2023-06-22 13:50:18',1),(8,42,3,5,'dwa','2023-06-22 13:51:02',1),(9,42,3,2,'daw','2023-06-22 13:51:08',2),(10,39,3,4,'# Отзыв\n*Курсив*\n**Жирный**\n\n1. вцфвцфв\n2. вфцвфвф\n3. вцфафауы\n4. мцымцуу\n5. цмм','2023-06-22 14:51:11',2);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'пользователь','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statuses`
--

DROP TABLE IF EXISTS `statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `statuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statuses`
--

LOCK TABLES `statuses` WRITE;
/*!40000 ALTER TABLE `statuses` DISABLE KEYS */;
INSERT INTO `statuses` VALUES (1,'на рассмотрении'),(2,'одобрена'),(3,'отклонена');
/*!40000 ALTER TABLE `statuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL,
  `HASH` varchar(256) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) NOT NULL,
  `role` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`),
  KEY `role` (`role`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'user','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','Иван','Иванов','Иванович',3),(2,'admin','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','Иван','Иванов','Иванович',1),(3,'moder','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','Иван','Иванов','Иванович',2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-22 21:57:04
