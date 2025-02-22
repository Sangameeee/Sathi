# <a href="">Sathi:A  Minimalist Social Network</a>
## Table of Contents 
- [Introduction](#1-introduction) 
-  [Features](#2-features) 
- [Technological Stack](#3-technological-stack) 
- [Frontend Implementation](#4-frontend-implementation) 
-  [Backend Implementation](#5-backend-implementation)
-   [Installation & Setup](#6-installation--setup) 
- [Deployment](#7-deployment) 
-  [Contribution](#8-contribution) 
-  [Contact](#9-contact) 
-  [Troubleshooting](#10-troubleshooting) 
-  [Overview](#11-overview) 
-  [Future Enhancements](#12-future-enhancements)
## 1. Introduction:
<a href = "https://justwriteit.onrender.com/">Sathi</a> is a  minimalistic family and friend focused social network designed to prioritize meaningful connections by focusing exclusively on friends,family and people near and dear to users.Users share updates, photos, views and comments without any algorithmic feed or irrelevant content like reels, videos, Influencers in their feed.Built to foster genuine and relevant interactions without wasting time in irrelevant contents.

## 2. Features:
- **Responsive Design:**:Optimized for both desktop and mobile devices.
- **Privacy-first:** Content visible only to approved connections.
- **Minimalist Design:** Focus on core features(posts, like, comments).
- **Secure Backend and Authentication:** Secure registration/login with Django's built in authentication.
- **Secure Database:** On top of Django's built in migrations postgres database is used for storing datas.

## 3. Technological Stack
- **Backend:** Django(Python)
- **Frontend:** HTML, CSS, Javascript, Bootstrap5
- **Database:** PostgreSQL(hosted on supabase)
- **Deployment:** Render

## 4. Frontend Implementation
- **Responsive Design:** Usage of **Bootstrap5** and css enables the site to be responsive according to screen and works on all kinds of screen desktop/mobile.
## 5. Backend  Implementation
Used Django to implement backend to connect with database make changes, authorize users,etc
**Database: PostgreSQl**
- PostgreSQL is used for its scalability, reliability and gave easier support for website hosting.
- Hosted on **supabase**, for easy database management and real-time capabilities.

## 6. Installation & Setup
1. Clone repository:<br>
	`` git clone https://github.com/Sangameeee/Sathi.git``

2. Create Virtual environment:<br>
``python -m venv venv``

3. Activate virtual environment:<br>
windows:
`` .\venv\Scripts\activate ``
	
	Linux:
``source venv/bin/activate``
4. Install dependencies:<br>
``pip install -r requirements.txt``
5. Create a .env file:<br>
	create a .env file in project location `sathi/.env/`
	```python
	ALLOWED_HOSTS=127.0.0.1 or #no need to specify can be kept empty	
	DATABASE_URL=  #your supabase database url
	GMAIL_ID= #Gmail account which will send forget password mail 
	GMAIL_PASS= #password from googleaccounts center
	DEBUG=True #false when deployment
	S_KEY= #can be any value
	```
	here GMAIL_ID and GMAIL_PASS will require additional google configuration(SMTP credentials) as 
	this gmail sends forget passoword mail to users who forget their password due to google privacy protection so isnt used as of right now.  


6. Setting up database:<br>
	**Local Database:**
	create a postgreSQL database and hostlocally
	ins``blog_project/settings.py``
	
	change databases or remove comment on this code snippet
	```python
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql',
	        'NAME': 'your database name', 
	        'USER': 'database user',   
	        'PASSWORD': 'database password',
	        'HOST': 'localhost',        
	        'PORT': '5432',              
	    }
	}
	```
	**Supabase Database:**
	Create a new project in supabase and copy and paste the database url of supabase inside **DATABASE_URL**  in .env file
7. Database Migrations:<br>
	```python
	python manage.py makemigrations
	python manage.py migrate
	```
8. Database management and PostgreSQL Query:<br>
	After migrations Django default tables will be created in database be it local or supabase from which delete auth_user in cascade
	and run query listed in database_example.txt or listed below:
	```
	CREATE TABLE IF NOT EXISTS auth_user (
	    id SERIAL PRIMARY KEY,
	    password VARCHAR(128) NOT NULL,
	    last_login TIMESTAMPTZ,
	    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
	    username VARCHAR(150) UNIQUE NOT NULL,
	    first_name VARCHAR(30),
	    last_name VARCHAR(30),
	    email VARCHAR(254) UNIQUE NOT NULL,
	    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
	    is_active BOOLEAN NOT NULL DEFAULT TRUE,
	    date_joined TIMESTAMPTZ DEFAULT NOW()
	);

	CREATE TABLE IF NOT EXISTS blog_post (
	    id SERIAL PRIMARY KEY,
	    title VARCHAR(100) NOT NULL,
	    image VARCHAR(255),
	    visibility VARCHAR(20) DEFAULT 'public',
	    date_posted TIMESTAMPTZ DEFAULT NOW(),
	    author_id INTEGER NOT NULL,
	    CONSTRAINT fk_author FOREIGN KEY (author_id)
	        REFERENCES auth_user(id) ON DELETE CASCADE
	);

	CREATE TABLE IF NOT EXISTS users_profile (
	    id SERIAL PRIMARY KEY,
	    user_id INTEGER UNIQUE NOT NULL,
	    image VARCHAR(255) DEFAULT 'profile_pics/default.jpg',
	    CONSTRAINT fk_user FOREIGN KEY (user_id)
	        REFERENCES auth_user(id) ON DELETE CASCADE
	);


	CREATE TABLE IF NOT EXISTS friends (
	    id SERIAL PRIMARY KEY,
	    user1_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
	    user2_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
	    status VARCHAR(20) NOT NULL DEFAULT 'pending',
	    created_at TIMESTAMPTZ DEFAULT NOW(),
	    UNIQUE(user1_id, user2_id)
	);


	CREATE TABLE IF NOT EXISTS post_likes (
	    id SERIAL PRIMARY KEY,
	    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
	    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
	    created_at TIMESTAMPTZ DEFAULT NOW(),
	    UNIQUE(user_id, post_id)
	);

	CREATE TABLE IF NOT EXISTS post_comments (
	    id SERIAL PRIMARY KEY,
	    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
	    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE,
	    content TEXT NOT NULL,
	    created_at TIMESTAMPTZ DEFAULT NOW()
	);
	```
9. Start server:<br>
	```python
	python manage.py runserver
	``` 
## 7. Deployment
- Deployed using  Render
- Used whitenoise for static files 
- In settings.py configure ``DEBUG=FALSE``

## 8. Contribution
- Fork the repository 
- Create a new branch 
- Submit pull requests with clear descriptions

## 9. Contact
- for support, send mail at: sangamparajuli99@gmail.com
- Send message at:<a href = "https://www.sangamparajuli.com.np/contactme">Message</a>
## 10. Troubleshooting 
- **Static files not loading:** Run ``python manage.py collectstatic``
- **Database connection issues:** Check if .env file is properly sending data and verify credentials in ``settings.py``

## 11. Overview
**Site link = <a href = "https://justwriteit.onrender.com/">Sathi</a><br>**
Screenshot of mobile and laptop is shown below:<br>
**Mobile View:** <br>
![Mobile Screenshot](https://github.com/Sangameeee/Sathi/blob/main/mobile%20ss.png?raw=true)
<br><br>**Desktop View:** <br>
![Mobile Screenshot](https://github.com/Sangameeee/Sathi/blob/main/desktop%20ss.png?raw=true)


## 12. Future Enhancements
- Error fixes and more smooth transitions
- Image privacy and image upload in cloud
- Direct messaging between users
- Photo albums/collages 
- Real time notifications
