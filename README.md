# Image  Uploader
A Project that every beginner must do by himself/herself to get started with Python Web-development

### Flow Diagram 

![Flow Diagram](https://github.com/Samrat002/ImageUploader/blob/master/flow_diagram.png) 


### Project Description
It contains an User Interface which contains an Image Uploader Widgets. The widget takes 3 parameters:-
    
    1) Image Blob Object
    2) Caption for the Image
    3) Resolution
    
It is mandatory to upload a image of resolution of 1024 X 786.
Upon successful upload , In backend it saves the image blob object in the model with details as follows:-

    1) Caption
    2) Height
    3) Width
    4) Image Quality 
    5) Blob object
    6) cloud URL
    
In current system , ``Image Quality `` can be of 4 types:-
    
    1) Very High (1024px x 1024px)
    2) High (1024px x 786px)
    3) Medium (786px x 786px)
    4) Low (124px x 124 px)
    
On successful validation of the image , A new copy image is created and processed to create the HIgh Quality Image
and uploaded to S3 in sync .
All the other 3 image Quality type is initiated in Async using celery Task using workers. 
This returns a response of success and the cloud url so that it can be rendered. 

### MOTIVE
    a) This is a simple mini project that i carried out at the beginning when i was trying to get deep hands on with the Django
       Framework.
       
    b) This project is completely build on django which uploads the image of specific size processes 
       it and creates 4 different images via Processing through PIL .

### PERKS FROM PROJECT 
    a) Simple hand on tool to get started with python and Django Framework
    b) Small Hands on work with  ***Celery***,  ***Redis Cache***, ***S3*** and ***Consistant Hashing***.
    
### Installing and Running Project in Local
   1) clone the repository in your system 
    
        ```git clone git@github.com:Samrat002/ImageUploader.git```
        
   2) Make your AWS free Account and add pass key in the non added settings.py file of the project\
   3) Go to the shell and run
      `python manage.py runserver`
      
~~Boom On !!! ~~~

### Scope of Enhancement
    1) Dockerization
    2) Proper credential service requied / Which can be built to store the Keys and Password
    3) This imageUploader can be integrated with the user management for leverage the scope.