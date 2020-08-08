/* Create a Table using SQL */
CREATE TABLE UNIVERSE (  
  galaxy_no     number,  
  name          varchar2(50) not null, 
  consellation  varchar2(50) not null, 
  location      varchar2(50),  
  constraint pk_departments primary key (galaxy_no)  
);

/* Alter Table add age to Universe table  */
ALTER TABLE UNIVERSE 
ADD AGE number(19,2);

/* Insert Data into Table */
INSERT INTO UNIVERSE (galaxy_no, name, consellation,location,age) 
VALUES (1, 'MilkyWay', 'Sagittarius','Southeast',1310000000);


/* Delete from Universe Table all galaxies which have age as NULL */
DELETE FROM UNIVERSE
WHERE AGE is null;

/* Group Galaxies By consellation */
SELECT consellation, COUNT(*)
FROM UNIVERSE
GROUP BY consellation;

/* HAVING */
SELECT consellation, COUNT(*)
FROM UNIVERSE
GROUP BY consellation
HAVING COUNT(*) > 10;
