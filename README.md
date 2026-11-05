# Personal Assistant — Python CLI Application

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/OOP-Object--Oriented%20Programming-lightgrey?style=flat-square)
![CLI](https://img.shields.io/badge/Interface-CLI-black?style=flat-square)
![Pickle](https://img.shields.io/badge/Data%20Persistence-Pickle-yellow?style=flat-square)

## Overview

Personal Assistant is a command-line application for managing a personal contact book. It was developed as an individual Python project and demonstrates object-oriented programming, input validation, exception handling, decorators, date processing, and persistent data storage.

The application allows users to manage contacts and birthdays through simple CLI commands while automatically saving the address book between sessions.

## Tech Stack

- **Programming:** Python
- **Architecture:** Object-Oriented Programming
- **Data Persistence:** Pickle
- **Interface:** Command Line Interface
- **Standard Library:** collections, datetime

## Functionality

The assistant supports the following operations:

- add a new contact and phone number;
- update an existing phone number;
- search for a contact's phone number;
- display all saved contacts;
- add a birthday to a contact;
- show a contact's birthday;
- display birthdays occurring within the next 7 days;
- move weekend birthday congratulations to the next Monday;
- validate phone numbers and birthday formats;
- handle user input errors;
- automatically save and restore the address book between application sessions.

## Available Commands

| Command | Description |
| --- | --- |
| `hello` | Display a greeting |
| `add <name> <phone>` | Add a new contact or phone number |
| `change <name> <old_phone> <new_phone>` | Update a phone number |
| `phone <name>` | Show phone numbers for a contact |
| `all` | Display all contacts |
| `add-birthday <name> <DD.MM.YYYY>` | Add a birthday |
| `show-birthday <name>` | Show a saved birthday |
| `birthdays` | Show upcoming birthdays |
| `close` / `exit` | Save data and exit |

## Project Structure

The project is implemented in a single Python module:

```text
.
├── console-bot.py
├── README.md
└── .gitignore
```

The main classes are:

- **Field** — base class for stored values;
- **Name** — stores a contact name;
- **Phone** — validates and stores phone numbers;
- **Birthday** — validates birthday dates;
- **Record** — represents one contact;
- **AddressBook** — stores and manages contact records.

## Data Persistence

The address book is serialized with Python's `pickle` module and saved to:

```text
addressbook.pkl
```

When the application starts, previously saved contacts are restored automatically. If the file does not exist, a new empty address book is created.

## Running the Application

Clone the repository and run:

```bash
python console-bot.py
```

Then enter commands in the terminal.

## Learning Outcomes

Through this project, I practiced:

- object-oriented application design;
- inheritance and custom classes;
- decorators and exception handling;
- input validation;
- date and time operations;
- serialization and persistent storage;
- building an interactive command-line application.
