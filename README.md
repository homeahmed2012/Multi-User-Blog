# Multi User Blog


### about
this is a multi user blog made using google app engine as the third project in `full stack web developer nano degree` program by `Udacity`.

### Usage
to run the blog locally you should first install google app engine then clone the repository:
``` bash
git clone https://github.com/homeahmed2012/Multi-User-Blog.git
```
then go inside the project directory and open the terminal then write:
``` bash
dev_appserver.py .
```
the open the browser and go to http://localhost:8000

or you can just use it online by go to

### Files

there are 4 python files:
1. `main.py`: the main file to run the blog it contains all handler classes.
2. `sec.py` : contains the methods that hash the password and the cookies.
3. `entities.py` : it contains the entities for blog, user, and comment it contains also some helper functions to work with datastore.
4. `helper.py` : contains some helper methods to validate user information.

and ther are the template html files for the blog in templates directory with the css files.
