# Battery Charge Calculator

This is a simple Flask application to calculate the kWh needed to charge a car battery to 80%.

## Installation

1. Clone the repository.
2. Install dependencies using pipenv:
   ```bash
   pipenv install
   ```

## Running the Application

To run the development server:

```bash
pipenv run python app.py
```

The application will be available at `http://localhost:8888`.

### Logging

The app logs basic information by default. To troubleshoot issues, set the
`LOG_LEVEL` environment variable to `DEBUG` before starting the server:

```bash
LOG_LEVEL=DEBUG pipenv run python app.py
```

This enables more detailed messages about JSON file access and calculation
requests, which are helpful when diagnosing problems.

## Running Tests

To run the tests:

```bash
pipenv run python -m unittest test_app.py
```

## Running the Application in Production

To run the application with a production-ready WSGI server like Gunicorn:

```bash
pipenv run gunicorn --workers 3 --bind 0.0.0.0:8888 wsgi:app
```

## Deploying on a Raspberry Pi (or other Linux server)

For a robust deployment, you should run the application as a `systemd` service. This will allow the application to start automatically on boot and restart if it crashes.

1. **Copy the `my-app.service` file to the systemd directory:**

   ```bash
   sudo cp my-app.service /etc/systemd/system/
   ```

2. **Reload `systemd`, enable, and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable my-app.service
   sudo systemctl start my-app.service
   ```

    The service file exports the `VIRTUAL_ENV` variable and uses the
    virtual environment's `gunicorn` binary so the process runs inside the
    project's virtual environment. If your virtual environment lives in a
    different location, update the paths in `my-app.service` accordingly
    before reloading `systemd`.

    The unit runs as the `pi` user and uses its default group. If your
    system uses a different account, adjust the `User` directive (and add a
    `Group` directive if needed) before reloading `systemd`.

Now your application is running as a system service. You can check its status with:

```bash
sudo systemctl status my-app.service
```
