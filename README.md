# Welcome to the Language Learning Assistant Project!

## Introduction
Thank you for your interest in our project! We're developing a Language Learning Assistant that will help users to easily input, store, and review vocabulary words along with their translations. Our platform will include features like quizzes to reinforce learning and visualizations to track progress. This project is part of the evaluation for the Advanced Python Course at the University of Berne.

## Team Members
- Aissata Kane  
- Ilyas Woo
- Newton Ollengo
- Ondrej Baco

We are Computer Science and Biomedical Engineering Students at the University of Berne, and this project is a critical component of our Data Science course.

## Project Repository
The GitHub repository for this project can be found here: [GitHub Link](https://github.com/PythonDataScience24/E-Lang.git)

## How to Contribute & Get Involved
Interested in contributing? Here's how you can get involved:
- [Project Protocol](https://github.com/PythonDataScience24/E-Lang.git) - Follow our protocol to understand our workflow and standards.
- [Project Roadmap](https://github.com/PythonDataScience24/Language-Learning-Assistant/blob/main/Roadmap.md) - Check out our roadmap to see what we're working on and what's coming next.

Your contributions and feedback are invaluable to the success of this project. We look forward to working together to make language learning a more engaging and streamlined experience.

## Feedback and Suggestions
Please feel free to raise an issue on our GitHub repository for any suggestions or feedback. If you'd like to propose a feature or report a bug, we'd love to hear from you!

# Getting Started with Docker

## Prerequisites
Ensure you have Docker and Docker Compose installed on your system. You can verify your Docker installation by running:

```bash
docker --version
docker-compose --version
```
# Cloning the Repository

First, clone the repository to your local machine:

```bash
 git clone https://github.com/PythonDataScience24/E-Lang.git
cd Language-Learning-Assistant
```
## Setting Up and Running the Application
### Step 1: Build and Run the Containers

Navigate to the root directory of the project where the docker-compose.yml file is located and run the following command:

```
docker-compose up --build
```
This command will build the Docker images and start the containers for both the frontend and backend services.
### Step 2: Verify Backend and Frontend Services

Once the containers are up and running, you can verify that both the backend and frontend services are running correctly.

#### Backend Service

Open your web browser and go to:

```bash
http://127.0.0.1:3000
```

This should display the frontend application.
## Using the Application

One can Register and start using the application

Additional Information
Stopping the Containers

To stop the running containers, press "CTRL+C" in the terminal where docker-compose up is running or use the following command in a new terminal:

```bash
docker-compose down
```
## Rebuilding the Containers

If you make changes to the code and need to rebuild the containers, you can use:

```bash
docker-compose up --build
```
This will rebuild the images and start the containers again.
## Troubleshooting

If you encounter any issues, please refer to the logs for both backend and frontend containers to diagnose the problem. You can view the logs using:
``` bash
docker-compose logs backend
docker-compose logs frontend
```

We are excited to embark on this journey to make language learning more accessible, and we invite you to join us in this endeavor! """



