## To run this application
- Create a directory data and subdirectories named db and pgadmin 
    `mkdir -p data/{db,pgadmin}`

- Change permissions on `./data/pgadmin` by running `sudo chown -R 5050:5050 ./data/pgadmin`

- When running for the first time, run `docker-compose up --build`, 
    for subsequent runs, run `docker-compose up`

- After `docker-compose up` go to 
    - `localhost:8000` => Django application
    - `localhost:5050` => pgadmin

## To run commands inside the container
- Basically the command is
  - `docker-compose run [CONTAINER_NAME] [COMMAND]`
  - `docker-compose run web python3 manage.py makemigration`

## To stop the container run 
- `docker-compose down`