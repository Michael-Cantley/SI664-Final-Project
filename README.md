`Final-Project app
The final-project app is used in SI 664, a University of Michigan, School of Information course, to explore both the Django web framework and a MySQL database composed of video game data sales available on Kaggle.


# Project Name
Video Game Sales Final Project

## Purpose
After the initial proposal and feedback, I have decided to build a Django app that reflects my interests in data pertaining to video games. My goals for this project are to structure the data regarding video game sales across regions, practice constructing tables that uphold the normal forms discussed in class, design a Django app with a clean user experience, and include an authentication pathway that allows users to log in and perform more/unique interactions within the Django app.

## Data Set
The data set that will be used for this project can be found on Kaggle at the following link: (https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings). This data is a summary of video game sales across the world, primarily broken down into four regions of sales. The data includes video games from across platforms, genres of games, and years of release and allows users to view several attributes related to a given video game's sales.

## Data Model

![Video Game Sales](https://github.com/Michael-Cantley/SI664-Final-Project/blob/master/static/img/complete_video_game_sales.PNG)

The data model can be found under /static/img in this repository. Please look at and review this model to learn about the intended database structure.
It is noted that this model is intended to fulfill the normal form requirements.

 To fulfill the first normal form, I have attempted to create domains that only contain atomic values. To fulfill the second normal form, I have put the non-key attributes in tables that they are completely dependent on that tables primary key. Finally, the third normal form is fulfilled by keeping non-key attributes contained to their primary key tables. These normal forms are considered when creating the logical model and when analyzing the data sets. The model is created to reflect the concepts of no data duplication and upholding referential integrity in the logical model.

 Lastly, for the project requirements, I would do the M2M relationship by using the ‘game-sale-region’ setup and look to display the data by video game initially and then look to make a by region display, similar to the sites + countries displays in our heritage sites app. I would investigate/create more fields to make the region displays more informative. I am planning on including “total sales” and “most popular developer” as new fields for each region. 


## Package Dependencies
Please refer to:
https://github.com/Michael-Cantley/SI664-Final-Project/blob/master/requirements.txt

certifi==2018.10.15
chardet==3.0.4
coreapi==2.3.3
coreschema==0.0.4
defusedxml==0.5.0
Django==2.1.2
django-allauth==0.38.0
django-cors-headers==2.4.0
django-crispy-forms==1.7.2
django-filter==2.0.0
django-rest-auth==0.9.3
django-rest-swagger==2.2.0
django-test-without-migrations==0.6
djangorestframework==3.9.0
idna==2.7
itypes==1.1.0
Jinja2==2.10
MarkupSafe==1.1.0
mysqlclient==1.3.13
oauthlib==2.1.0
openapi-codec==1.3.2
PyJWT==1.6.4
python3-openid==3.1.0
pytz==2018.5
PyYAML==3.13
requests==2.20.0
requests-oauthlib==1.0.0
simplejson==3.16.0
six==1.11.0
social-auth-app-django==3.0.0
social-auth-core==2.0.0
uritemplate==3.0.0
urllib3==1.24
