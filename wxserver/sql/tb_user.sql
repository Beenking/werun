/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50634
Source Host           : localhost:3306
Source Database       : werun

Target Server Type    : MYSQL
Target Server Version : 50634
File Encoding         : 65001

Date: 2018-05-20 14:45:33
*/

USE `werun`;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `tb_user`
-- ----------------------------
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
  `openid` char(40) NOT NULL,
  `session_Key` char(40) DEFAULT NULL,
  `nickName` varchar(40) CHARACTER SET utf8 DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `language` char(10) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `province` varchar(20) DEFAULT NULL,
  `country` varchar(30) DEFAULT NULL,
  `avatarUrl` varchar(150) DEFAULT NULL,
  `steps` int(7) DEFAULT 0,
  `upvotes` int(5) DEFAULT 0,
  PRIMARY KEY (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

