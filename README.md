# api-spotify
A script to retrieve data from the **spotify API** and generate a csv file with the **top 50 songs by country**.
For the script to work correctly, a **client_id** and **secret_id** must be passed to the following os.environ.get() functions:

```python
id = os.environ.get('ID')
secret = os.environ.get('SECRET')
```

In order to achieve this, the script is looking for a **.env** file outside of the repository. The layout of the repository should be as follows:

```
ID = "your_custom_client_id"
CLIENT = "your_custom_client_id"
```

To get this ids, the Spotify API requires to create a free app in the **Spotify for Developers** webpage (https://developer.spotify.com/).
