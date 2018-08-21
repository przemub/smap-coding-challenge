Full-stack coding challenge

By Przemysław Buczkowski, 20th/21st of August 2018

* General comments
    * Code is sometimes over-commented in places where I wanted to direct your attention to minor implementation design choices.
    * In production I would use a local copy of all external stylesheets and scripts but I didn't want to clutter the repository.

* Environment
    * As it turned out, the version of Django specified in requirements.txt is incompatible with Python 3.7 (cf. https://code.djangoproject.com/ticket/28814).
    Not wanting to mess with versions you specified, I compiled and installed Python 3.6 on my system.
    Unless it is intentional, I strongly suggest updating requirements.txt :)

* Models
    * User model named MeterUser to avoid confusion with the built-in User model
    * Consumption stored as a decimal type to ensure accuracy (up to one mWh)
        * The trade-off is lower performance which will be taken care of by caching.

* Import
    * Considering the nature of this project, I opted for a simple implementation utilising
    built-in csv module and Django ORM. Unfortunately it is slow. If we had to import a lot of data, it would be beneficial
    to optimise it - I would use pandas library to import CSV files directly into the database and parallelise the task.
    * There is a mantra I heard a long time ago and it stuck with me - *If you need more than 3 levels of indentation, you’re screwed anyway, and should fix your program.*
    Therefore this part of code seems completely off to me. But on the other hand, *There should be one-- and preferably only one --obvious way to do it.*
    And the solution seemed obvious when I wrote it. But I'm not Dutch, even though I'm tall, so how could I know… Eh, who would expect that a requirement project would give me an
    existential crisis…

    