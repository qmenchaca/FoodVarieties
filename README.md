# Fruit and Veggie Variety Database

### Completed as Partial Fulfillment of 
### Udacity Full Stack Web Development ND


## About

This database allows a user to view/add/edit/delete food and their varietals in a database. Login authorization is handled via a user's Google account. Any user can add/edit/delete foods (except for a few protected ones), but a user can only edit/delete varieties that they created.

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
