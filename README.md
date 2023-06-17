### installation
- copy file called cot-env from fenv folder, paste and renamed to .cot-env to
  root folder
- copy file called cot-envdb from fenv folder, paste and renamed to .cot-envdb
  to root folder
 
### build docker
```
 - docker-compose build
```

### up docker
```
 - docker-compose up -d 
```

### migreate db
```
 - docker-compose exec api python manage.py migrate --noinput 
```

### inside the docker images data base 
```
 - docker-compose exec db psql --username=myuser --dbname=mydatabase 
```
### create user in db
- reference = https://phoenixnap.com/kb/postgres-create-user
```
 - CREATE USER myuser WITH PASSWORD 'password';
```

### list volumes docker 
### display a list of volumes
```
 - docker volume ls 
```

### inspect a volume 
```
 - docker volume inspect my-volume-listed 
```

### build a docker using tag 
```
 - docker build -f ./app/Dockerfile -t mytagfordocker:latest ./app
```

### run another images in other port 
### docker is running on port localhost:9002
```
docker run -d \                                     
-p 9002:9001 \
-e "SECRET_KEY=mysecretkey" -e "DEBUG=1" -e "ALLOWED_HOSTS=*" \
api python /usr/src/app/manage.py runserver 0.0.0.0:9001
```

### show docker lgos
```
- docker-compose -f docker-compose.prod.yml logs -f
```
