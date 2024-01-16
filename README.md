# Data Engineering
Data engineering is the aspect of data science that focuses on practical applications of data collection and analysis. The key to understanding what data engineering lies in the “engineering” part.  Engineers design and build things. “Data” engineers design and build pipelines that transform and transport data into a format wherein, by the time it reaches the Data Scientists or other end users, it is in a highly usable state.  These pipelines must take data from many disparate sources and collect them into a single warehouse that represents the data uniformly as a single source of truth. It is a critical discipline within the broader field of data management, focusing on the design, development, and maintenance of systems and architectures for collecting, storing, processing, and analyzing large volumes of data. It involves the creation of robust infrastructure, data pipelines, and workflows to ensure the efficient and reliable flow of data throughout an organization. Data Engineers play a key role in transforming raw data into a usable format for analysis, enabling businesses to derive valuable insights and make informed decisions.

### List of various technologies related to this: 
- Database management systems
- ETL (Extract, Transform, Load) processes
- Data Warehousing
- Data Quality
- Data Accessibility

## Understanding of:
- Data models
- Data Ingestion
- Feature Engineering
- Relational and non-relational database design
- Information flow
- Query execution and optimization
- Comparative analysis of data stores
- Logical operations
- Big Data Tools
- Data Accessibility

## Data engineers may be responsible for:
- Data Architecture
- Database Setup and Management
- Data Infrastructure Design and build


## Data Tools
- Apache Airflow [https://airflow.apache.org/]
- Pentaho Data Integration ( ETL/ELT ) a.k.a Kettle
- AbInitio 
- Informatica
- Apache Spark
- Apache Flink 

## Data Engineering
![Data Engineering](https://github.com/ninadgawad/data-engineering/blob/master/Data_Engg.jpg)

## Tradinal Data Warehousing 

## Slowly Changing Dimensions (SCD) Types
- Type 0 – Fixed Dimension: No changes allowed, dimension never changes
- Type 1 – No History: Update record directly, there is no record of historical values, only current state
- Type 2 – Row Versioning: Track changes as version records with current flag & active dates and other metadata
- Type 3 – Previous Value column: Track change to a specific attribute, add a column to show the previous value, which is updated as further changes occur
- Type 4 – History Table: Show current value in dimension table but track all changes in separate table
- Type 6 – Hybrid SCD: Utilise techniques from SCD Types 1, 2 and 3 to track change


### Sample Type2 SCD
| SEQ_ID | PHONE_ID | START_DATE | END_DATE | ACTIVE | PHONE_NAME | PRICE |
|---|---|---|---|---|---|---|
| 1001 | S101 | 1/1/2021 | 12/31/2022 | N | Sam | 1240 |
| 1002 | A202 | 5/10/2022 | 12/31/9999 | Y | App | 1425 |
| 1003 | G103 | 3/5/2020 | 12/31/9999 | Y | Gog | 985 |
| 1112 | S101 | 1/1/2023 | 12/31/9999 | Y | Sam v2 | 4560 |


## Top 5 Java based Data Engineering Tools:
- **Apache Hadoop**: Hadoop is an open-source framework for distributed storage and processing of large data sets. It includes the Hadoop Distributed File System (HDFS) for storage and MapReduce for parallel processing.
- **Apache Spark**: Spark is a fast and general-purpose cluster-computing framework that provides in-memory data processing. It supports various programming languages, including Java/Scala/Python.
- **Apache Kafka**: Kafka is a distributed streaming platform that is widely used for building real-time data pipelines and streaming applications.
- **Apache Flink**: Flink is a stream processing framework for big data processing and analytics. It supports both batch and stream processing.
- **Spring Batch**: Spring Batch is a framework for building batch processing applications in Java. It simplifies the development of robust and scalable batch applications.

## Links
- https://help.hitachivantara.com/Documentation/Pentaho/8.0/Products/Data_Integration
- https://www.talend.com/

