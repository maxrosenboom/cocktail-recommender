# cocktail-recommender
🥂 Recipe recommendation website using Flask, REST APIs, and scikit-learn.

## To run it:
The project is actually very simple to run due to the use of Flask. All you need to do is run `python server.py`.

## Technologies used:
- Web Scraper: Beautiful Soup
- Database: Redis
- Hosting: Google Cloud Platform Kubernetes Engine
- Flask Web Server / restAPI
- Jinja
- scikit-learn & FastText  

## How does it work?
I began with BeautifulSoup to scrape the DrinksMixer website. This allowed to easily populate the database with the recipes and information of 12,334 recipes. I used a Flask server with rest API's to run the overall website and run GET and POST requests to retrieve information from the scikit-learn model (using FastText to compare strings). This allowed me to then find the most similar scores from the database, and return it to the user. I used Jinja to format the webpage, which allowed me to keep everything on one page and help performance.

## Ideas list for future features
- Rewrite entire front end site with React to make it look nice 
- Add hyperlinks to videos showing cocktail walkthrough
- Rating system for cocktails (along with a way to filter by reviews)
- Cocktail history and facts (just for fun)
- Nutritional info
- User accounts and profiles to provide search history