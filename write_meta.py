import meta



source = "source.mkv" 
new_file ="RENAME.mkv"
IMDB_id = "145852"
addIMDB = (ffmpeg -i str(source) -vcodec copy -acodec copy -metadata IMDB=str(IMDB_id) str(new_file))
