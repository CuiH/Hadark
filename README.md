### dependencies:
```
pip install django
pip install djangorestframework
apt-get install libmysqld-dev
apt-get install python-dev
pip install mysql-python
pip install django-cors-headers
pip install PyMysql
```

---

### pre works
```
mysql> create database hadark;
python manage.py migrate
mysql> insert into file(name, file_type, permission) values("/", "directory", "none");
mysql> insert into file(name, file_type, permission, parent_id) values("user", "directory", "none", 1);  -- the parent_id should be the id of the above item
---

### run:
```
python manage.py runserver
``` 
