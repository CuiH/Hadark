### dependencies:
```
pip install django
pip install djangorestframework
apt-get install libmysqld-dev
apt-get install python-dev
pip install mysql-python
pip install django-cors-headers
```

---

### pre works
1. add a File object values(name="/", file_type="directory", parent="None")
2. add a File object values(name="user", file_type="directory") and its parent should be the above one

---

### run:
```
python manage.py migrate
python manage.py runserver
``` 
