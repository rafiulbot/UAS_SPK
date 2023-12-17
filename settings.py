USER = 'postgres'
PASSWORD = '1234'
HOST = 'localhost'
PORT = '5432'
DATABASE_NAME = 'uas_spk'

DEV_SCALE = {
    'ram': {
        '32 gb': 5,
        '16 gb': 4,
        '12 gb': 3,
        '8 gb': 1,
    },
    'sistem_operasi': {
        'Windows 11 Home': 5,
        'macOS Monterey': 4,
        'Windows 11 Pro': 3,
        'Windows 11 Home': 2,
        'Windows 11 Home': 1,
    },
    'baterai': {
        '9920 mAh': 5,
        '8640 mAh': 5,
        '7680 mAh': 4,
        '7040 mAh': 4,
        '6400 mAh': 3,
        '5800 mAh': 3,
        '4800 mAh': 2,
        '4000 mAh': 1,
    },
    'ukuran_layar': {
        '15,6 inci': 5,
        '14 inci': 4,
        '13,3 inci': 3,
        '13 inci': 2,
    },
    'harga': {
        '<= 4999000': 5,
        '10999000 - 12999000': 4,
        '12999000 - 23999000': 3,
        '23999000 - 29999000': 2,
        '49999000 >=': 1,
    },
    'memori_internal': {
        '2048 gb ssd': 5,
        '1024 gb ssd': 4,
        '512 gb ssd ': 3,
        '256 gb ssd': 2,
        '128 gb ssd': 1,
    },
}