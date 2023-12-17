from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
import numpy as np
import pandas as pd

Base = declarative_base()


class Laptop(Base):
    __tablename__ = "laptop"
    no = Column(Integer, primary_key=True)
    merek = Column(String(255))
    ram = Column(String(255))
    sistem_operasi = Column(String(255))
    baterai = Column(String(255))
    ukuran_layar = Column(String(255))
    harga = Column(String(255))
    memori_internal = Column(String(255))

    def __init__(self, merek, ram, sistem_operasi, baterai, ukuran_layar, harga, memori_internal):
        self.merek = merek
        self.ram = ram
        self.sistem_operasi = sistem_operasi
        self.baterai = baterai
        self.ukuran_layar = ukuran_layar
        self.harga = harga
        self.memori_internal = memori_internal

    def calculate_score(self, dev_scale):
        score = 0
        score += self.ram * dev_scale['ram']
        score += self.sistem_operasi * dev_scale['sistem_operasi']
        score += self.baterai * dev_scale['baterai']
        score += self.ukuran_layar * dev_scale['ukuran_layar']
        score -= self.harga * dev_scale['harga']
        score += self.memori_internal * dev_scale['memori_internal']
        return score

    def __repr__(self):
        return f"Laptop(merek={self.merek!r}, ram={self.ram!r}, sistem_operesi={self.sistem_operasi!r}, baterai={self.baterai!r}, ukuran_layar={self.ukuran_layar!r}, harga={self.harga!r}, memori_internal={self.memori_internal!r})"


class Movie():
    def __init__(self) -> None:
        self.movies = pd.read_csv('ml-latest-small/movies.csv')
        self.matrix = pd.read_csv('ml-latest-small/matrix_by_id.csv')
        self.films = np.array(self.movies)

    @property
    def film_data(self):
        data = []
        for film in self.films:
            data.append({'movie_id': film[0], 'movie_title': film[1]})
        return data

    @property
    def film_data_dict(self):
        data = {}
        for film in self.films:
            data[film[0]] = film[1]
        return data

    def pearson(self, s1, s2):
        s1_c = s1-s1.mean()
        s2_c = s2-s2.mean()
        return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))

    def get_recs(self, movie_id, num):
        reviews = []
        movie_id = str(movie_id)
        for id in self.matrix.columns:
            if id == movie_id:
                continue
            cor = self.pearson(self.matrix[movie_id], self.matrix[id])
            if np.isnan(cor):
                continue
            else:
                reviews.append((id, cor))
            reviews.sort(key=lambda tup: tup[1], reverse=True)
        return reviews[:num]


class Laptop():
    def __init__(self) -> None:
        self.lp = pd.read_csv('ml-latest-small/UAS_SPK.csv')
        self.matrix_lp = pd.read_csv('ml-latest-small/Matrix_UAS_SPK.csv')
        self.lptp = np.array(self.lp)

    @property
    def lpt_data(self):
        data = []
        for lpt in self.lptp:
            data.append({'no': lpt[0],'merek': lpt[1]})
        return data

    @property
    def lpt_data_dict(self):
        data = {}
        for lpt in self.lptp:
            data[lpt[0]] = lpt[1] 
        return data
    
    def pearson(self, s1, s2):
        s1_c = s1-s1.mean()
        s2_c = s2-s2.mean()
        return np.sum(s1_c*s2_c)/np.sqrt(np.sum(s1_c**2)*np.sum(s2_c**2))
    
    def get_recs(self, no, num):
        reviews = []
        no = str(no)
        for no in self.matrix_lp.columns:
            if no == no:
                continue
            cor = self.pearson(self.matrix_lp[no], self.matrix_lp[no])
            if np.isnan(cor):
                continue
            else:
                reviews.append((no, cor))
            reviews.sort(key=lambda tup: tup[1], reverse=True)
        return reviews[:num]