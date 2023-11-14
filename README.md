# TEMG-4950-JPM-Dashboard
Usage: 
1. git pull everything from michael branch
2. download everything from the TEAMS data file
3. configure the project directory to match with the one in my screenshot
4. cd into directory and cmd python to run the __main__analyzer.py
5. input year-quarter and mode to run query
6. find output file in output/query directory

*note: mac user has to change all \ to /


![image](https://github.com/Shao-Fu-Wang/TEMG-4950-JPM-Dashboard/assets/45915603/87f68b7a-8e2b-4577-8484-0afc92587fae)

* Updates from Jayson:
    *  Currently to run the __main__scraper.py, build a new virtual environment (look online for tutorials) in order not to interfere with what you are doing at this momement, after activating the virtual environment call pip install -r requirements.txt
    *   However if you have already built the virtual environment and install the required packages, just make sure everytime when you are using the codebase to use it inside the virtual environment
    * include the .gitignore in repo so any temp / data folders wont be included in the project repo
