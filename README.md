# GTTD Organizer CLI Bot
GTTD aka helper provides user Address Book, Note Book and Sorter Assist tools

## Installation
For using this tool you have to install Python3.10+ version
To intall, wright in your console:
~~~
pip install GTTD
~~~
For launch the tool, just type:
~~~
helper
~~~

## Address Book

This sublayer is an implementation of an address book that allows users to store and manage contacts. Users can add contacts by providing their name, phone number, email address, birthday, and home address. They can also view all contacts, search for specific contacts by name or phone number, view upcoming birthdays, and update existing contact information.

### Commands
Here are the commands that are available in this sublayer:

- add: Adds a new contact to the address book.
- show all: Shows all contacts in the address book.
- find: Searches for a contact by name or phone number.
- get bith: Shows upcoming birthdays.
- change: Changes an existing contact's information.
- del: Deleted one contact or oll contact in Address Book.
- back: Back to the general menu.


## Notebook

This sublayer is a notebook implementation that allows users to store and manage their notes. Users can add notes by specifying the title name, hashtag, as well as directly the text of the note itself. They can also view all notes, search for specific notes by title or hashtag, and sort notes by the number of hashtags they contain.

### Commands
Here are the commands that are available in this sublayer:

- add: Adds and saved a new note to the notebook
- del: Deleted one note or oll notes in notebook
- change: Changes an existing notes information
- find: Searches for a notes by title or hashtag
- tag sort: Sorts notes by len tags in notebook
- show all: Shows all notes in the notebook
- back: Back to the general menu


## Sorter Assist

This sublayer allows you to sort your trash folder. It normalizes the names of your files, depending on the file extension, decomposes them into folders (images, videos, documents, archives, and others).

### Commands
Here are the commands that are available in this sublayer:

- sort: Runs Sorter Assist itself
- back: Back to the general menu