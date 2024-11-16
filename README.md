
### To setup database
1. Setup docker
2. Run the following to setup a postgres container
``` sh 
docker run --name dentalapipostgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres -c log_statement=all
```
3. Run the following to create the postgres database in the container
``` sh
docker exec -it dentalapipostgres psql -U postgres -c "CREATE DATABASE dentalapidb"
```

### Setup Virtual Environment
``` sh
cd repositoryfolder
python3 -m venv .venv
source .venv/bin/activate
```
### Install dependencies
``` sh
pip install -r requirements.txt
```

### Run the application
``` sh
uvicorn app.main:app --reload
```
Send a POST request to http://127.0.0.1:8000/scrape with the following body
``` json
{
    "pages": "2",
    "proxy": "proxy" 
}
```