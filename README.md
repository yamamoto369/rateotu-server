# Restaurant at the end of the universe

Frontend clients for guests and staff.

## Running

Running both apps is simply if you have `make` and `python3` installed:

### Guest app

`make guest`

will start simple Python HTTP server on port 8081, therefore guest application should be available at `http://localhost:8081`.

### Staff app

`make staff`

will start simple Python HTTP server on port 8082, therefore guest application should be available at `http://localhost:8082`.

## Working with custom server

In order to connect frontend clients to a custom server, modify `guest-app/index.html` and `staff-app/index.html` files.

Find a line starting with `const BASE_URL = "..."` , replace the value with your custom server base URL, and you should be ready to go.