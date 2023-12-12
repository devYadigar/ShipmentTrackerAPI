# ShipmentTrackerAPI

Project overview:

This project is composed of UserApi and Shipping api and simple crud operations.
All tests are included.

Installation:
- git clone https://github.com/devYadigar/ShipmentTrackerAPI.git 
- cd ShipmentTrackerAPI
- docker-compose build
- docker-compose up
-  docker-compose run --rm app sh -c "python manage.py wait_for_db"
-  docker-compose run --rm app sh -c "python manage.py migrate"
-  docker-compose run --rm app sh -c "python manage.py createsu" (for creating superuser)
