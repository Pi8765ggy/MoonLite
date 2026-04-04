## About
  MoonLite is an interface for the AstronomyAPI to query data about the moon at a specific date and time.
  It also has an included database and user login system through Google's OAuth for future use.
  Using MoonLite, a user can:
  - Input their longitude and latitude (which is NEVER stored on the server database.)
  - Input a date and time
  - Recieve data about the moon for that specific date and time, including position in the sky and an image of the phase.
  
## Steps to installing and running MoonLite (Linux):
1. Make sure python's venv is installed, along with npm.
2. Run the build.sh script included in the repository. (Or, if you don't trust me, run it line by line).
  - Note: This command will scrub the database. Do not build the app again if you want the database to persist.
3. Create a .env file following the included envBlank format.
	- SECRET_KEY: A random, secret key for the flask application. Keep it secure!
	- CLIENT_SECRET: Google OAuth client secret
	- CLIENT_ID: Google OAuth client ID
	- ASTRONOMY_SECRET: AstronomyAPI secret
	- ASTRONOMY_ID: AstronomyAPI ID
	- UCD_LAT / UCD_LONG: Originally the location of UC Davis. Change to a vaild float for a default latitude and longitude when the page loads.
4. Activate the python venv with:
    - source .venv/bin/activate
5. Run the application from the root folder, using the flask command: 
	- flask --app moonlite run --cert=adhoc --debug 
6. Go to https://127.0.0.1:5000 to access the app.
    
## Tech Stack
MoonLite utilizes Vue, Flask, and SQLite for its execution.
It follows a semi-RESTful API structure, where the user "logged-in" state is stored on the server.

## Video Demo
https://youtu.be/4qMDgV5V9JU
Other than that, Flask only serves as a backend API to be queried by Vue on the frontend.
It utilizes basic GET requests and url parameters to recieve information.

SQLite is used to store user data as returned by Google's OAuth flow.
This data can then be queried by Vue to show the user's profile picture and verify if they are logged in.
