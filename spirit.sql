SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `spirit` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `spirit`;

CREATE TABLE IF NOT EXISTS `users` (
  `Id` int(11) NOT NULL,
  `Username` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Swid` varchar(39) COLLATE utf8mb4_unicode_ci NOT NULL,
  `LoginKey` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ConfirmationHash` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Avatar` smallint(6) NOT NULL DEFAULT '0',
  `AvatarAttributes` varchar(98) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '{"spriteScale":100,"spriteSpeed":100,"ignoresBlockLayer":false,"invisible":false,"floating":false}',
  `Coins` mediumint(9) NOT NULL DEFAULT '10000',
  `Moderator` tinyint(1) NOT NULL DEFAULT '0',
  `Inventory` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `Color` tinyint(4) NOT NULL DEFAULT '1',
  `Head` mediumint(9) NOT NULL DEFAULT '0',
  `Face` mediumint(9) NOT NULL DEFAULT '0',
  `Neck` mediumint(9) NOT NULL DEFAULT '0',
  `Body` mediumint(9) NOT NULL DEFAULT '0',
  `Hands` mediumint(9) NOT NULL DEFAULT '0',
  `Feet` mediumint(9) NOT NULL DEFAULT '0',
  `Photo` mediumint(9) NOT NULL DEFAULT '0',
  `Pin` mediumint(9) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `users` (`Id`, `Username`, `Password`, `Swid`, `LoginKey`, `ConfirmationHash`, `Avatar`, `AvatarAttributes`, `Coins`, `Moderator`, `Inventory`, `Color`, `Head`, `Face`, `Neck`, `Body`, `Hands`, `Feet`, `Photo`, `Pin`) VALUES
(101, 'Arthur', '5F4DCC3B5AA765D61D8327DEB882CF99', '{b2b6ffd1-9f89-4277-afa8-9ed143451f0a}', NULL, NULL, 0, '{"spriteScale":100,"spriteSpeed":100,"ignoresBlockLayer":false,"invisible":false,"floating":false}', 4980, 0, '4%1634%5042%24318%5542%21072%24349%5344%5184%24350%24157%24352%24354%24338%24336%24337%21068%711%712', 4, 21068, 0, 0, 24337, 5042, 0, 0, 0);


ALTER TABLE `users`
  ADD PRIMARY KEY (`Id`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD UNIQUE KEY `Swid` (`Swid`);


ALTER TABLE `users`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=102;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
