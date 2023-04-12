# Meetup RSVP data stream processing 

___

## Index

- App structure
- Instructions
___

## Folder Structurre

<pre>
|- requirement.md
|- sample.json
|- backendService (For now, backend code)
|-- app.py
</pre>

___

## Instructions

### Backend 

- To run the application

```python
# /backgroundService/
$ flask --app app run #to run app.py locally. 
```

- To install the Flask (Virtual environment)

```python
# /backgroundService/
$ python3 -m venv venv 
$ . venv/bin/activate

$ pip3 install Flask
```