CREATE TABLE `members` (
  `slackID` varchar(10) NOT NULL,
  `_name` varchar(128) NOT NULL,
  `_kana` varchar(128) DEFAULT NULL,
  `_grade` char(10) NOT NULL,
  PRIMARY KEY (`slackID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `trash` (
  `slackID` varchar(10) NOT NULL,
  `_onDuty` bit(1) NOT NULL,
  `_doneInLoop` bit(1) NOT NULL,
  PRIMARY KEY (`slackID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
