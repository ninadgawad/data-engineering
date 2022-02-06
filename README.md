# Data Engineering
Data engineering is the aspect of data science that focuses on practical applications of data collection and analysis. The key to understanding what data engineering lies in the “engineering” part.  Engineers design and build things. “Data” engineers design and build pipelines that transform and transport data into a format wherein, by the time it reaches the Data Scientists or other end users, it is in a highly usable state.  These pipelines must take data from many disparate sources and collect them into a single warehouse that represents the data uniformly as a single source of truth.

## Understanding of:
- Data models
- Relational and non-relational database design
- Information flow
- Query execution and optimization
- Comparative analysis of data stores
- Logical operations

## Data engineers may be responsible for:
- Data Architecture
- Database Setup and Management
- Data Infrastructure Design and build


## Data Tools
- Apache Airflow [https://airflow.apache.org/]
- Pentaho Data Integration ( ETL/ELT ) a.k.a Kettle
- AbInitio 
- Informatica

## Data Engineering
![Data Engineering](https://github.com/ninadgawad/data-engineering/blob/master/Data_Engg.jpg)

## Tradinal Data Warehousing 

## Slowly Changing Dimensions (SCD) Types

- Type 0 – Fixed Dimension
No changes allowed, dimension never changes

- Type 1 – No History
Update record directly, there is no record of historical values, only current state

- Type 2 – Row Versioning
Track changes as version records with current flag & active dates and other metadata

- Type 3 – Previous Value column
Track change to a specific attribute, add a column to show the previous value, which is updated as further changes occur

- Type 4 – History Table
Show current value in dimension table but track all changes in separate table

- Type 6 – Hybrid SCD
Utilise techniques from SCD Types 1, 2 and 3 to track change


## Links
- https://help.hitachivantara.com/Documentation/Pentaho/8.0/Products/Data_Integration
- https://www.talend.com/

