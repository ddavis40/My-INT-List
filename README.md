# My INT list
#### Video Demo:  <https://youtu.be/-6O8rmq4A80>
#### Description:
# My INT List
# The API key I used to develop and use this project is a temp key, and expires every 24 hours. It is only a development key, and to get a permanent key I will need to apply for one and be approved for it.


# The file called helpers.py contains the following helper functions:
- apology() - This is a function initially shown to me in week 9s finance problem set. It provides a way to provide fun dynamic error messages when a user ends up making a mistake somewhere or fails to provide some type of input.
- login_required() - This is another function we used in week 9s problem set. It’s purpose is to decorate certain routes of your web application with a function that checks to see if there is someone logged in, this is so that someone should not be able to access a certain area of your webpage without providing login credentials first.

# In app.py there are many functions going on, all associated with a web page of my application. They are:
- after_request() - after request is meant to run after every request to the application is made, the code in this function is designed to ensure that things are not cached client side and are insead updated each time they are requested.
- logout() - logout is a function with the purpose of forgetting the current users unique id and returning to the login page.
- login() - is designed to query the database containing our clients usernames and hashed passwords, and then to check if the entered credentials match any of them, and if they do log them into their homepage, and if they don't, to deny login altogether.
- index() - index queries our database for our users listed players, and then goes on to display an updated list of them on their homepage, along with an input area for inputting or updating any notes a user may have for a certain player.
- register() - is a function that can register a user. It first gets all information inputted through a form on the webpage, it then queries our database to make sure there is not already a user with the same requested user name, if all is well it will then insert into our database a new user with a new password and id, and then return the user to their new homepage.
- add() - this function displays a form to add a new player to the list, by inputting the players credentials into a form on the page, when this happens the code will query an Riot Games API(requires an updated key to properly work) where it will request the players puuid(unique id) and if the player is found and a response containing a puuid is received it will be inserted and stored in our database in the int_list table.
- history() - this is used to display a history of adds/drops from the list, it queries the history table and displays the information associated with the user on their history tab.
- remove() - this function is used to remove a user from the list. It is a web page that renders each player in the users list and provides the user with a clickable button that will remove the player from their list, and then update the page with the desired player now gone from the list.
- change() - is a function that allows an already logged in user to change their current password, it takes input from forms on the webpage, ensures the new password and confirmation match. Then it hashes the new password and inserts it into the database for that user.
- check() - this function renders a form when accessed by GET where a user can input a name, most likely the name of their account, or a name of a player they care about, and when requested by POST a query will be sent out to a Riot Games API(requires and updated key to properly work) where the requested players puuid is obtained, if there is no puuid obtained an error message will be displayed. Then a different Riot Games API(requires an updated key to properly work) is queried using the player puuid that will obtain the current games participants if the entered player is in a game, or return an error if they are not currently in game. This function will then check the current games participants if there are any against the database’s int_list table to see if any of the current games' puuids match any of the puuids stored in the int_list table. If there are one or more matches found, a web page will be displayed listing the names of the players that are found in both sets of data. If there are no matches found a more static webpage will be displayed in the event of there being no matches across the two sets of data.

# Outside of the main python files:
- There is test.py and test1.py where I played around with querying the riot games API’s.
- There is requirements.txt which is where I put every library that was used to provide functionality to the script.
- data.db is the sql database file containing a users table,  int_list table, and a history table.
- There is an .env file containing my API key.
- And a .gitignore file.
- And finally readme.md which you are reading right now!

# There are a few more directories in the project folder, flask_session, static, and templates.

# In flask_session there are files containing data from different flask sessions.

# In static are the image files and css files:
- Images are used as background images or embedded images on the web pages
- Css files layout1.css are used for layout1.html and layout2.css is used for layout2.html which are very similar, and could probably been named better for better understanding, but, layout1 is the layout for the login, register, and add pages, and layout2 is the layout for only the check page. Finally styles.css is for layout.html and it contains all of the css to provide a nice pretty dark style to the navbar and all elements rendered on screen.

# In templates there are a lot of html files each for a different function of the web application:
- add.html, displays a form to input player information to be added to the list.
- apology.html displays our dynamic error message.
- change.html displays a form to change an already logged in user's password.
- check_int.html is displayed when there is someone on the list in the same game as you.
- check_no.html is displayed when there isn't anyone on the list in the same game as you.
- check.html displays a form to input your name to check your list against the current games players.
- history.html displays a page where a user's dynamic add/drop history is displayed.
- index.html displays a user’s homepage and dynamic table of current listed players, along with an updatable notes section for each listed player.
- layout.html is a layout html page with a dark themed navbar from bootstrap, and links to outside css files, and some metadata for ensuring a scaling experience when accessed on different screen types.
- layout1.html is very similar to layout.html but uses a layout1.css as a css file.
- layout2.html is also very similar to layout.html but instead uses layout2.css for its css file.
- login.html displays a form for a user to login to their account.
- register.html displays a form for a user to create a new account.
- remove.html displays a form for a user to remove players from their list with the click of a button next to the players name.

# And that is the end of all of the files inside my final project directory, all listed and all explained as to what their purpose is in the schema of My INT List v0.1.

Thank you for reading my README.md and possibly using my application!

