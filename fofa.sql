/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50547
Source Host           : localhost:3306
Source Database       : fofa

Target Server Type    : MYSQL
Target Server Version : 50547
File Encoding         : 65001

Date: 2019-06-28 15:57:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for fofa_spider
-- ----------------------------
DROP TABLE IF EXISTS `fofa_spider`;
CREATE TABLE `fofa_spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `port` varchar(255) DEFAULT NULL,
  `protocol` varchar(255) NOT NULL,
  `country_name` varchar(255) DEFAULT NULL,
  `region_name` varchar(255) DEFAULT NULL,
  `city_name` varchar(255) DEFAULT NULL,
  `fofa_sql` text NOT NULL,
  `create_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=191 DEFAULT CHARSET=utf8mb4;
