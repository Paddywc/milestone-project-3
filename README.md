# Riddle-Me-This

## Overview
![Screenshot](https://snag.gy/JChAGR.jpg)

### What it the website for? 
Playing a game where users attempt to solve riddles

### What does it do?
Up to four players take turns solving riddles. Answer correctly and gain a point. Answer incorrectly and lose a life.  Players must answer a riddle correctly before moving onto the next one. The riddles become more difficult as the player’s score increases. Players are eliminated when they run out of lives. Final scores are logged to a leaderboard. 

### How does it work? 
Players set their usernames using a POST method form. A list of dictionaries is then created and saved in a JSON file. Each dictionary represents one player. It stores all their information required throughout the game. This includes their username, score, current question and incorrect guesses. Functions written in Python3 and Flask get data from this file, edit the data, and then dump it back. Players submit their answer using a POST method form. The functions then adjust the JSON data accordingly. For example, if a player answers a question incorrectly, Python subtracts 1 from that player’s score, turns their “last question correct” value to false, and adds their guess to their ‘incorrect guesses’ value. Once eliminated, players scores are added to a high scores JSON file. Flask routing is used to render these high scores in a HTML template, as well as all other pages in the web app. 

## Features

### Existing Features
-	Text-based and picture-based riddles that users can answer
-	A text box for user’s answers which can determine from free-form text if their answer was correct
-	Up to 4 players can play together
-	Scores and lives for each player. Players are eliminated when their lives reach 0
-	Displays the correct answer to the riddle if the player is eliminated 
-	Several difficulty levels that adjust automatically based on the player’s score
-	Functionality to repeat the same question if the player guessed incorrectly on their last turn  
-	Displays the player’s previous incorrect guesses for their current question
-	Leaderboard

### Features Left to Implement
-	None

## Tech Used

### Some of the tech used includes:
-	**HTML**  and **CSS**
    *	To structure and style the web app content, Including creating the POST method form
-	**Python3**
    *	To design the logic of the game
    * For reading from, and writing to, the game’s text files
    * For unit testing the game’s functions. These tests are found in test_game.py
    *	Creating a requirements.txt and Procfile to deploy the app on Heroku 
    *	Sorting the leadboard data
-	[**Flask**]( http://flask.pocoo.org/)
    *	For binding functions to URLs using routing 
    *	To render HTML templates, including the use of a base template. These templates are in the templates directory 
    *	To  enable Python programming within HTML pages
    *	To trigger functions on GET or POST requests
    *	For getting data from, and dumping data to, JSON files
    *	Used for debugging 
-	**JSON**
    *	For storing and editing player data (players.json) and previously asked questions (used_questions.json) throughout the game
    *	Used to store high score data, found in /data/high_scores.json
- [**Bootstrap**](http://getbootstrap.com/)
    *	Used primarily for the website’s grid layout and for styling buttons, player cards, and the leaderboard table
- [**Heroku**](https://project-3-riddle-me-this.herokuapp.com/)
    *	To host the final version of the game 

## Testing 

### Approach to Testing
This project used Test Driven Development(TDD). Tests were (mostly) written before the functions. The functions were then designed to pass these tests. The tests were designed in such a way that in order to pass them, the functions had to serve their desired purpose within the program. 

### Manual Testing
Manual tests were carried out primarily for two purposes:
1.	**Testing the flow off the game**
The game loop (the render_game() function) is a combination of various functions. All these functions may work correctly, thus passing all the automated tests, but not work together as planned. Therefore, manual testing was required to ensure the game flowed as planned. An example of this was removing dead players from the JSON data before checking if all players have been eliminated.
2.	**Experimenting with the project**
There were times throughout development where some experimentation was required to understand what functions to design. In these instances, the first step was to experiment by designing a few functions. Then, once it was known what functions should be designed, these functions could be tested to ensure that they worked as planned.

### Automated Tests
Pseudocode was often used when designing the automated tests.  As python resembles written English, the final code largely resembles the pseudocode. Below are two examples of pseudocode used, along with the final, python version of these tests: 
1.	Test that ask_question writes the current player’s question to question.txt 
-	Wipe all previous game text
- Add a list of dictionaries 
    * All of which have a 'turn' key
    * One, and only one, of these keys have a value of True
    * All dictionaries also have a 'question' key. These each have a different question tuple as a value
- Dump these dictionaries to players.json
- Run ask_question
- Open and read the question.txt
- Store the response as a variable
- Assert that this variable is equal to the player's question
![Python code](https://i.snag.gy/EwZv6m.jpg)

2.	Test that post_to_leaderboard function adds its argument to high_scores.json
-	Get the current leaderboard data
    *	Save its length as a variable
-	Create an empty list variable
-	Dump it to the high_scores.json file
-	Get the leaderboard data from players.json
    *	Assert that its length is 0
-	Dump the original leaderboard data to high_scores.json
-	Get the data in high_scores.json
-	Save its length as a variable 
    *   Assert that it equals the length of the original data
![Python code](https://i.snag.gy/ByibWu.jpg)

## Contributing 
### Getting the project running locally
1.	Clone or download this GitHub repository using the ‘Clone or Download’ button found on [the main page](https://github.com/Paddywc/milestone-project-3) 
2.	Open the project directory using an integrated development environment (IDE)  software application, such as Eclipse or Visual Code Studio
3.	Ensure you have Python3 installed on your computer, and install it if you do not. How you should do this depends on which operating system you are using.  See the [Python Documentation](https://docs.python.org/3.4/using/index.html) for instructions 
4.	Next, you’ll need to install Flask. Detailed documentation can be found on the [Flask Website]( http://flask.pocoo.org/docs/1.0/installation/#installation). The simplest way to install Flask is to:
    *	Create a project folder 
    *	Create a python3 venv folder within this project folder
    *	Activate the environment using either _. venv/bin/activate_ or _venv\Scripts\activate_
    *	Within this activated environment, install Flask by using the following command : _pip install Flask_
5.	Run the code in run.py
6.	Well done! The project is now up and running on your local port. Click the link in your terminal to view the web app

## Credits
-	Almost all text riddles came from [IcebreakerIdeas.com]( https://icebreakerideas.com/riddles-for-kids/) . All others came from friends and family
-	All picture riddles are from [BRiddles.com](http://www.briddles.com/riddles/picture)

