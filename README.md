# AI Study Guide Backend

## Instructions
Pick your favorite issue, assign it to yourself, and start working on it. You may select zero (if you really want to) and
more than one issue. See the description of each issue for more details.  
You need to create a new branch for contributing code, you may not change the `master` branch directly. After you finish your work, please create a pull request (PR) and assign me to review it.
Before get started, please also read the following sections. They will give you a better understanding of this project.

## General information
### Project information
This is the backend of the AI Study Guide project. It is a Django REST framework application that provides an API for the frontend application. 

Endpoints:  
- `/api/notes/`: CRUD (create, retrieve, update, delete) operations for notes
- `/api/course/`: CRUD operations for courses
- `/api/subject/{id}/generate-quiz/`: Generate a quiz for a subject

Data model:
- `Note`: Represents a note
  - `title`: The title of the note
  - `content`: The content of the note
  - `course`: The course the note belongs to
- `Course`
  - `name`: The name of the course
  - `instructor`: The instructor of the course
  - `syllabus`: The syllabus of the course (PDF)

### Project structure
This is a standard Django project with Django REST framework. For more details, check out the [Django documentation](https://docs.djangoproject.com/en/stable/) and the [Django REST framework documentation](https://www.django-rest-framework.org/).
- `AI_study_guide_backend/`: Contains project settings, URLs, and other configuration files.
- `notes_analysis/`: This is the application folder, which you'll be interacting with most of the time
- `notes_analysis/models`: This file defines the database models for the application.
- `notes_analysis/views`: This file contains functions/classes that handle HTTP requests and responses.
- `notes_analysis/serializers`: This file defines the serialization logic for the models, which is used to convert complex data types (like Django models) into JSON, and also the other way around.
- `notes_analysis/urls.py`: This file defines the URL routing for the application. It maps URLs to views.
- `notes_analysis/admin.py`: This file defines the admin interface for the application. It allows you to manage the models through a web interface.

### Development environment setup
As a Python project, we have a `requirements.txt` file that lists all the dependencies for the project. You can run `pip install -r requirements.txt` to install all them.  
It's also a good practice to create a virtual environment for the project. See previous announcements in Slack for instructions.  
If you introduce new dependencies, you need add them to the `requirements.txt` file. You can do this by running `pip freeze >> requirements.txt` after installing the new dependencies.

### HTTP and REST basics
Basic understand of HTTP and REST can help you understand what we are doing.  
This YouTube video could be helpful: [A Beginner's Guide to REST APIs in Under 10 Minutes!](https://www.youtube.com/watch?v=LzOtbUw6f_o)  
You could also do some research by yourself. Also, feel free to ask me if you have any questions.

### Database basics
Some basic database knowledge is also helpful. Just need to know what is a database and what foreign key is.
You could search for blog posts or YouTube videos about it.
