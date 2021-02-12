# YOUR PROJECT TITLE
#### Video Demo:  https://youtu.be/pNrTOTJkhlI
#### Description:
My project is a web application that
 - Reads in data on countries (255) from a public API
 - Stores this in a variable inside the web application
 - Selects a country at random and displays 3 metrics on this country (e.g. population, capital, currency)
 - Then the correct country is displayed below
 - The user makes a choice - their score is tracked
 - After 10 questions the users score is presented back to them and they are asked to enter their name
 - After this the final screen is the leaderboard where all previous scores and contestant names are displayed

The files contained in this project are
 - **application.py** Primary application file contain main logic for the quiz
 - **helpers.py** Supporting functions for primary application
 - **quizResults.db** Stores users progress as they move through the quiz, also contains all historical results
 - **/templates** All html screens used in quiz
 - **/static** CSS file and an Icon for the web application