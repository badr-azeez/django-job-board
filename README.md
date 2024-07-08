# Django Job Board
Job Board is a web application has job posting and blog system, allow users post job and interact with blog posts.
## Features

The project consists of 5 main apps:

### 1. Accounts
- User registration and login
- Profile management
- User can create and update their account
- User can add experiences to their profile

### 2. Blog
- Admin can post articles with categories and tags
- Superusers can create, edit, update, and delete posts
- Users can filter posts
- Users can comment on posts

### 3. Jobs
- Users can post jobs
- Users can view posted jobs
- Users can view jobs they've applied to
- Job posters can view applicants for their jobs
- Both registered users and non-users can apply for jobs

### 4. Home
- Main landing page of the website
- Features a job search functionality
- Displays popular job categories
- Showcases top 6 job listings

### 5. Contact
- Provides a contact form for anyone to send messages to the website administrators

## Video Usage
[![Watch the video](https://i.ibb.co/JnxKLNN/full-video-Cover.jpg)](https://www.youtube.com/watch?v=oWY2uQypCiM)

## Installation

```sh
git clone https://github.com/badr-azeez/django-job-board.git
cd  django-job-board
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip  install -r requirements.txt
#run
python manage.py runserver
```
### admin credit
```
username : admin
password : admin
```
## License

Apache 2.0 License
