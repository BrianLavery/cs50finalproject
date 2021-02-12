import requests
import random
from cs50 import SQL
from flask import Flask, render_template, request, redirect
from tempfile import mkdtemp
from helpers import km2, num, apology


# Configure application
app = Flask(__name__)



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quizResults.db")



# Calls APIs and store data within a variable
url_countries = "https://restcountries.eu/rest/v2/all"
countries = requests.get(url_countries).json()

# Create a dictionary with country codes and country names
ctryNameDict = {}
for i in range(len(countries)):
    ctryName = countries[i]['name']
    ctryCode = countries[i]['alpha3Code']
    ctryNameDict[ctryCode] = ctryName



# Home page - render a webpage
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")



# Quiz - begins the quiz sequence
@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    # Create logic flow for when click on the "Quiz" link
    if request.method == "GET":

        # Clear table in results
        db.execute("DELETE FROM results;")
        db.execute("DELETE FROM countries;")

        # Set quiz round as the first round
        currRound = 1

        # Select a random country list for these 10 Questions for this contestant amongst list of countries
        totalCtrs = len(countries)
        numCtrsList = list(range(0,totalCtrs))
        numCtrs = random.sample(numCtrsList, k=10, counts=None)
        numCtry = numCtrs[0]

        # Store these 10 countries into countries table in the database
        for i in range(len(numCtrs)):
            countryNumber = numCtrs[i]
            countryName = countries[countryNumber]['name']
            db.execute("INSERT INTO countries (round, countryNumber, countryName) VALUES (:round, :countryNumber, :countryName)",
                        round = i + 1, countryNumber=countryNumber, countryName=countryName)

        # Set metrics for correct country as variables
        ctryName = countries[numCtry]['name']
        ctryCapital = countries[numCtry]['capital']
        ctryFlagLink = countries[numCtry]['flag']

        # Format population when stored
        ctryPopulation = num(countries[numCtry]['population'])

        # For area do a check that is not null
        if not countries[numCtry]['area']:
            ctryArea = "N/A"
        else:
            ctryArea = km2(int(countries[numCtry]['area']))

        # Keep printing out country name to make error checking easier
        print(f"ctryName = {ctryName}")

        # Set metrics for those variables within a list where could keep multiple variables
        ctryBordersListCodes = countries[numCtry]['borders']
        ctryTimesList = countries[numCtry]['timezones']

        # Convert Borders List into country names not country codes
        ctryBordersList = []
        for i in ctryBordersListCodes:
            ctry = ctryNameDict[i]
            ctryBordersList.append(ctry)

        # Adjust metrics inside lists to get string variables I can pass into html
        ctryBorders = ", ".join(ctryBordersList)
        ctryTimes = ", ".join(ctryTimesList)

        # Set language info to variable which will be a list of dictionaries
        ctryLangListDict = countries[numCtry]['languages']

        # initialise separate lists for native languages (hard) and those in English language (easy)
        ctryLangList = []
        ctryLangNatList = []

        # Add values into the lists
        for i in range(len(ctryLangListDict)):
            ctryLangList.append(ctryLangListDict[i]['name'])
            ctryLangNatList.append(ctryLangListDict[i]['nativeName'])

        # Set Currencies info to variable which can be a list of dictionaries
        ctryCurrCode = countries[numCtry]['currencies']

        # Add values into a list
        ctryCurrList = []
        for i in range(len(ctryCurrCode)):
            ctryCurrList.append(str(ctryCurrCode[i]['code']))

        # Convert lists info into comma-separated strings
        ctryLang = ", ".join(ctryLangList)
        ctryNatLang = ", ".join(ctryLangNatList)
        ctryCurr = ", ".join(ctryCurrList)

        # Create 2 dictionaries one with harder metrics, one with easier
        ctryAnsListEasy = {'Capital': ctryCapital, "Languages": ctryLang, 'Flag': ctryFlagLink}
        ctryAnsListHard = {'Population': ctryPopulation, 'Area': ctryArea, 'Timezones': ctryTimes, 'Bordering countries': ctryBorders}
        ctryAnsListHard.update({'Languages (native)': ctryNatLang, "Currencies": ctryCurr})

        # Create a dictionary to allow me to randomly select a dictionary key-value pair from the Answer Dictionaries
        easyDict = {'1': 'Capital', '2': 'Languages', '3': "Flag"}
        hardDict = {'1': 'Population', '2': 'Area', '3': 'Timezones', '4': 'Bordering countries', '5': 'Languages (native)', '6': 'Currencies'}

        # Create my random selectors
        easyNum = random.randint(1,2)
        hardNum1 = random.randint(1,6)

        # Create a while statement to ensure hardNum1 and hardNum2 are different
        increment = 1
        while increment > 0:
            hardNum2 = random.randint(1,6)
            if hardNum2 != hardNum1:
                break

        # Select relevant Keys and set to metric names
        metricName1 = easyDict[str(easyNum)]
        metricName2 = hardDict[str(hardNum1)]
        metricName3 = hardDict[str(hardNum2)]

        # Select relevant values (these will become metrics)
        metric1 = ctryAnsListEasy[metricName1]
        metric2 = ctryAnsListHard[metricName2]
        metric3 = ctryAnsListHard[metricName3]

        # Select random other countries making sure they are not the same as correct answer country
        increment = 1
        while increment > 0:
            numCtry2 = random.randint(0, totalCtrs - 1)
            if numCtry2 != numCtry:
                break

        while increment > 0:
            numCtry3 = random.randint(0, totalCtrs - 1)
            if numCtry3 != numCtry and numCtry3 != numCtry2:
                break

        while increment > 0:
            numCtry4 = random.randint(0, totalCtrs - 1)
            if numCtry4 != numCtry and numCtry4 != numCtry2 and numCtry4 != numCtry3:
                break

        # Store country names as variables
        ctryName2 = countries[numCtry2]['name']
        ctryName3 = countries[numCtry3]['name']
        ctryName4 = countries[numCtry4]['name']

        # Create a dict so that can select random country variables
        ctryDict = {'1': ctryName, '2': ctryName2, '3': ctryName3, '4': ctryName4}

        # Generate random order to display countries
        order1 = random.randint(1,4)

        while increment > 0:
            order2 = random.randint(1,4)
            if order2 != order1:
                break

        while increment > 0:
            order3 = random.randint(1,4)
            if order3 != order1 and order3 != order2:
                break

        while increment > 0:
            order4 = random.randint(1,4)
            if order4 != order1 and order4 != order2 and order4 != order3:
                break

        # Set randomised country values
        country1 = ctryDict[str(order1)]
        country2 = ctryDict[str(order2)]
        country3 = ctryDict[str(order3)]
        country4 = ctryDict[str(order4)]

        # Store answer in results table
        db.execute("INSERT INTO results (round, answer, countryNumber) VALUES (:round, :answer, :countryNumber)"
                    , round = currRound, answer=ctryName, countryNumber=numCtry)

        return render_template("quiz.html", metricName1=metricName1, metricName2=metricName2, metricName3=metricName3,
                            metric1=metric1, metric2=metric2, metric3=metric3,
                            country1=country1, country2=country2, country3=country3, country4=country4)


    # Create logic flow for when submitted via POST
    else:

        # Find answer user submitted
        if request.form.get("option1") != None:
            response = request.form.get("option1")
        elif request.form.get("option2") != None:
            response = request.form.get("option2")
        elif request.form.get("option3") != None:
            response = request.form.get("option3")
        else:
            response = request.form.get("option4")

        # Extract last round from SQL database
        lastRoundDict = db.execute("SELECT max(round) FROM results;")
        lastRound = lastRoundDict[0]['max(round)']

        # Extract answer from SQL database
        answerDict = db.execute("SELECT answer FROM results WHERE round = :quizRound", quizRound=lastRound)
        answer = answerDict[0]['answer']

        # Update whether respondent got answer correct or not
        if response == answer:
            db.execute("UPDATE results SET correct = 1 WHERE round = :quizRound", quizRound=lastRound)
        else:
            db.execute("UPDATE results SET correct = 0 WHERE round = :quizRound", quizRound=lastRound)

        # Update quiz round
        currRound = lastRound + 1

        # Select next country from randomly generated list
        numCtryDict = db.execute("SELECT countryNumber FROM countries WHERE round = :quizRound", quizRound=currRound)
        print(currRound)
        print(numCtryDict)
        numCtry = numCtryDict[0]['countryNumber']

        # Set metrics for correct country as variables
        ctryName = countries[numCtry]['name']
        ctryCapital = countries[numCtry]['capital']
        ctryFlagLink = countries[numCtry]['flag']

        # Format population when stored
        ctryPopulation = num(countries[numCtry]['population'])

        # For area do a check that is not null
        if not countries[numCtry]['area']:
            ctryArea = "N/A"
        else:
            ctryArea = km2(int(countries[numCtry]['area']))

        # Keep printing out country name to make error checking easier
        print(f"ctryName = {ctryName}")

        # Set metrics for those variables within a list where could keep multiple variables
        ctryBordersListCodes = countries[numCtry]['borders']
        ctryTimesList = countries[numCtry]['timezones']

        # Convert Borders List into country names not country codes
        ctryBordersList = []
        for i in ctryBordersListCodes:
            ctry = ctryNameDict[i]
            ctryBordersList.append(ctry)

        # Adjust metrics inside lists to get string variables I can pass into html
        ctryBorders = ", ".join(ctryBordersList)
        ctryTimes = ", ".join(ctryTimesList)

        # Set language info to variable which will be a list of dictionaries
        ctryLangListDict = countries[numCtry]['languages']

        # initialise separate lists for native languages (hard) and those in English language (easy)
        ctryLangList = []
        ctryLangNatList = []

        # Add values into the lists
        for i in range(len(ctryLangListDict)):
            ctryLangList.append(ctryLangListDict[i]['name'])
            ctryLangNatList.append(ctryLangListDict[i]['nativeName'])

        # Set Currencies info to variable which can be a list of dictionaries
        ctryCurrCode = countries[numCtry]['currencies']

        # Add values into a list
        ctryCurrList = []
        for i in range(len(ctryCurrCode)):
            ctryCurrList.append(str(ctryCurrCode[i]['code']))

        # Convert lists info into comma-separated strings
        ctryLang = ", ".join(ctryLangList)
        ctryNatLang = ", ".join(ctryLangNatList)
        ctryCurr = ", ".join(ctryCurrList)

        # Create 2 dictionaries one with harder metrics, one with easier
        ctryAnsListEasy = {'Capital': ctryCapital, "Languages": ctryLang, 'Flag': ctryFlagLink}
        ctryAnsListHard = {'Population': ctryPopulation, 'Area': ctryArea, 'Timezones': ctryTimes, 'Bordering countries': ctryBorders}
        ctryAnsListHard.update({'Languages (native)': ctryNatLang, "Currencies": ctryCurr})

        # Create a dictionary to allow me to randomly select a dictionary key-value pair from the Answer Dictionaries
        easyDict = {'1': 'Capital', '2': 'Languages', '3': "Flag"}
        hardDict = {'1': 'Population', '2': 'Area', '3': 'Timezones', '4': 'Bordering countries', '5': 'Languages (native)', '6': 'Currencies'}

        # Create my random selectors
        easyNum = random.randint(1,2)
        hardNum1 = random.randint(1,6)

        # Create a while statement to ensure hardNum1 and hardNum2 are different
        increment = 1
        while increment > 0:
            hardNum2 = random.randint(1,6)
            if hardNum2 != hardNum1:
                break

        # Select relevant Keys and set to metric names
        metricName1 = easyDict[str(easyNum)]
        metricName2 = hardDict[str(hardNum1)]
        metricName3 = hardDict[str(hardNum2)]

        # Select relevant values (these will become metrics)
        metric1 = ctryAnsListEasy[metricName1]
        metric2 = ctryAnsListHard[metricName2]
        metric3 = ctryAnsListHard[metricName3]

        # Select random other countries making sure they are not the same as correct answer country
        totalCtrs = len(countries)

        increment = 1
        while increment > 0:
            numCtry2 = random.randint(0, totalCtrs - 1)
            if numCtry2 != numCtry:
                break

        while increment > 0:
            numCtry3 = random.randint(0, totalCtrs - 1)
            if numCtry3 != numCtry and numCtry3 != numCtry2:
                break

        while increment > 0:
            numCtry4 = random.randint(0, totalCtrs - 1)
            if numCtry4 != numCtry and numCtry4 != numCtry2 and numCtry4 != numCtry3:
                break

        # Store country names as variables
        ctryName2 = countries[numCtry2]['name']
        ctryName3 = countries[numCtry3]['name']
        ctryName4 = countries[numCtry4]['name']

        # Create a dict so that can select random country variables
        ctryDict = {'1': ctryName, '2': ctryName2, '3': ctryName3, '4': ctryName4}

        # Generate random order to display countries
        order1 = random.randint(1,4)

        while increment > 0:
            order2 = random.randint(1,4)
            if order2 != order1:
                break

        while increment > 0:
            order3 = random.randint(1,4)
            if order3 != order1 and order3 != order2:
                break

        while increment > 0:
            order4 = random.randint(1,4)
            if order4 != order1 and order4 != order2 and order4 != order3:
                break

        # Set randomised country values
        country1 = ctryDict[str(order1)]
        country2 = ctryDict[str(order2)]
        country3 = ctryDict[str(order3)]
        country4 = ctryDict[str(order4)]

        # Store answer in results table
        db.execute("INSERT INTO results (round, answer, countryNumber) VALUES (:round, :answer, :countryNumber)"
                    , round = currRound, answer=ctryName, countryNumber=numCtry)

        if currRound < 10:
            return render_template("quiz.html", metricName1=metricName1, metricName2=metricName2, metricName3=metricName3,
                            metric1=metric1, metric2=metric2, metric3=metric3,
                            country1=country1, country2=country2, country3=country3, country4=country4)
        else:
            return render_template("finalquiz.html", metricName1=metricName1, metricName2=metricName2, metricName3=metricName3,
                            metric1=metric1, metric2=metric2, metric3=metric3,
                            country1=country1, country2=country2, country3=country3, country4=country4)






# Score submission pages
@app.route("/scores", methods=["POST"])
def scores():
    # Find final answer user submitted
    if request.form.get("option1") != None:
        response = request.form.get("option1")
    elif request.form.get("option2") != None:
        response = request.form.get("option2")
    elif request.form.get("option3") != None:
        response = request.form.get("option3")
    else:
        response = request.form.get("option4")

    # Extract final round from SQL database (should always be 10)
    lastRoundDict = db.execute("SELECT max(round) FROM results;")
    lastRound = lastRoundDict[0]['max(round)']

    # Extract answer for final round from SQL database
    answerDict = db.execute("SELECT answer FROM results WHERE round = :quizRound", quizRound=lastRound)
    answer = answerDict[0]['answer']

    # Check whether contestant got answer correct or not and update results table
    if response == answer:
        db.execute("UPDATE results SET correct = 1 WHERE round = :quizRound", quizRound=lastRound)
    else:
        db.execute("UPDATE results SET correct = 0 WHERE round = :quizRound", quizRound=lastRound)

    # Calculate contestant's final score
    scoreDict = db.execute("SELECT sum(correct) FROM results;")
    score = scoreDict[0]['sum(correct)']

    # Pass that score as a variable to the scores page
    return render_template("scores.html", score=score)






# Leaderboard page
@app.route("/leaderboard", methods=["GET", "POST"])
def leaderboard():

    # Ensure contestant submitted a name otherwise score will not be stored
    if not request.form.get("name"):
        return apology("Please enter a name to submit", 403)
    else:
        name = request.form.get("name")

    # Check contestant's final score
    scoreDict = db.execute("SELECT sum(correct) FROM results;")
    score = scoreDict[0]['sum(correct)']

    # Load contestant's score into leaderboard table - first check if it already exists
    if not db.execute("SELECT * FROM leaderboard WHERE name = :name AND score = :score", name=name, score=score):
        db.execute("INSERT INTO leaderboard (name, score) VALUES (:name, :score)", name=name, score=score)

    # Create headings - this will be passed into webpage to render leaderboard
    headings = ["Name", "Score"]

    # Create a data list - will create a list of lists and pass this into webpage to render leaderboard
    data = []

    # Extract all scores and users from leaderboard with which to populate data within the table. ORDER BY score descending
    namesScores = db.execute("SELECT name, score from leaderboard ORDER BY score DESC")

    # Run through each dict from SQL extract: each dict is one row in SQL, from which create one list that goes into data list of lists
    for i in namesScores:

        # Initialise an empty list
        tdata = []

        # Assign dictionary values to variables
        name = i['name']
        score = str(i['score']) + "/10"

        # Append these variables into my list
        tdata.append(name)
        tdata.append(score)

        # Append these lists into master list of lists
        data.append(tdata)

    # Render template and pass in headings and data lists
    return render_template("leaderboard.html", headings=headings, data=data)