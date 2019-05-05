/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50051
Source Host           : localhost:3306
Source Database       : test1

Target Server Type    : MYSQL
Target Server Version : 50051
File Encoding         : 65001

Date: 2019-03-08 18:40:07
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `userinfo`
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `id` int(10) unsigned zerofill NOT NULL auto_increment COMMENT '逐渐自增',
  `nikename` varchar(52) character set latin1 NOT NULL,
  `describe` varchar(100) character set latin1 default NULL,
  `username` varchar(52) character set latin1 NOT NULL,
  `pwd` varchar(52) character set latin1 NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('0000000001', 'gulu', '????', 'gulu', '123456');
INSERT INTO `userinfo` VALUES ('0000000002', 'test11', '??', 'test11', '123456');
