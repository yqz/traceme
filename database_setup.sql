delimiter $$

CREATE TABLE `TraceRecord` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `cid` varchar(48) COLLATE utf8_bin NOT NULL,
      `state` tinyint(4) NOT NULL,
      `longitude` double NOT NULL,
      `latitude` double NOT NULL,
      `timestamp` datetime NOT NULL,
      `altitude` double DEFAULT NULL,
      `speed` float DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `cid_index` (`cid`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin$$


