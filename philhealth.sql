-- SQLite does not have a CREATE DATABASE statement, use .open command to create a new database
-- .open philhealth.db

-- Dropping tables if they exist
DROP TABLE IF EXISTS `member`;
DROP TABLE IF EXISTS `dependents`;
DROP TABLE IF EXISTS `membertype`;

-- Table structure for table `member`
CREATE TABLE `member` (
  `PhilHealth_ID` TEXT NOT NULL,
  `Members_Name` TEXT NOT NULL,
  `Mothers_Name` TEXT NOT NULL,
  `Spouses_Name` TEXT DEFAULT 'N/A',
  `Birth_Date` TEXT NOT NULL,
  `Birth_Place` TEXT NOT NULL,
  `Sex` TEXT NOT NULL,
  `Civil_Status` TEXT NOT NULL,
  `Citizenship` TEXT NOT NULL,
  `PhilSys_ID` TEXT DEFAULT 'N/A',
  `TIN_ID` TEXT DEFAULT 'N/A',
  `Address` TEXT NOT NULL,
  `Tel_No` TEXT NOT NULL,
  `Mobile_No` TEXT NOT NULL,
  `Email_Address` TEXT DEFAULT 'N/A',
  PRIMARY KEY (`PhilHealth_ID`)
);

-- Dumping data for table `member`
INSERT INTO `member` VALUES
('0101-1234-2024','DELA CRUZ, JUAN B. JR','BAUTISTA, MARIA C.','DELA CRUZ, CRISTINA A.','1997-01-01','BUSTILLOS STREET, SAMPALOC, MANILA','M','M','FILIPINO','1234-5678-91-01-1213','123-456-789','833 SISA ST., BARANGAY 526, ZONE 52, SAMPALOC, MANILA','02-1234-5678','09123456789','juandelacruz@gmail.com'),
('0102-4567-2023','REYES, PAUL JOHN D.','DIAZ, JOSEFINA M.','REYES, PATRICIA L.','1989-02-24','ALABANG-ZAPOTE ROAD, MUNTINLUPA, METRO MANILA','M','M','FILIPINO','2312-4123-56-10-9867','214-345-542','108 GEN. CONCEPTION ST., CALOOCAN CITY, METRO MANILA','63-4567-1298','09872531423','reyespauljohn@gmail.com'),
('0103-1275-2012','SANTOS, ANNE C.','CRISOSTOMO, MARIA E.','','1991-03-21','PASONG TAMO UP, SAN JUAN, MAKATI','F','S','FILIPINO','7563-5823-11-09-5321','355-238-094','139 MANGO ST., CIRCUMFERENTIAL ROAD, QUEZON AVENUE, ANTIPOLO RIZAL','63-8123-4567','09388137430','santosfranco@gmail.com'),
('0104-1026-2022','ARELLANO, DAVE G.','OLAES, ROSE G.','ARELLANO, MIKAELA M.','1995-12-25','RAMON MAGSAYSAY AVE,ANGELES CITY, PHILIPPINES','M','M','FILIPINO','6757-4332-98-43-2246','985-230-219','73 ROOSEVELT AVENUE, SFDM, QUEZON CITY, METRO MANILA','63-7248-2481','09746329181','arellanodave@gmail.com'),
('0105-7821-2020','TRINIDAD, TRISHA E.','EVANGELINE, LIZEL D.','TRINIDAD, RUEL C.','1999-04-21','GEN. ROXAS ST., BRGY SAN JOSE, QUEZON CITY, METRO MANILA','F','M','FILIPINO','3428-2395-41-27-0032','232-125-687','8751 PASEO DE ROXAS STREET, SAN MIGUEL VILLAGE, BRGY. POBLACION, MAKATI CITY','63-1674-2439','09651869402','trinidadtrisha2@gmail.com'),
('0107-1283-2018','OCAMPO, FRANCESCA G.','GOMEZ, PACITA C.','OCAMPO, MIKE O.','1987-10-04','BRGY. PAG-ASA, LAMITAN, ANGONO, RIZAL','F','W','FILIPINO','8923-9409-01-23-9867','331-563-216','667 AB FERNANDEZ AV, DAGUPAN CITY, ILOCOS','63-2841-5950','09994732772','ocampofrancesca11@gmail.com'),
('0108-2381-2014','MARASIGAN, IGNACIO F.','ORDONA, PERCY H.','MARASIGAN, ERIN B.','1992-11-03','SUMAGDANG, ISABELA CITY','M','M','FILIPINO','5685-3241-04-34-6967','673-452-123','1081 EDSA BALINTAWAK, QUEZON CITY, METRO MANILA','63-0894-1920','09937413349','marasigan_ignacio@gmail.com'),
('0110-5230-2019','JAVIER, LUCIA M.','MALABANAN, GREGORIA S.','','2000-07-08','GENESIS ST., MALITLIT, SANTA ROSA, LAGUNA','F','S','FILIPINO','1345-6942-10-90-4854','345-495-120','25 EAST CAPITOL DRIVE, PASIG, METRO MANILA','63-5895-1009','09932374671','javierlucia21@gmail.com');



-- Table structure for table `dependents`
CREATE TABLE `dependents` (
  `Dependent_ID` TEXT NOT NULL,
  `Dependent_Name` TEXT NOT NULL,
  `Dependent_Relationship` TEXT NOT NULL,
  `Dependent_Birthdate` TEXT NOT NULL,
  `Dependent_Citizenship` TEXT NOT NULL,
  `Disability` TEXT DEFAULT 'N/A',
  `Philhealth_ID` TEXT NOT NULL,
  PRIMARY KEY (`Dependent_ID`),
  FOREIGN KEY (`Philhealth_ID`) REFERENCES `member` (`PhilHealth_ID`)
);

-- Dumping data for table `dependents`
INSERT INTO `dependents` VALUES
('0001-0001-2024','DELA CRUZ, KYLA A.','Child','2015-10-15','Filipino','Autism','0101-1234-2024'),
('0002-0001-2024','REYES, CRIZEL L.','Child','2011-03-12','Filipino','','0102-4567-2023'),
('0002-0002-2024','REYES, CRISTOPHER L.','Child','2012-05-06','Filipino','','0102-4567-2023'),
('0003-0001-2024','CRISOSTOMO, MARIA E.','Mother','1955-08-11','Filipino','Deaf','0103-1275-2012'),
('0004-0001-2024','ARELLANO, BRUCE M.','Child','2009-09-30','Filipino','','0104-1026-2022'),
('0004-0002-2024','ARELLANO, CAITLYN M.','Child','2011-03-26','Filipino','','0104-1026-2022'),
('0004-0003-2024','ARELLANO, CASSY M.','Child','2015-01-28','Filipino','','0104-1026-2022'),
('0005-0001-2024','TRINIDAD, RUEL E.','Spouse','1999-09-20','Filipino','PWD','0105-7821-2020'),
('0006-0001-2024','OCAMPO, RECHELLE G.','Child','2015-06-29','Filipino','','0107-1283-2018'),
('0006-0002-2024','OCAMPO, DAVID G.','Child','2017-02-16','Filipino','','0107-1283-2018'),
('0007-0001-2024','MARASIGAN, ERIN B.','Spouse','1992-09-26','Filipino','','0108-2381-2014'),
('0008-0001-2024','MALABANAN, GREGORIA S.','Mother','1960-12-29','Filipino','PWD','0110-5230-2019');

-- Table structure for table `membertype`
CREATE TABLE `membertype` (
  `Philhealth_ID` TEXT NOT NULL,
  `Contributor_Type` TEXT NOT NULL,
  `Direct_Contributor` TEXT DEFAULT 'N/A',
  `Direct_Contributor_Type` TEXT DEFAULT 'N/A',
  `Profession` TEXT DEFAULT 'N/A',
  `Monthly_Income` TEXT DEFAULT 'N/A',
  `Proof_Of_Income` TEXT DEFAULT 'N/A',
  `Indirect_Contributor` TEXT DEFAULT 'N/A',
  PRIMARY KEY (`Philhealth_ID`)
);

-- Dumping data for table `membertype`
INSERT INTO `membertype` VALUES
('0101-1234-2024','Direct','Employee Private','','Software Engineer','50000','Payslip',''),
('0102-4567-2023','Direct','Employed Government','','Teacher','24000','Payslip',''),
('0103-1275-2012','Indirect','','','','','','4ps/MCCT'),
('0104-1026-2022','Direct','Family Driver','','Driver','22000','Payslip',''),
('0105-7821-2020','Indirect','','','','','','4ps/MCCT'),
('0107-1283-2018','Direct','Kasambahay','','Domestic Worker','8000','Payslip',''),
('0108-2381-2014','Direct','Migrant Worker','Sea-Based','Marine Engineer','98000','Payslip',''),
('0110-5230-2019','Direct','Employed Private','','Nurse','24000','Payslip','');

-- SQLite does not require statements like SET SQL_MODE or SET FOREIGN_KEY_CHECKS
-- SQLite does not use collation and character set settings in the same way as MySQL

-- Dump completed on 2024-07-12 16:27:42

