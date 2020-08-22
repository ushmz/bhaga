CREATE TABLE members (
  slackID varchar(10) NOT NULL,
  _name varchar(128) NOT NULL,
  _kana varchar(128) DEFAULT NULL,
  _grade char(10) NOT NULL,
  /*'kanaOrder_grade' int(11) unsigned DEFAULT NULL,*/
  PRIMARY KEY (slackID)
) ENGINE=InnoDB;

CREATE TABLE trash (
    slackID varchar(10) NOT NULL,
    _room char(10) NOT NULL,
    _order int(11) DEFAULT NULL,
    _onDuty bit(1) NOT NULL,
    _cursor bit(1) NOT NULL,
    PRIMARY KEY (slackID)
) ENGINE=InnoDB;

CREATE TABLE minutes (
    slackID varchar(10) NOT NULL,
    _order int(11) DEFAULT NULL,
    _onDuty bit(1) NOT NULL,
    _cursor bit(1) NOT NULL,
    PRIMARY KEY (slackID)
) ENGINE=InnoDB;
