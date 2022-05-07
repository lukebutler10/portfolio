# Building a blockchain and cryptocurrency


In this project I followed a course to create my own blockchain and cryptocurrency using Python, JavaScript and React. 

Some of the things this involved:
What your app


Some of the things this involved:
Using a sha -256
Testing using the pytest module


Here's a [link](https://www.udemy.com/course/python-js-react-blockchain/) to the course webpage


**Activate the virtual environments**

```

source blockchain-env/bin/activate
```

**Install all packages**
```

pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment

```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment

```
python -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment

```
set PEER=True 
python -m backend.app  #I had to run these in 2 separate lines to get it to work whereas Dave put them in same, connected with "&&"
```

**Run the frontend**

In the frontend directory:
```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment

```
set  SEED_DATA=True
python -m backend.app
```
