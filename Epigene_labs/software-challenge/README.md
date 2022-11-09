# Software Challenge

Welcome to Epigene Labs' Engineering Challenge. The goal of this challenge is to have some material for a following discussion with our engineers. Thus, we will pay special attention to a code that:

- can evolve easily; 
- is clean and robust;
- on which we can easily onboard new developers;
- is tested;

## How to proceed ?

1. Clone the repo (don't fork it) and create your own repo with the code;
2. Select the track you prefer (🐍 is more backend oriented, 🌈 is more frontend oriented), or feel more confortable with;
3. Resolve issues one by one of the selected track only (try to have the clearest commit history as possible)
4. Once you are done, send an email to benjamin@epigenelabs.com, we will organize a meeting afterward.

⚠️ We don't expect you to spend more than 1 to 4 hours in that challenge, and don't expect you to finish the challenge as well.

The interview will be the opportunity for you to expose your solution to the challenge you picked, but also an opportunity to learn more about Epigene Labs, and to meet more engineers. For us, the most important aspect will be to evaluate how much we could work together as a team. 

Also, do not hesitate to suggest some improvements for this test, we remain a very young start up and will love to hear your feedback. 

## Repository description

There is a `backend` folder where you will find a FastAPI python app. The App allows a user to manage what we call a Geneset, which is basically a list of known Genes that, put together, have a particular meaning or a particular impact on a specific protein, disease.

The API allows the user to create a Geneset, create some Genes, and add genes to a particular Genesets.

## Install and run the API

The following should be run under `/backend` folder.

### 1 - Install python

Install `python 3.8` with [pyenv](https://github.com/pyenv/pyenv)

```
brew install pyenv
pyenv install 3.8.0
pyenv local 3.8.0
```

Copy/paste at the following command at the end of your `.zshrc` or `.bash_rc`

```bash
eval "$(pyenv init -)"
```
### 2 - Install poetry

We need to install [poetry](https://python-poetry.org/docs/#installation) to manage python dependencies.

You can make sure poetry is correctly installed by running 

````
poetry --version
````

Then, install dependencies `poetry install`.


### 3 - Launch


````
poetry run uvicorn main:app --reload
````

You should now have an API running locally on port `8000`. The documentation of that API should be available at `localhost:8000/docs`

## 🐍 Track Backend

In that track, we will explore the API and try to improve it.

### Level 0

Make sure you can query the API. We use Postman at Epigene Labs, but feel free to use the tool you want.

Create a couple of Genesets to get more familiar with it. 

### Level 1

Now as a user, let's say you want to retrieve a gene based on its name, and know in which genesets it is present. 

Update the API so that we can deliver that new feature.

### Level 2

Sometimes, users don't know the specific name of a gene. They might not be able to retrieve correctly the gene they are looking for thanks to the previous API's update in Level 1. 

Update the API with a way to allow a user to search for genes.


### Level 3

We like to be able to search Geneset by title.Let's say you have a Geneset with title `Great Genes`, you could search and retrieve it with: 

````
127.0.0.1:8000/genesets/search/Great
````
Make sure it works as expected.

Now, we have thousands of users. 

Run `poetry run python populate.py` to populate the database and simulate the number of users. 

Let's check again the endpoint that allow a user to retrieves the full list of genesets. The output doesn't look good, and it's getting slower right ? 

Suggest a way to improve it.

### Level 4 - Bonus

Let's be real, this API isn't best in class. How do you think we could improve it ?

The idea here is not to implement any solution. Just think of some improvements we could discuss during the interview.


## 🌈 Track Frontend 

In that track, we will create an application that consumes the existing API.

### Level 0

Make sure you can query the API. We use Postman at Epigene Labs, but feel free to use the tool you want.

Create a couple of Genesets to get more familiar with it. 

### Level 1

Set up a React App from scratch. That retrieves and displays the list of genesets available. The user should be able to see the list of genesets with the geneset's title and the list of genes inside it.

### Level 2

Add an interface where a user can create a geneset, with a list of genes.

### Level 3

Unfortunately, the API doesn't prevent a user from creating a geneset with a uniq set of genes (ie we could have two identic genes in a geneset). 

Suggest a way for a user to display duplicate within a geneset.

### Level 4 - Bonus

We are missing one last step for a usable App which is the update of a geneset. Use the API, and suggest an interface to update a geneset with two actions (1) Update the title (2) Remove a gene from the geneset. 
