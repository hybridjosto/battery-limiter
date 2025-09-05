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

## Running Tests

To run the tests:

```bash
pipenv run python -m unittest test_app.py
```

## Deploying on a Raspberry Pi (or other Linux server)

To keep the server running after you exit your SSH session, you have a couple of options.

### Method 1: Using `nohup` (the simple way)

The `nohup` command (no hang up) is a simple way to run a command that will ignore the hangup signal, which is sent to processes when a terminal is closed.

1. **Navigate to your project directory:**
   ```bash
   cd /path/to/your/project
   ```

2. **Run the application with `nohup`:**
   ```bash
   nohup pipenv run python app.py &
   ```

The server will now be running in the background, and you can safely exit your SSH session. The output of the application will be redirected to a file named `nohup.out`.

You can check the output with:
```bash
cat nohup.out
```

### Method 2: Creating a `systemd` service (the robust way)

For a more robust solution, you can create a `systemd` service. This will allow the application to start automatically on boot, restart if it crashes, and manage logging more effectively.

1. **Create a service file:**

   Create a file named `my-app.service` with the following content:

   ```ini
   [Unit]
   Description=My Flask Application
   After=network.target

   [Service]
   User=pi
   WorkingDirectory=/path/to/your/project
   ExecStart=/usr/bin/pipenv run python app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   **Important:** You will need to edit this file and replace `/path/to/your/project` with the actual path to your project directory on the Raspberry Pi. You may also need to change the `User` to your username if it's not `pi`.

2. **Move the service file to the systemd directory:**
   ```bash
   sudo mv my-app.service /etc/systemd/system/my-app.service
   ```

3. **Reload `systemd`, enable, and start the service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable my-app.service
   sudo systemctl start my-app.service
   ```

Now your application is running as a system service. You can check its status with:

```bash
sudo systemctl status my-app.service
```
