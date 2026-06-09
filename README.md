# Resource Recommendation System

## Overview

Resource Recommendation System is a web-based application that helps users discover learning resources for different career paths. The system provides curated educational content, career guidance, and learning recommendations to support students in skill development.

## Features

* Career-based resource recommendations
* Learning roadmap suggestions
* YouTube resource integration
* Interactive and responsive user interface
* Admin dashboard for content management
* Fast resource retrieval using caching

## Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### APIs

* YouTube Data API

## Project Structure

Resource-Recommendation-System/

├── backend/

│   ├── app.py

│   ├── requirements.txt

│   └── youtube_cache.json

├── frontend/

│   ├── index.html

│   ├── quiz.html

│   ├── result.html

│   ├── style.css

│   └── script.js

└── README.md

## Installation

1. Clone the repository

git clone <repository-url>

2. Move into project directory

cd Resource-Recommendation-System

3. Install dependencies

pip install -r backend/requirements.txt

4. Create a .env file and add your YouTube API key

YOUTUBE_API_KEY=your_api_key

5. Run the Flask application

python backend/app.py

## Usage

1. Open the application in your browser.
2. Select your preferred career path.
3. Explore recommended learning resources.
4. Follow the suggested roadmap to improve skills.

## Future Enhancements

* AI-powered personalized recommendations
* User authentication
* Progress tracking
* Learning analytics dashboard

## Author

Kritika Raturi
