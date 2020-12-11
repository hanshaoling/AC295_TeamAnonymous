# AC295 TEAM Annonymous final project

## Video Link: 

## Docker setup instruction:

First we build the frontend and backend images:

Go to frontend folder and then :

```docker build -t project:frontend -f Docker_frontend . ```

Then go to backend folder :

```docker build -t web:backend -f Docker_maindb . ```

Now create a docker network:

``` docker network create appNetwork ```

Run these two images:

``` docker run --name mywebdb -d --network appNetwork web:backend ```

``` docker run --name fe -d -p 5000:8081 --network appNetwork project:frontend ```

You can run ```docker network inspect appNetwork``` to check if these two images are running

Now you can go to **http://0.0.0.0:5000/** and submit your essay for grading!

