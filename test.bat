@echo off
setlocal enabledelayedexpansion

echo Building the Docker containers...
docker-compose build

echo Running migrations...
docker-compose run --rm app flask db upgrade

echo Running unit tests...
docker-compose run --rm app pytest

echo Removing containers...
docker-compose down --volumes --remove-orphans

echo Done!
exit /b
