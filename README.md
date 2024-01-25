# Smart Schedule Server

Smart Schedule Server is a practical tool designed to assist in daily planning and finding interesting events. It simplifies the process of organizing a daily to-do list and suggests activities and events tailored to the user's preferences. Here are its key functionalities:

 - Automated Daily Planner: Automatically generates a daily schedule based on user preferences.
 -  Event Recommendation: Suggests events and activities that align with the user's interests.
 - Simple User Interface: Features a card-based interface on the client side, making it easy to view and manage tasks.
 - AI Integration: Utilizes AI models like ChatGPT and Bard to refine event recommendations and generate new events for different user groups.

Overall, Smart Schedule Server aims to streamline daily planning and bring relevant events to the user's attention, all through a user-friendly interface.

## Technology Stack
Our project integrates various technologies, each serving a specific purpose:

 - Python & Django REST Framework: Core tools for backend development.
 - Selenium: Used for automating web browsers, essential in testing.
 - Redis: Acts as a fast, in-memory data store, used primarily for caching.
 - Celery: A task queue for managing background jobs, utilizing Redis as a broker.
 - PostgreSQL: Our primary database, selected for its robustness.
 - JWT (JSON Web Tokens): Handles secure user authentication.
 - Flower: A tool for monitoring Celery tasks.
 - JSON Logger: Provides structured logging for better analysis.
 - Sentry: Offers real-time error tracking and fixing.

## Installation and Setup with Docker
To ensure a smooth and consistent setup across different environments, our project can be easily set up using Docker and Docker Compose. Here are the steps to get it running:
### Prerequisites
Make sure Docker and Docker Compose are installed on your machine. If they're not, you can download them from the Docker website.
### Running the Project
**Clone the Repository**: First, clone the project repository to your local machine:
```
git clone https://github.com/Ivan-Klishevskiy/smartschedule_server.git
```
### Navigate to the Project Directory: 
Change into the directory where your project is located:
```
cd smartschedule_server
```
### Build the Docker Images:
Before running the containers for the first time or after any changes to the Docker configurations, build the Docker images:
```
docker-compose build
```
### Start the Services: 
Now, start all the services with Docker Compose:
```
docker-compose up
```
This will start the services defined in your docker-compose.yml.
### Access the Application: 
Once the containers are up, the application should be accessible through your web browser or API client at the defined ports.

This setup process with Docker and Docker Compose ensures that the application environment is consistent and ready to use.

## Related Projects
For a complete experience of Smart Schedule Server, check out our frontend project as well:

   Smart Schedule Client: https://github.com/MarcusKordunski/smartschedule_client.git. This repository contains the frontend code of our application, built to interact seamlessly with the Smart Schedule Server. It provides a user-friendly interface for managing schedules and accessing AI-powered recommendations.

