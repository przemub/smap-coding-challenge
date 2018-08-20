Full-stack coding challenge

By Przemysław Buczkowski, 20th of August 2018

* Models
    * User model named MeterUser to avoid confusion with built-in User model
    * Consumption stored as a decimal type to ensure accuracy (up to one mWh)
        * The trade-off is lower performance which will be taken care of later.