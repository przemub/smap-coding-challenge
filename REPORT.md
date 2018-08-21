Full-stack coding challenge

By Przemysław Buczkowski, 20th/21st of August 2018

* General comments
    * Code is sometimes over-commented in places where I wanted to direct your attention to minor implementation design choices.

* Environment
    * As it turned out, the version of Django specified in requirements.txt is incompatible with Python 3.7 (cf. https://code.djangoproject.com/ticket/28814).
    Not wanting to mess with versions you specified, I compiled and installed Python 3.6 on my system.
    Unless it is intentional, I strongly suggest updating requirements.txt :)

* Models
    * User model named MeterUser to avoid confusion with the built-in User model
    * Consumption stored as a decimal type to ensure accuracy (up to one mWh)
        * The trade-off is lower performance which will be taken care of later.
    * I decided to cache aggregate functions directly in a model to avoid computing
    them in views.

* Import
    * Considering the nature of this project, I opted for a simple implementation utilising
    built-in csv module and Django ORM. Unfortunately it is slow. If we had to import a lot of data, it would be beneficial
    to optimise it - I would use pandas library to import CSV files directly into the database and parallelise the task.
    