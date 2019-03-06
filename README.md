# Fruit and Veggie Variety Database

### Completed as Partial Fulfillment of 
### Udacity Full Stack Web Development ND


## About

This database allows a user to view/add/edit/delete food and their varietals in a database. Login authorization is handled via a user's Google account. Any user can add/edit/delete foods (except for a few protected ones), but a user can only edit/delete varieties that they created.

## This project is live on the web!

This can be accessed on the web at:

http://34.223.207.207.xip.io/foods

*If you are a Udacity grader, you can log-in with the following:

`ssh -p 2200 -i <PATH_TO_GRADER_SSH_KEY> ubuntu@34.223.207.207`*

To set this up, I used AWS Lightsail.

I used an instance of Vanilla Ubuntu 16.06 with the following packages installed:

* apache2ctl
* libapache2-mod-wsgi
* python-pip

I also needed to install the python modules specified in requirements.txt.

After that, I checked out my code onto the Lightsail server, and created a wsgi file. The file essentially consists of one line:

`from catalog_project import app as application`

catalog_project is my git code - with the addition of __init__.py, it can be imported as a module.

To get this code working with wsgi, I followed the instructions the in the [Flask documentation](http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/) by adding necessary lines to the file `/etc/apache2/sites-enabled/000-default.conf`:

```
   WSGIScriptAlias / /var/www/html/myapp.wsgi
   WSGIDaemonProcess catalog_project user=<USER_ON_LIGHTSAIL_HERE> \ 
                                     group=<GROUP_ON_LIGHTSAIL_HERE> threads=5
```

(Some information redacted for security information.)

Independent research was very helpful in getting this operating. Flask documentation in particular was great in implementing this project on the instance, AWS documentation for setting up the server, and StackOverflow/man pages all throughout the project to make sure I was employing these commands correctly.

Thanks for checking it out!


**However, if you'd like to run this locally yourself, read on...**


## Prerequisites

In order to run this, you will need to install the following:

* python 2.7 - Programming language
     * Download here: https://www.python.org/downloads/release/python-2712/ ]
     * Excellent installation instructions can be found here:
         * Windows: https://docs.python-guide.org/starting/install/win/#install-windows
         * Mac: https://docs.python-guide.org/starting/install/osx/#install-osx
         * Linux: https://docs.python-guide.org/starting/install/linux/#install-linux
* Virtualbox - Virtual Machine (VM) Program
     * Download here: https://www.virtualbox.org/wiki/Downloads
     * I am VirtualBox version 6.0.2
     * Find your relevant operating system
     * Virtual box also provides installation instructions: https://www.virtualbox.org/manual/ch02.html
* Vagrant - A program for configuring VMs
    * Download here: https://www.vagrantup.com/downloads.html
    * If prompted during installation, grant network permissions to Vagrant.
    * I am using Vagrant version 2.2.2
* You will need many modules - please check the included requirements.txt
    * Run the command below to install these modules:
` pip install -r requirements.txt`

## Setup

### Entering the virtual machine

First start up the needed vagrant machine. You'll need to be in the same directory as your cloned repo. First type

`vagrant up`

which will start up the machine. Then enter the machine with 

`vagrant ssh`

If you enter the command 'whoami' at the prompt and it returns 'vagrant' you're good to go!

### Filling the database

There are two steps needed here. You must first create a database, then fill the database with data.

First, create the needed schema by running

`python models.py`

This will create the tables in the database. Next, populate with some sample data by running

`python add_to_database.py`

The foods that are entered in the database from running this command are protected and cannot be modified. You can however add varieties to these foods or add your own!

## Running the server

You're ready to run the server. Run

`python project.py`

And you should have a server running.

### IMPORTANT:
### The output in your terminal says you can visit http://0.0.0.0:5000/
### You MUST go to http://localhost:5000
### Otherwise, the Google Authentication will not work
### And you will not be able to add your own varieties!

## Needed improvements

There is plenty more that needs to be done here! Here are some ideas:

1. There is currently no way to add characteristics of varieties to the database. You'll have to contact the administrator (that's me!)
2. It would be great to be able to sort by characteristics. This is currently in development.
3. Pretty the website up more. The developer is currently building his CSS skills, and he's proud of getting it looking like this. But there is always more to learn!
