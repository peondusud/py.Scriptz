import tmdb
import sys
api_key="838c66a69f92542c658a03da687b8b99"
tmdb.configure(api_key)

movie_pattern = sys.argv[1]
movie_pattern = "benjamin gates"

movies = tmdb.Movies(movie_pattern)
for movie in movies.iter_results():
    # Pick the movie whose title is exactly "patern"
    if movie["title"] == movie_pattern:
        # Create a Movie object, fetching details about it
        movie = tmdb.Movie(movie["id"])
        # Access the fetched information about the movie
        print dir(movie)

    movie = tmdb.Movie(movie["id"])
    #for k,v in movie.movies.iteritems():
        #print k,v
    print "Title :",movie.get_title()
    print "Original Title :",movie.get_original_title()
    print "Release date :",movie.get_release_date()
    print "IMDB ID :",movie.get_imdb_id()
    tmdb_id= movie.get_id()
    print "TMDB ID :",tmdb_id

    dic_alternate = tmdb.Core().getJSON(tmdb.config['urls']['movie.alternativeti                                                                                      tles'] % tmdb_id)
    #print  dic_alternate
    print "Alternate Titles :"
    for elem in dic_alternate['titles']:
        if elem['iso_3166_1']== 'US' or elem['iso_3166_1'] == 'FR':
            print "\t",elem['iso_3166_1'],elem['title']
    print ""
