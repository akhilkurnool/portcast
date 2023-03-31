A mini project to get random paragraph from [metaphorpsum](http://metaphorpsum.com) and search and get definitions of 10 most frequent words in all the paragraphs that are queried till that point.

The paragraphs are persisted in `SQLite` database. Details of APIs are mentioned below.

This project is made with `fastapi`, to learn more about it check out the offical [website](https://fastapi.tiangolo.com/). The application is run within a [docker](https://www.docker.com/) container.

## Getting started

Make sure you have docker installed, please follow the official [guide](https://docs.docker.com/get-docker/) and install for appropriate OS

1. Clone the repository

```bash
git clone <repo-link>
```

2. Change directory to the root of the application

```bash
cd portcase
```

3. Run `docker-compose` command to start the container

```bash
docker-compose up -d --build
```

You should be able to open `localhost:8000` in any browser and get a random paragraph. Current parameters: number of paragraphs = 1, no of sentences = 50

## Run tests

You can run the following command and see the test results

```bash
docker-compose run tests
```

### APIs

- **GET** `/` return a random paragraph
- **GET** `/search` return all the paragraphs which match the search parameters
*Query parameters*:
  - `q` search query: comma separated list of words to be searched for. e.g `?q=word1,word2,word3`
  - `in` search operator: values can be either `or` or `and`. If `and` is used then only those paragraphs are returned where **all** the words in `q` are matched. If `or` is used then only those paragraphs are returned where **any** one of the words in `q` are present.
- **GET* *`/dictionary` return meanings of 10 most frequent words in all the paragraphs combined
