To run the project:

```sh
pip install -r requirements.txt
flask --app app run
```

Send a POST request with a JSON body:
```json
{"text": "Мама мыла раму. Папа мыл кота."}
```

to `http://127.0.0.1:5000/analyse`.
