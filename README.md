
# Scrapper Fast Api fow wilderries

This is a scrapper for wildberries, which is able to scrape and save product cards, as well as automatically update the data in these cards.




## Tech Stack

Fast Api, Sqlalchemy, PostgreSQL, Celery, RabbitMQ.


## Environment Variables

You can find all environment variables in .env.example file.


## Run Locally

Clone the project

```bash
  git clone https://github.com/Sumchatyj/scrapper_Fast_API.git
```

Go to the project directory

```bash
  cd scrapper_Fast_API
```

Create an .env file and fill it.

Run docker-compose with 

```bash
  docker-compose up --build
```

And all done!

You can find api doc [here](http://127.0.0.1:8000/docs)