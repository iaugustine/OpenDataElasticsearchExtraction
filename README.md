# OpenDataElasticsearchExtraction

This is a CLI application to extract Open Parking and Camera
Violations dataset from NYC open data to an Elasticsearch instance
hosted on AWS. Once the data has been extracted, it can be visualized
in Kibana.
<br>
Pre-Requisites:
1. Machine with docker installed. Eg: EC2 instance or localhost with
docker installed.
2. Elasticsearch instance up and running. This could be in the cloud
or on a machine. The important factors are the availability of
the ES host address for access, and a username and password for
authentication.
3. APP token generated from the Socrata open data API to access and
extract data.
<br>
**How to run the application:**
1. Extract the zipped files.
2. In the terminal, navigate to the directory of the unzipped file.
3. Run the following command:
docker build -t bigdata1:1.0 project01/
This will build a docker image based on the instructions in the
Dockerfile which exists in the project01 folder.
4. Once the docker image is built, we can run a docker container
which will execute the application. In the application, we will
have to pass a few environment variables. They are:
a. DATASET_ID: For OPCV, the id is ‘nc67-uf89’
b. ES_USERNAME: The ES username for access
c. ES_PASSWORD: The ES password for access
d. APP_TOKEN: APP token generated for the Socrata Open Data API
e. ES_HOST: The address of the elasticsearch host to be used.
5. In addition to the above environment variables, we will also pass
2 command line arguments:
a. Num_pages: Number of pages of the data to fetch
b. Page_size: Size of each page which is to be fetched.
6. In order to run the docker container, the following command must
be executed and the variable values from step 4 and 5 must be
substituted:
docker run \
-e DATASET_ID="nc67-uf89" \
-e APP_TOKEN="<YOUR APP_TOKEN>" \
-e ES_HOST="<YOUR ES HOST>" \
-e ES_USERNAME="<USER ID>" \
-e ES_PASSWORD="<PASSWORD>" \
--network="host" \
bigdata1:1.0 --num_pages=<NUMBER OF PAGES NEEDED>
--page_size=<REQUIRED PAGE SIZE>
On running the above command the program will begin execution and
will extract the data from NYC Open data.
7. In order to view this data, you will need to login to the
Elasticsearch instance.
8. Once logged in to the elasticsearch instance, navigate to ‘Stack
Management’ and click on Index Patterns -> Create Index pattern
9. Enter the characters ‘my*’ and you will see an index by the name
‘my-index-1’. This is the index to which the program will write
the data to. Click on next and select issue_date as the time
field with which to view the data.
10. Click on create index pattern.
11. Navigate to Discover and search for the index pattern ‘my*’
from the top left corner.
12. Once you have navigated to Discover, you can view the data as
it is being loaded in Elasticsearch. (Kindly adjust the time
filter to the past 22 years to view the data)
