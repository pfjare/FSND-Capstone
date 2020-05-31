# Setup

## Running the server

From within the base directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

# Casting Agency API Documentation

This API follows the given Casting Agency Specifications with a few added endpoints and functionality.

-   Base URL: https://fsnd-pfjare.herokuapp.com/
-   Local Base URL: The local app is hosted at the default, http://127.0.0.1:5000/.

## Authentication:

All endpoints require authorization. Users are assigned one of three roles. Each role has a different set of permissions.

-   **Casting Assistant** - get:movies, get:actor
-   **Casting Directior** - get:movies, get:actor, post:actor, patch:actor, delete:actor, patch:movie
-   **Executive Producer** - get:movies, get:actor, post:actor, patch:actor, delete:actor, patch:movie, post:movie, delete:movie

Each request must be sent with a bearer token corresponding to a user.
If you are using Curl, include `-H "Authorization: Bearer an_example_4eC39HqLyjWDarjtT1zdp7dc"`.

I have created 3 users and included the corresponding bearer tokens in config.py .

Run './set.sh' in terminal to set Auth0 env variables.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:

-   400: Bad Request
-   404: Resource Not Found
-   422: Unprocessable Entity

Errors with authentications (401) provide additional info about the error in the form

```
{
    'code': 'authorization_header_missing',
    'description': 'Authorization header is expected.'
}
```

## Postman

I have included a Postman collection FSND-Capstone.postman_collection.json with each endpoint to make it easy for the reviewer to test. Just change the bearer token to test a different role.

## The movie object

Contains the unique id of the movie, the movie's title, the movie's genre, and the movies release date.

### Example

```
    {
        "genre": "Comedy",
        "id": 5,
        "release_date": "2004-06-28",
        "title": "Anchorman: The Legend of Ron Burgundy"
    }
```

## The actor object

Contains the unique id of the actor, the actor's name, the actor's gender, and the actors age.

### Example

```
        {
            "age": 46,
            "gender": "male",
            "id": 6,
            "name": "Christian Bale"
        }
```

## Endpoints

-   GET /movies
-   GET /movies/:id
-   POST /movies
-   PATCH /movies/:id
-   DELETE /movies/:id
-   POST /movies/:id/actors/:id
-   DELETE /movie/:id/actors/:id
-   GET /actors
-   GET /actors/:id
-   POST /actors
-   PATCH /actors/:id
-   DELETE /actors/:id

### GET /movies

Fetches all movies in the dataset.

**Roles with access:**

Casting Assistant, Casting Director, Executive Producer

**Query String Parameters:**

page \[int\] (optional) - Movies are paginated in groups of 10. Include a page argument to retreive the desired page. If unspecified the page defaults to 1.

**Returns:** A dictionary with a movies property that contains an array of movie objects. If there are no movies in the database, the resulting array will be empty. The dictionary also contains a success value and the total number of movies.

`curl {host}/movies?page=1 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "movies": [
        {
            "genre": "Comedy",
            "id": 1,
            "release_date": "2002-10-31",
            "title": "Zombieland"
        },
        {
            "genre": "Comedy",
            "id": 5,
            "release_date": "2004-06-28",
            "title": "Anchorman: The Legend of Ron Burgundy"
        },
        {
            "genre": "Comedy",
            "id": 6,
            "release_date": "2007-03-30",
            "title": "Blades of Glory"
        },
        {
            "genre": "Comedy",
            "id": 7,
            "release_date": "2006-08-04",
            "title": "Talladega Nights: The Ballad of Ricky Bobby"
        },
        {
            "genre": "Action/Adventure",
            "id": 8,
            "release_date": "2008-07-18",
            "title": "The Dark Knight"
        }
    ],
    "success": true,
    "total_movies": 5
}
```

### GET /movies/:id

Fetches a single movie from the dataset.

**Roles with access:**

Casting Assistant, Casting Director, Executive Producer

**Query String Parameters:**

None

**Returns:** A dictionary with a movie property that contains a movie object. Appended to the movie object is an actors property with an array of ids of actors assigned to the movie. If there is not a movie with the given id in the database, a 404 error will be returned. The dictionary also contains a success value.

`curl {host}/movies/1 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "movie": {
        "actors": [
            2
        ],
        "genre": "Comedy",
        "id": 1,
        "release_date": "2002-10-31",
        "title": "Zombieland"
    },
    "success": true
}
```

### POST /api/movie

Creates a new movie in the database.

**Roles with access:**

Executive Producer

**Query String Parameters:**
None

**Body Parameters:**

title \[string\] (required) - The movie title.

genre \[string\] (required) - The genre of the movie.

release_date \[string\] (required) - The movie release date. Format y-m-d (Ex: 1997-12-05).

**Returns:** A success value and the id of the created movie.

`curl {host}/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyjh.example.yJhbGczI" -d '{"title": "The Dark Knight", "genre": "Action/Adventure", "release_date": "2008-7-18" }'`

```
{
    "created": 8,
    "success": true
}
```

### PATCH /api/movie/:id

Edits a movie in the database.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**

title \[string\] (optional) - The movie title.

genre \[string\] (optional) - The genre of the movie.

release_date \[string\] (optional) - The movie release date. Format y-m-d (Ex: 1997-12-05).

**Returns:** A success value and the id of the edited movie.

`curl {host}/movies/8 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer eyjh.example.yJhbGczI" -d '{"release_date": "2008-8-18" }'`

```
{
    "edited": 8,
    "success": true
}
```

### DELETE /api/movies/:id

Deletes a movie in the database with the specified id.

**Roles with access:**

Executive Producer

**Query String Parameters:**
None

**Body Parameters:**
None

**Returns:** A success value and the id of the deleted movie.

`curl -X DELETE {host}/movies/24 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "deleted": 24,
    "success": true
}
```

### POST /api/movies/:id/actors/:id

Assigns an actor to a movie role with the specified ids.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**
None

**Returns:** A success value.

`curl -X POST {host}/movies/6/actors/4 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "success": true
}
```

### DELETE /api/movies/:id/actors/:id

Removes an actor from a movie role with the specified ids.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**
None

**Returns:** A success value.

`curl -X DELETE {host}/movies/6/actors/4 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "success": true
}
```

### GET /actors

Fetches all actors in the dataset.

**Roles with access:**

Casting Assistant, Casting Director, Executive Producer

**Query String Parameters:**

page \[int\] (optional) - Actorss are paginated in groups of 10. Include a page argument to retreive the desired page. If unspecified the page defaults to 1.

**Returns:** A dictionary with a actors property that contains an array of actor objects. If there are no actors in the database, the resulting array will be empty. The dictionary also contains a success value and the total number of actors.

`curl {host}/actors?page=1 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "actors": [
        {
            "age": 52,
            "gender": "male",
            "id": 4,
            "name": "Will Ferrell"
        },
        {
            "age": 55,
            "gender": "male",
            "id": 5,
            "name": "John C. Reilly"
        },
        {
            "age": 46,
            "gender": "male",
            "id": 6,
            "name": "Christian Bale"
        }
    ],
    "success": true,
    "total_actors": 3
}
```

### GET /actors/:id

Fetches a single actor from the dataset.

**Roles with access:**

Casting Assistant, Casting Director, Executive Producer

**Query String Parameters:**

None

**Returns:** A dictionary with a actor property that contains a actor object. Appended to the actor object is a movies property with an array of ids of movies assigned to the actor. If there is not a actor with the given id in the database, a 404 error will be returned. The dictionary also contains a success value.

`curl {host}/actors/1 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "actor": {
        "age": 52,
        "gender": "male",
        "id": 4,
        "movies": [
            6
        ],
        "name": "Will Ferrell"
    },
    "success": true
}
```

### POST /api/actor

Creates a new actor in the database.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**

first_name \[string\] (required) - The actor's first name.

last_name \[string\] (required) - The actor's last name.

birth_date \[string\] (required) - The actor's birth date. Format y-m-d (Ex: 1997-12-05).

gender \[string\] (required) - The actor's gender.

**Returns:** A success value and the id of the created actor.

`curl {host}/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyjh.example.yJhbGczI" -d '{"first_name": "Will","last_name":"Ferrell", "gender":"male", "birth_date":"1967-7-16"}'`

```
{
    "created": 4,
    "success": true
}
```

### PATCH /api/actor/:id

Edits a actor in the database.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**

first_name \[string\] (optional) - The actor's first name.

genre \[string\] (optional) - The actor's last name.

birth_date \[string\] (optional) - The actor's birth date. Format y-m-d (Ex: 1997-12-05).

gender \[string\] (optional) - The actor's gender.

**Returns:** A success value and the id of the edited actor.

`curl {host}/actors/4 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer eyjh.example.yJhbGczI" -d '{"birth_date":"1967-7-13"}'`

```
{
    "edited": 4,
    "success": true
}
```

### DELETE /api/actors/:id

Deletes a actor in the database with the specified id.

**Roles with access:**

Casting Director, Executive Producer

**Query String Parameters:**
None

**Body Parameters:**
None

**Returns:** A success value and the id of the deleted actor.

`curl -X DELETE {host}/actors/21 -H "Authorization: Bearer eyjh.example.yJhbGczI"`

```
{
    "deleted": 21,
    "success": true
}
```
