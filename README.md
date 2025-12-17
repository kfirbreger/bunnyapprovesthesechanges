# Bunny Approves These Changes

A fun WSGI application that generates ASCII art bunnies with random commit-related messages. Inspired by [whatthecommit.com](http://whatthecommit.com/).

## Example Output

```
(\ /)
(^.^)
(> <) Bunny approves these changes
```

## Endpoints

- `/` or `/index.html` - HTML formatted bunny
- `/txt` or `/index.txt` - Plain text bunny
- `/py` or `/index.py` - Python docstring formatted bunny

## Running with Docker

```bash
docker build -t commit-bunnies .
docker run -p 8000:8000 commit-bunnies
```

## Running Locally

```bash
pip install -r requirements.txt
uwsgi --ini bunnies.ini
```
