# matchmaking-match-api
Matching api for the matchmaking product. cima ecosystem.



Run on flask development server:
```
flask --app matchapi run --host=0.0.0.0 --port=8000 --debug
```


Run on gunicorn production server
```
gunicorn -w=4 -b=0.0.0.0:80 matchapi:app --access-logfile=-
```
