# Movies API
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

## Overview
This API returns 50+ movies. I will keep adding more.

I used selenium to scrape movie data.

## Usage
Clone the repo
```
git clone https://github.com/raykipkorir/movies-api.git
```
Navigate into movies-api directory
```
cd movies-api
```
Create virtual environment
```
virtualenv venv
```
Activate virutal environment 
```
\venv\Scripts\activate
```
Install the dependencies
```
pip install -r requirements.txt
```
Run server
```
uvicorn app.main:app --reload
```
N/B -> Make sure you create environment variables shown in .env.example

## Contribution
Feel free to fork the project and contribute.

Any minor changes would be greatly appreciated.
