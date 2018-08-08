# ezra - the ez roster assistant

ezra is a scheduling app for Cornell that knows (or will know) about degree
requirements. Here's a summary of where the project stands as of 7 August 2018.

The /apicode folder contains the Python code responsible for interacting with
the Scheduler API detailed [here](https://classes.cornell.edu/content/SP18/api-details).
This code is called by the Flask app when server requests are made.

/static contains folders for Javascript and CSS files. The file index.js
currently contains all the Javascript responsible for the dynamic behavior of
the web interface.

app.py contains the entirety of the Flask code. As the project grows, I will
likely adopt a more conventional and more complex directory structure.

Currently, the web interface can successfully interact with the Python code base
and display class information on the schedule. I plan to focus next on some code
review and refactoring, of both the server-side and client-side code. After
that, I would like to work on improving the web display, and then on adding the
degree requirement functionality.
