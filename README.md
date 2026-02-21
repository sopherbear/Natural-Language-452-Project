# CS 452 Natural Language Project
This program uses a SongInfo Database that has the following tables:
* Song
* Artist
* ArtistSong
* Album
* AlbumSong
* Band
* BandMember


The database contains songs from the following artists:
* Gorillaz
* Blur
* Graham Coxon
* De la Soul
* Tom Misch
* Little Dragon
* Djo
  
... and keeps track of all the members of each band, some of whom are also solo artists. 

The purpose of the database is to keep track of songs, albums, the artists on those albums, and members of bands.


db_bot_interactions.py contains the script for getting queries from chat, getting resulting data from the database, and getting interpretations from chat.

## Results

I found that the zero-shot queries were usually ok, but that I needed to clarify concepts like featuring for them to work. Otherwise, chat didn't know how to tell what songs belonged to an artist and which ones they only featured on. 

My single-domain response also had this problem with multiple queries. Otherwise, it performed comparably. 

I found that my prompts greatly impacted chat's quality of responses. If I told it to tell me the data, it listed it out concisely. If I asked it to describe the data, it was often vague and described what general content was returned, but not the actual artists or songs.