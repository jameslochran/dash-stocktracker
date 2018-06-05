# dash-stocktracker

The stock tracker app is a basic Dash app that enables the user to monitor the status of thier investments in the FANG stocks. If you're not familar with the term FANG, its a acronym for Facebook, Amazon, Netflix and Google(Alphabet). The app tracks the closing prices for these 4 stocks over the designated time frame and displays the results in a line graph. The user can also set up an investment goal and see how their investments are tracking torwards their goal. The final component is a editable table that allows that user to update the share counts for each of the companies. Updating the share count will resulting in the bar chart adjjusting accordingly. 



<b>Getting started</b>

Create a virtual environment, this is not required but good practice. Here's a good article on the mertics and techniques for creating a virtual environment. Here's a good article on why you need a virtual environment. https://medium.freecodecamp.org/why-you-need-python-environments-and-how-to-manage-them-with-conda-85f155f4353c 

Now that you have your environement set up, you can either download or clone this project. 

To install all of the libraries that are required for this project run:

<b>pip install requirements.txt</b>

Then you can start the app by running the stocktracker1.py file from the command line.


<b>Future considerations</b>
1. Add a database to track changes to your investments overtime
2. Fix the progress report graph to enable it to update when the table is updated, currently you need to push the button to trigger the update. 
3. Store the goal in the database
4. Expose ability to add more stocks to the watch list and table. The code is currently commented out for the first part, but you'll need to add a function to populate the dropdown list with additional stocks. There's also code to add a new line to the table which would enable to user to add stocks to the table. This code is commented out. 


Have fun!







