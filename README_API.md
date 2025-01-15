Getting Started
	Install the dependencies for the project:
        Run the commands: pip3 install -r requirements.txt from the home directory.

    To start the backend server:
        Run the command: python app.py

    Base URL: At present this app can be run locally or via the cloud. 
    local url: http://localhost:5000/
    cloud url: https://fsnd-02012025-bd5be96ef148.herokuapp.com 
    
    Authentication: Token is required 

Error Handling

Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return four error types when requests fail:

    400: Bad Request
    404: Resource Not Found
    422: Not Processable
    405: Method Not Allowed

Authentication Error
Errors are returned as JSON objects in the following format:
{
    'code': '401',
    'message':{
        authorization_header_missing
        description	"Authorization header is expected."
    }
    "success": False, 
}

Authentication will return four error types when requests fail:
    
    400: invalid_header
    400: invalid claims
    401: token expired
    401: authorization header missing
    401: invalid header
    401: invalid claims
    403: unauthorized

Endpoints
GET /actors
    General:
        Returns a list of all actors, if no actors are found it returns an 404 error       
    Sample: curl -L "http://localhost:5000/actors"
	
	"Actors": [
        {
            "age": 45,
            "full_name": "Robert Downey Jr.",
            "gender": "Male",
            "id": 1
        }
    ],
    "success": true
	
	
GET	/movies
	General:
        Returns a list of movies, if no movies are found returns an 404 error
		Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.	
    Sample: curl --location "http://127.0.0.1:5000/movies" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg"
	
	{
    "Movies": [
        {
            "duration": "2,2 hours",
            "id": 1,
            "imdb_rating": 8,
            "release_date": "05-04-2012",
            "title": "Avengers"
        }
    ],
    "success": true
}
	
DELETE /movies/<int:movie_id>
	General:
	 Deletes a movie based on its id , then returns the deleted movie id and its movie details , if the movie to be deleted is not found in the database it returns an 404 error
	 Sample: curl --location --request DELETE "localhost:5000/movies/1" --header "Content-Type: application/json" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg"
		
    {
    "Movie": {
        "duration": "2,2 hours",
        "id": 1,
        "imdb_rating": 8,
        "release_date": "05-04-2012",
        "title": "Avengers"
    },
    "deleted": 1,
    "success": true
}

DELETE /actors/<int:actor_id>
	General:
	 Deletes an actor based on its id , then returns the deleted actor id and actor details. 
	 Sample: curl --location --request DELETE "localhost:5000/actor/2" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg"
		
    {
    "Actor": {
        "age": 45,
        "full_name": "Robert Downey Jr.",
        "gender": "Male",
        "id": 2
    },
    "deleted": 2,
    "success": true
}

POST /actors
	General:
	 Adds an actor to the database, returns the actor that has been just added to the database
	 Sample: curl --location "localhost:5000/actors" --header "Content-Type: application/json" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg" --data "{\"movie_ids\":[1], \"full_name\":\"Robert Downey Jr.\",\"age\":45,\"gender\":\"Male\"}"
	 
	{
    "Actor": [
        {
            "age": 45,
            "full_name": "Robert Downey Jr.",
            "gender": "Male",
            "id": 1
        }
    ],
    "New_Actor": 1,
    "success": true
}

POST /movies
	General:
	 Adds Movies to the database, returns the Movie that has been just been added 
	 Sample: curl --location "localhost:5000/movies" --header "Content-Type: application/json" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg" --data "

    {\"actor_ids\":[1], \"title\":\"Avengers\",\"release_date\":\"05-04-2012\",\"duration\":\"2,2 hours\",\"imdb_rating\":8}"
	
	{
    "Movie": [
        {
            "duration": "2,2 hours",
            "id": 1,
            "imdb_rating": 8,
            "release_date": "05-04-2012",
            "title": "Avengers"
        }
    ],
    "New Movie": 1,
    "success": true
    }

    PATCH /actors
	General:
	 Updates an actor on the database, returns the actors details that has been just updated to the database
	 Sample: curl --location "localhost:5000/actors" --header "Content-Type: application/json" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg" --data "{\"movie_ids\":[1], \"full_name\":\"Robert Downey Jr.\",\"age\":45,\"gender\":\"Male\"}"
	 
	{
    "Actor": [
        {
            "age": 40,
            "full_name": "Robert Downey Jr.",
            "gender": "Male",
            "id": 1
        }
    ],
    "success": true
}

PATCH /movies
	General:
	 Updates a Movie on the database, returns the Movie's details that has been updated on the database 
	 Sample: curl --location --request PATCH "http://127.0.0.1:5000/movies/2" --header "Content-Type: application/json" --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzY5NTAxNjQsImV4cCI6MTczNjk1NzM2NCwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.jyNLWaEOOtmsMjAy08KLybIG_8HaQoa1KFGIwJn63K2_eYMsARxfF-oGuvXsoDFbO9BQY5-rOOAu7u5aY5_KuAC0gB6-75KXIQgOT_1iPom1zp-O9pOOOUBAVIEBHVi1cSx2Whdh9wfCzoXsNx9YQk4yVeK042aWrmWwz56Lf78vh4dD8ISeHSvby9yjV4PdWbGb5MNiXQV_yIF_VpMtqwJQtk_o7M0Bkyiy8Y6uZ1QP97X5KsYWHR3rR_v6dYe2w5bKXnM_5y_kWkYBlWEK6jxyGb8OoCU3GNvKm9gJ1Ze5BDfukYsbpyOzCbS3rcU9NJE5xKtmvGNOP9m0qe7ROg" --data "{ \"imdb_rating\":10}"
	
	{
    "Movie": [
        {
            "duration": "2,2 hours",
            "id": 2,
            "imdb_rating": 10,
            "release_date": "05-04-2012",
            "title": "Avengers"
        }
    ],
    "success": true
}




