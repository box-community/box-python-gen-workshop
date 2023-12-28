<img src="images/box-dev-logo.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>


# Box Python Workshops
This project contains workshops on how to use the Box Python SDK to interact with the Box API.


## Box configuration steps

1. Create a [Box free account](https://www.box.com/pricing/individual) if you don't already have one.
2. Complete the registration process for a Box developer account.
3. Making sure you're logged in navigate to the [Box Developer Console](https://app.box.com/developers/console). This will activate your developer account.
4. Create a new Box application. Select Custom App, fill in the form and then click Next.
5. Select User Authentication (OAuth 2.0) and then click Create App.
6. Scroll down to Redirect URIs and add the following redirect URI:
    - http://127.0.0.1:5000/callback
    - (or whatever you have configured in the .env file)
7. Check all boxes in application scopes.
    - (or only what you think will be necessary)
8. Click Save Changes.
9. Note the Client ID and Client Secret. You will need these later.

## Installation and configuration

### Get the code
```bash
git clone git@github.com:barduinor/box-python-gen-workshop.git
cd box-python-gen-workshop
```

### Set up your virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Create your local application environment file
```bash
cp sample_oauth.env .oauth.env
```

### Open the code in the code editor of your choice.
```
code .
```

`Update the CLIENT_ID and CLIENT_SECRET field values in the env file with the Box application client id and client secret you created on the developer console.
Depending on the workshop you are working on, you may need to update other environment variables in the .env file.`
```bash
# Common settings
CLIENT_ID = YOUR_CLIENT_ID
CLIENT_SECRET = YOU_CLIENT_SECRET

# OAuth2 settings
CALLBACK_HOSTNAME = 127.0.0.1
CALLBACK_PORT = 5000
REDIRECT_URI = http://127.0.0.1:5000/callback

```

## Test the application 
Depending on the type of authentication you'll be using test the associated files.

```bash
python test_oauth.py
```

The first time you run the application, it should open a web browser window and prompt you to log in to Box. 
After you log in, it will ask you to authorize the application.
Once this process is complete you can close the browser window.
By default the sample app prints the current user's name to the console, and lists the items on the root folder.

The authorization token last for 60 minutes, and the refresh toke for 60 days.
If you get stuck, you can delete the .oauth.tk.db file and reauthorize the application.

JWT or CCG authentication **will not** require you to log in to Box.

### Questions
If you get stuck or have questions, make sure to ask on our [Box Developer Forum](https://forum.box.com/c/box-platform/box-workshops/50)

# Workshops
You'll find the workshop exercises in the [workshops](workshops) folder.
* [Folders](workshops/folders/folders.md) - List, recursion, create, update, rename, copy, error handling, and delete
* [Files](workshops/files/files.md) - Upload, download, update, move, copy, error handling, and delete
* [File Comments](workshops/comments/comments.md) - Interact with the activity feed and comments
* [File Collaboration](workshops/collaboration/collaboration.md) - Create and manage collaborations
* [File Requests](workshops/file_requests/file_requests.md) - Create and manage file requests
* [Search](workshops/search/search.md) - Using search in the Box API
* [Shared Links](workshops/shared_links/shared_links.md) - Create and manage shared links
* [File Representations](workshops/file_representations/file_representations.md) - Working with file representations
* [Sign - Unstructured documents](workshops/sign/) - Working with Sign, and simple documents. Includes most features of the Sign request.
* [Sign Templates](workshops/sign_templates/) - Working with Sign Templates.
* [Sign Structured documents](workshops/sign_structured/) - Working with Sign Structured documents.
* [Tasks](workshops/tasks/) - Working with Tasks.
