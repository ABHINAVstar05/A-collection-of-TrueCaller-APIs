# A collection of TrueCaller APIs

**All API endpoints are thoroughly tested on Postman**

1.) Create a python virtual environment using below command in terminal

    python -m venv virtual_env

2.) Activate the virtual_env using

    virtual_env/Scripts/Activate

3.) Download the code folder in the same directory.

4.) Open terminal and install dependencies using below command

    python -m pip install -r requirements.txt

5.) Setup a MySQL DB in local system and enter credentials in .env file.

6.) Run migrations using

    python manage.py makemigrations
    python manage.py migrate

7.) Finally, run the local server using below command to run the project in your localhost

    python manage.py runserver