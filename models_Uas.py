from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


class Base(declarative_base):
    pass


class Laptop(Base):
    __tablename__ = "laptop"
    no = Mapped(Integer, primary_key=True)
    merek = Mapped(String(255))
    ram = Mapped(String(255))
    sistem_operasi = Mapped(String(255))
    baterai = Mapped(String(255))
    ukuran_layar = Mapped(String(255))
    harga = Mapped(String(255))
    memori_internal = Mapped(String(255))

    def __repr__(self):
        return f"Laptop(merek={self.merek!r}, ram={self.ram!r}, sistem_operesi={self.sistem_operasi!r}, baterai={self.baterai!r}, ukuran_layar={self.ukuran_layar!r}, harga={self.harga!r}, memori_internal={self.memori_internal!r})"