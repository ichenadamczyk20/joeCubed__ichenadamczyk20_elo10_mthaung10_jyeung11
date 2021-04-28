# Ample Examples by Team Joe Cubed
## Roster
* Ian Chen-Adamczyk (Project Manager)
    * API, Flask, HTML, __JavaScript__, __Markdown__
* Eric Lo
    * Bootstrap, __DB__, Flask, HTML, JavaScript
* Michelle Thaung
    * __Bootstrap__, DB, HTML
* Jessica Yeung
    * __API__, CSS, Flask, HTML
## Description
A website to contain lists about topics, meant to serve as creative inspiration. Users can log in to favorite items on lists as well. Currently only two lists are implemented, one about dog breeds and one about tropical fruits and vegetables. There is also a random image generator in case you know your topic but need an image for it.

Implemented using Flask, Python 3, SQLite, HTML, CSS, JavaScript, Bootstrap, and various RESTful APIs.

## APIs Used:
- DogCEO: https://github.com/stuy-softdev/notes-and-code20-21/blob/master/api_kb/411_on_DogCEO.md
- TropicalFruitandVeg: https://github.com/stuy-softdev/notes-and-code20-21/blob/master/api_kb/411_on_TropicalFruitandVeg.md
- MediaWiki: https://github.com/stuy-softdev/notes-and-code20-21/blob/master/api_kb/411_on_MediaWikiAPI.md

## Launch codes
1. Clone this repository: 
`git clone https://github.com/ichenadamczyk20/joeCubed__ichenadamczyk20_elo10_mthaung10_jyeung11.git`
2. Go to the folder containing the app:
`cd joeCubed__ichenadamczyk20_elo10_mthaung10_jyeung11`
3. Install the required modules:
`pip install -r requirements.txt`
4. Run dbsetup.py (from outside the app folder):
`python app/dbsetup.py`
5. Run \__init\__.py (from outside the app folder):
`python app/__init__.py`