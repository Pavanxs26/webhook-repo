# webhook-repo

# Developer Assessment Task

Flask application that receives GitHub webhooks (Push, Pull Request, Merge) and displays them in a live UI.

# Prerequisites

- **Python 3.7+**
- **MongoDB** (local installation or MongoDB Atlas account)
- **ngrok** (for exposing your local server to the internet)
- **Git** (for cloning the repository)

# How to setup

**1. Install stuff**

- First, make sure you have Python and MongoDB installed on your computer. Then run this in your terminal:
- pip install flask pymongo pytz

**2. Run MongoDB**

- Make sure your MongoDB is running on localhost:27017. The app will automatically create a database called github_webhooks.

**3. Start the app**

- In your terminal, run:
- python run.py
- Now you can open http://localhost:5000 in your browser to see the dashboard.

**4. Connect to GitHub**

- Start ngrok to get a public link: ngrok http 5000.
- Copy the https link ngrok gives you.
- Go to your GitHub Repo -> Settings -> Webhooks -> Add Webhook.
- Payload URL: YOUR_NGROK_LINK/webhook/receiver
- Content type: application/json
- Select "Push" and "Pull Request" events.

# Project Structure

- **app/** - Contains all the Flask code and HTML.
- **run.py** - The main file to start the server.
- **requirements.txt** - List of libraries needed.
- **extensions.py** - MongoDB connection setup.

# How it works 
- The app uses a 15-second timer to refresh the page and check for new events from MongoDB.
- It stores the Author, Action, Branches, and Timestamp for every event.