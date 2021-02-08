## Note App
___
***A simple web based note taking application with markdown support***

Note app is a server-side rendered app written with Python Django. It allow you to take notes
with markdown language support. You could preview markdown live while you are editing. You can save them,
edit them, or delete them if you want.

### Screenshots
___
![App page](/assets/notes_app.png)

![Mobile_app page](/assets/notes_app_mobile.png)

### Features
___

* **Markdown** live preview
* Allows **tagging** the notes for easier classification
* Allows **searching** within notes and titles 
* Mobile responsiveness

### Getting Started
___
To get started application, run the following commands in a virtual environment:

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Built With
___
* Python Django version 3.1.3 
* Bootstrap v4.5.3
* Django Crispy Forms v1.10.0, Django Markdownx v3.0.1, and Django Taggit v1.3.0
* SQLite 3

### Author
___
* Halil Can Uğur

### Licence
___
This project is open source and available under the MIT License [MIT Licence](https://github.com/hcugur/notes-app/blob/main/LICENSE)
