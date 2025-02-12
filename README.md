#retail-data-etl-project
An ETL pipeline for a fake retail store.
<br />
What this project does: 
1: Defines an ETL pipeline to store(in RDS), retreive, transform and store(in S3) retail data(pipeline dag can be found below). <br />
2: Creates a database with relevant tables(schema can be found below) if the database does not exist. <br />
3: Generates random fake data to populate the tables. <br />
4: Pushes the data to the database. <br />
5: Transforms data based on user requirements. <br />
6: Stores transformed data in cloud. <br />
<br />
What this project uses: <br />
1: Airflow to orchestrate the ETL pipeline. <br />
2: Python as programming language for logic implemntation. <br />
3: AWS RDS for database management. <br />
4: AWS S3 as data lake for transformed data. <br />
5: Faker(package) to generate random/fake data. <br />
6: psycopg2(PostgreSQL package) to connect to RDS database and perform SQL operations. <br />
7: Boto3 to connect to S3 bucket for storing transformed datasets. <br />

<br />
Pipeline DAG: 

![dag-img](image.png)

<br />
Database schema: 

![schema-img](image-1.png)

Custom transformations: 
The best feature of this pipeline is to be able to create your own custom dataset without having to modify the code!
All one would have to do is write a sql query to query what they'd want and place it inside /customScripts/sqlScripts with '.txt' extension and the the transformed csv will be available in the users S3 bucket once the pipeline is run.
<br />
Data generation: <br />
This project is also capable of generating fake data to be pushed into the RDS for experimentation. <br />
This step is required initially as there is no data present at the start. <br />
One can generate n users, n discounts, and n orders. <br />
To modify, please go to the generate_and_push_data_to_rds() in /dags/etl-pipeline.py and modify the numbers. <br />