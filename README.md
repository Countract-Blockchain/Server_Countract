# REST API Countrack

# Download and setup

Step-1: Creating venv
  ```bash
    python -m venv venv
    ./venv/Scripts/activate
  ```

Step-2: Installing Dependencies
  ```bash
    pip install -r requirements.txt
  ```

Step-3: Change to venv
  ```bash
    & venv/Scripts/Activate.ps1 
  ```

Step-4: Run The app
  ```bash
    python -u "app.py"
  ```

# How to Migrate
```bash
python -u "migration\migration.py"
```

# List API Countrack
## 1. Register User
```
method: POST
endpoint: "/user/add"
request form-data: {
    email, password
}
response(200): {
    "message":"CREATED_SUCCESSFULLY"
}
```

## 2. Login User
```
method: POST
endpoint: "/user/login"
request form-data: {
    email, password
}
response(200): {
    "token":"**token**"
}
```


## 3. Upload Document
```
method: POST
endpoint: "/dokumen/upload"
header: {
    Authorization
}
request form-data: {
    image-hidden(file), image-visible(file), jenis
}
response(200): {
    "status": "OK",
    "message": "Success"
}
```

## 4. Decode Hidden Image
```
method: POST
endpoint: "/dokumen/decode"
request form-data: {
    encoded_image(file)
}
response(200): {
    "url":"***[url-image]***"
}
```

## 5. Add Akses
```
method: POST
endpoint: "/akses/add"
header: {
    Authorization
}
request form-data: {
    user_id, dokumen_id
}
response(200): {
    "message":"CREATED_SUCCESSFULLY"
}
```

## 6. Get Document
```
method: POST
endpoint: "/dokumen"
header: {
    Authorization
}
request form-data: {
    jenis
}
response(200): {
    data: [
        {ID, path/url}
    ]
}
```
## 7. Get Other Person Document
```
method: POST
endpoint: "/dokumen/akses"
header: {
    Authorization
}
request form-data: {
    jenis, email_owner
}
response(200): {
    data: [
        {ID, path/url}
    ]
}
```