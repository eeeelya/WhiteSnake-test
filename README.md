# WhiteSnake-test
My test project for a WhiteSnake company.

### Installing


Install repo on your computer:

    git clone https://github.com/eeeelya/WhiteSnake-test.git

Run docker container:

    sudo docker-compose up --build

If you want to create superuser:
    
    sudo docker exec -it car_shop_web_1 python manage.py createsuperuser


## Running the tests


    sudo docker exec -it car_shop_web_1 pytest --disable-warnings
