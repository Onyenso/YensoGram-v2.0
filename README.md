# YensoGram v2.0

An updated version of <a href="https://github.com/Onyenso/YensoGram" target="blank">YensoGram</a>, built with Django and JavaScript. This project was created as a result of the requirement to complete [Harvard University's CS50W Final Project](https://cs50.harvard.edu/web/2020/projects/final/capstone/). YensoGram is basically a web application that allows a user to send instant messages in form of chats to other users and make posts with pictures.

## Project Description

Unilke its previous version, it allows the ability to send messages instantly. The greatest challenge was making it possible for any message to appear immediately on an other user's browser. This was made possible with the JavaScript found in <a href="https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/yensogram/static/yensogram/messages.js">messages.js</a>. Also, posts can now contain pictures.

When a new user signs up, the user will have no friends and thus no posts to be seen. The application allows the user to find other users by sending them friend requests. The user is allowed the ability to accept and decline any friend request. When the user makes a post, it will be visible to other users who are friends with him/her and vice versa.

## Why this project?
I did this project because I had already done a previous version of it for the [Final Project of CS50x](https://cs50.harvard.edu/x/2020/project/) and it gave me a sense of achievement when it featured on the gallery of final projects. The previous version lacked the instant messaging feature because every request was processed server-side and hence it was seen as "boring" by critiques. It also lacked the ability to post media. It only made sense to continue on this project by making it better for CS50W, especially seeing as I have acquired knowledge of JavaScript.

In this project,

- [yensogram-v2.0](https://github.com/Onyenso/YensoGram-v2.0/tree/main/yensogram-v2.0) is the folder that holds the entire project.
- [yensogram-v2.0/db.sqlite3](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/db.sqlite3) is the database for the project.
- [yensogram-v2.0/media](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/media) is the folder that holds uploaded media from users.
- [yensogram-v2.0/static](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/static) holds the static files for the project.
- [yensogram-v2.0/yensogram/templates/yensogram](https://github.com/Onyenso/YensoGram-v2.0/tree/main/yensogram-v2.0/yensogram/templates/yensogram) holds frontend HTML files.
- [yensogram-v2.0/yensogram/forms.py](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/yensogram/forms.py) hold the forms used in the application.
- [yensogram-v2.0/yensogram/models.py](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/yensogram/models.py) hold the models used in the application.
- [yensogram-v2.0/yensogram/urls.py](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/yensogram/urls.py) are the urls for the application.
- [yensogram-v2.0/yensogram/views.py](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/yensogram/views.py) hold the functions used to process requests to the urls.

## What's New
- Intuitive form error feedback on registration and login
- Instant messaging
- Posts with media
- Removed "title" field from posts

## Usage

- Install Python and Django.
- Install the Python packages in the [requirements.txt](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/requirements.txt) file using pip install.
- In your terminal or command line, navigate to the folder where [yensogram-v2.0/manage.py](https://github.com/Onyenso/YensoGram-v2.0/blob/main/yensogram-v2.0/manage.py) lives.
- Then, you can run the program by running:
```
$  python manage.py runserver
```
## Video demonstration
- https://www.youtube.com/watch?v=BiTGvADB9cs

## Creator

Onyenso Uchenna J.

- https://onyenso.github.io/yensodev
- [Twitter](https://twitter.com/Yensodev)
- [Linkedin](https://linkedin.com/in/onyenso)
