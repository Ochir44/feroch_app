# Feroch-blog-API

This project is a blog where users can add, receive, update and delete posts. All these listed actions of course require registration and user authentication, which is also present in the project. In general, the Feroch-blog project has the basic logic of a blog as a web application.

## Installation and Configuration

To start the project, you need to perform the following steps:

1. Install the necessary packages:
   pip install -r requirements.txt

2. Start server:
   uvicorn main:app --reload

3. Start tests:
   pytest

4. Starting code standardization:
   pre-commit run --all-files

5. Start database postgresql(linux):
   sudo service postgresql start

## So that I would like to finalize it in the project

1. Add docker
2. After confirming the mail (when registering, a link to the website is sent to the mail to confirm it), the account was added to the database.
3. The highlighting of the post update buttons and the post deletion pages also identified a specific user and were shown only to him, and not to strangers.
4. Adding tags when creating a post.
