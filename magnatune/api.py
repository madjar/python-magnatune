# -*- coding: utf-8 -*-

import time
import requests
import os
import gzip
from magnatune.config import config_dir

from sqlalchemy import (create_engine, Column, Integer, String, Table, Text,
                        ForeignKey)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


import logging

logger = logging.getLogger(__name__)

CRC_URL = 'http://he3.magnatune.com/info/changed.txt'
DB_URL = 'http://he3.magnatune.com/info/sqlite_normalized.db.gz'

CRC_FILE = os.path.join(config_dir, 'changed.txt')
DB_FILE = os.path.join(config_dir, 'sqlite_normalized.db')


def download():
    """
    Downloads the last version of the api file from the server.
    """
    data = requests.get(DB_URL, stream=True).raw
    with gzip.GzipFile(fileobj=data) as gzfile, open(DB_FILE, 'wb') as f:
        f.write(gzfile.read())


def update_if_needed():
    """
    Checks if an update of the api file if needed, and download it if needed.
    """
    if os.path.exists(CRC_FILE):
        updated = os.stat(CRC_FILE).st_mtime
        if time.time() - updated < 60 * 60 * 24:  # 24 hours
            logger.debug(
                'Database file updated less than 24 hours, not updating.')
            return

        with open(CRC_FILE, 'rb') as f:
            crc = f.read()
    else:
        crc = None

    logger.info('Updating CRC file')
    new_crc = requests.get(CRC_URL).content

    if crc == new_crc:
        logger.debug('Database file up-to-date.')
        return

    logger.info('Updating database file.')
    download()

    with open(CRC_FILE, 'wb') as f:
        f.write(new_crc)


def get_session():
    """Returns a session to access the database, updating it before if
    needed"""
    update_if_needed()
    engine = create_engine('sqlite:///' + DB_FILE)
    Session = sessionmaker(bind=engine)
    return Session()

Base = declarative_base()
metadata = Base.metadata


t_genres_albums = Table(
    'genres_albums', metadata,
    Column('genre_id', Integer, ForeignKey('genres.genre_id'), index=True),
    Column('album_id', Integer, ForeignKey('albums.album_id'), index=True)
)


t_playlist_songs = Table(
    'playlist_songs', metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.playlist_id'),
           index=True),
    Column('sort_order', Integer),
    Column('song_id', Integer, ForeignKey('songs.song_id'))
)


class Album(Base):
    __tablename__ = 'albums'

    album_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artists_id'), index=True)
    name = Column(Text, index=True)
    description = Column(Text)
    sku = Column(Text)
    upc = Column(String)
    release_date = Column(Integer)
    popularity = Column(Integer)
    itunes_buy_url = Column(Text)

    artist = relationship('Artist', backref=backref('albums',
                                                    order_by=release_date))

    _genres = relationship('Genre', secondary=t_genres_albums, backref='songs')
    genres = association_proxy('_genres', 'name')


class Artist(Base):
    __tablename__ = 'artists'

    artists_id = Column(Integer, primary_key=True)
    name = Column(Text, index=True)
    description = Column(Text)
    homepage = Column(Text)
    bio = Column(Text)
    photo = Column(Text)


class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    name = Column(Text)


class Playlist(Base):
    __tablename__ = 'playlists'

    playlist_id = Column(Integer, primary_key=True)
    sort_order = Column(Integer)
    owner_id = Column(Integer)
    name = Column(Text)

    songs = relationship('Song', secondary=t_playlist_songs,
                         order_by=t_playlist_songs.c.sort_order)


class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.album_id'), index=True)
    name = Column(Text)
    track_no = Column(Integer)
    duration = Column(Integer)
    mp3 = Column(Text)

    album = relationship(Album, backref=backref('songs', order_by=track_no))
