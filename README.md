# Emailer
Emailer is a django application to send mass email.

## Setup Instructions
-   Clone the repository: `git clone git@github.com:subodhu/emailer.git`
-   Change directory: `cd emailer`
- Install [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/) if not already installed.
- Build `docker compose build`
- And run the application `docker compose up`

After running the application, you can view the swagger docs in [localhost:8000](localhost:8000). A simple fixture with admin user and email template is also in fixtures directory. You can load the fixture with`docker-compose run --rm django python manage.py loaddata fixtures/data.json`. Now create another user, and you can send emails by calling the `/api/v1/emails/` API within swagger or using postman.
