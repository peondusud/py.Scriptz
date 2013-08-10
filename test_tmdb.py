import tmdb
api_key="838c66a69f92542c658a03da687b8b99"
tmdb.configure(api_key)
# Search for movie titles containing "Alien"
movies = tmdb.Movies("Alien")
for movie in movies.iter_results():
    # Pick the movie whose title is exactly "Alien"
    if movie["title"] == "Alien":
        # Create a Movie object, fetching details about it
        movie = tmdb.Movie(movie["id"])
        break
# Access the fetched information about the movie
movie.get_tagline() # or other methods...
