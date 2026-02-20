
CREATE TABLE Song (
  songId INT AUTO_INCREMENT,
  songName VARCHAR(60) NOT NULL,
  songLengthSecs INT NOT NULL,
  genre VARCHAR(60) NOT NULL,
  numStreams BIGINT NOT NULL,
  PRIMARY KEY (songId)
);

CREATE TABLE Artist (
  artistId INT AUTO_INCREMENT,
  artistName VARCHAR(60) NOT NULL,
  PRIMARY KEY (artistId)
);

CREATE TABLE ArtistSong(
  songId INT NOT NULL,
  artistId INT NOT NULL,
  isFeatured BOOLEAN NOT NULL,
  PRIMARY KEY (songId, artistId),
  FOREIGN KEY (songId) REFERENCES Song(songId)
    ON DELETE CASCADE,
  FOREIGN KEY (artistId) REFERENCES Artist(artistId)
    ON DELETE CASCADE
);

CREATE TABLE Album (
  albumId INT AUTO_INCREMENT,
  albumName VARCHAR(60) NOT NULL,
  artistId INT NOT NULL,
  albumLength INT NOT NULL,
  releaseDate DATE,
  PRIMARY KEY (albumId),
  FOREIGN KEY (artistId) REFERENCES Artist(artistId)
    ON DELETE CASCADE
);

CREATE TABLE AlbumSong(
  songId INT NOT NULL,
  albumId INT NOT NULL,
  trackNum INT NOT NULL,
  PRIMARY KEY (songId, albumId),
  FOREIGN KEY (songId) REFERENCES Song(songId)
    ON DELETE CASCADE,
  FOREIGN KEY (albumId) REFERENCES Album(albumId)
    ON DELETE CASCADE
);

CREATE TABLE BAND(
  bandId INT AUTO_INCREMENT,
  startDate DATE NOT NULL,
  endDate DATE,
  PRIMARY KEY (bandId),
  FOREIGN KEY (bandId) REFERENCES Artist(artistId)
    ON DELETE CASCADE
);

CREATE TABLE BandMember(
  artistId INT NOT NULL,
  bandId INT NOT NULL,
  bandName VARCHAR(60),
  PRIMARY KEY (artistId, bandId),
  FOREIGN KEY (artistId) REFERENCES Artist(artistId)
    ON DELETE CASCADE,
  FOREIGN KEY (bandId) REFERENCES Band(bandId)
    ON DELETE CASCADE
);




