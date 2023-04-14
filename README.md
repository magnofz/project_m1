## Name
"Finding the Closest BiciMAD Station to Every Monument in Madrid"


## Status
Alpha version


## One-liner
This project uses REST APIs from the City of Madrid and BiciMAD to find the closest BiciMAD station to every monument in Madrid, providing useful information for tourists who want to explore the city by bike.


## Technology stack
Python, Requests library, JSON, Pandas, Geopandas, Shapely.geometry, Fuzzywuzzy.


## Core technical concepts and inspiration
This project was inspired by the idea of combining public data sources to provide useful information to tourists. The technical concepts demonstrated include REST API requests, data manipulation, geolocation calculations and visualization of results.


## Configuration
The project requires Python 3.x and several libraries, which can be installed using the requirements.txt file included in the repository.


## Usage
The main script is located in the root folder and is named "main.py". The script requires an API login for the BiciMAD API, which should be stored in a file named ".env" in the folder named '__dotevn__'. The file should contain two variables with your information from the BiciMAD API: "MAIL=<YOUR_MAIL>" and "PASSWORD=<YOUR_PASSWORD>". Once the API key is set up, the script main.py can be run. The script will output a CSV file with the closest BiciMAD station to every monument in Madrid.

```
Folder structure
├── .git
├── __dotenv__
├── data
├── modules
│ └── modules.py
├── notebooks
│ └── dev_notebook_.ipynb
├── requirements.txt
├── .gitignore
├── main.py
└──README.md
```


## ToDo
Improve the error handling and user interface of the script.


## Further info
This project was created as part of the Ironhack Data Analytics Bootcamp in Madrid. The City of Madrid API provides access to a wealth of data about the city, including information about its monuments, parks, and public transportation systems. BiciMAD is the public bike-sharing system of Madrid, which allows users to rent bikes from stations located throughout the city.


## Contact info
If you have any questions or feedback, please contact me at magnofz@gmail.com.