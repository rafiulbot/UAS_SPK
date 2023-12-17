from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import Laptop as LaptopModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from tabulate import tabulate

session = Session(engine)

app = Flask(__name__)
api = Api(app)

class BaseMethod:
    def __init__(self):
        # 1-5
        self.raw_weight = {
            "ram": 2,
            "memori_internal": 4,
            "sistem_operasi": 2,
            "ukuran_layar": 3,
            "harga": 5,
            "baterai": 5,
        }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v / total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(
            LaptopModel.no,
            LaptopModel.merek,
            LaptopModel.ram,
            LaptopModel.sistem_operasi,
            LaptopModel.baterai,
            LaptopModel.ukuran_layar,
            LaptopModel.harga,
            LaptopModel.memori_internal,
        )
        result = session.execute(query).fetchall()
        return [
            {
                "no": Laptop.no,
                "merek": Laptop.merek,
                "ram": Laptop.ram,
                "sistem_operasi": Laptop.sistem_operasi,
                "baterai": Laptop.baterai,
                "ukuran_layar": Laptop.ukuran_layar,
                "harga": Laptop.harga,
                "memori_internal": Laptop.memori_internal,
            }
            for Laptop in result
        ]

    @property
    def normalized_data(self):
        ram_values = []  # max
        sistem_operasi_values = []  # max
        baterai_values = []  # max
        ukuran_layar_values = []  # max
        harga_values = []  # min
        memori_internal_values = []  # max

        for data in self.data:
            # RAM
            ram_spec = data['ram']
            ram_numeric_values = [
                int(value) for value in ram_spec.split() if value.isdigit()]
            max_ram_value = max(
                ram_numeric_values) if ram_numeric_values else 1
            ram_values.append(max_ram_value)

            # Sistem Operasi
            sistem_operasi_spec = data["sistem_operasi"]
            numeric_values = [
                int(value.split()[0])
                for value in sistem_operasi_spec.split(",")
                if value.split()[0].isdigit()
            ]
            max_sistem_operasi_value = max(numeric_values) if numeric_values else 1
            sistem_operasi_values.append(max_sistem_operasi_value)

            # Baterai
            baterai_spec = data['baterai']
            baterai_numeric_values = [int(
                value.split()[0]) for value in baterai_spec.split() if value.split()[0].isdigit()]
            max_baterai_value = max(
                baterai_numeric_values) if baterai_numeric_values else 1
            baterai_values.append(max_baterai_value)

            # Ukuran Layar
            ukuran_layar_spec = data["ukuran_layar"]
            ukuran_layar_numeric_values = [
                float(value.split()[0])
                for value in ukuran_layar_spec.split()
                if value.replace(".", "").isdigit()
            ]
            max_ukuran_layar_value = (
                max(ukuran_layar_numeric_values) if ukuran_layar_numeric_values else 1
            )
            ukuran_layar_values.append(max_ukuran_layar_value)

            # Harga
            harga_cleaned = "".join(char for char in data["harga"] if char.isdigit())
            harga_values.append(
                float(harga_cleaned) if harga_cleaned else 0
            )  # Convert to float

            # Memori Internal
            memori_internal_spec = data["memori_internal"]
            memori_internal_numeric_values = [
                int(value.split()[0])
                for value in memori_internal_spec.split()
                if value.split()[0].isdigit()
            ]
            max_memori_internal_value = (
                max(memori_internal_numeric_values)
                if memori_internal_numeric_values
                else 1
            )
            memori_internal_values.append(max_memori_internal_value)

        return [
            {"no": data["no"],
             "ram": ram_value / max(ram_values),
             "sistem_operasi": sistem_operasi_value / max(sistem_operasi_values),
             "baterai": baterai_value / max(baterai_values),
             "ukuran_layar": ukuran_layar_value / max(ukuran_layar_values),
             "harga": min(harga_values) / max(harga_values) if max(harga_values) != 0 else 0,
             "memori_internal": memori_internal_value
                / max(memori_internal_values),
            }
            for data, ram_value, sistem_operasi_value, baterai_value, ukuran_layar_value, harga_value, memori_internal_value in zip(
            self.data,
            ram_values,
            sistem_operasi_values,
            baterai_values,
            ukuran_layar_values,
            harga_values,
            memori_internal_values,
                )
        ]
    
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                "no": row["no"],
                "produk": row["ram"] ** self.weight["ram"] *
                row["memori_internal"] ** self.weight["memori_internal"] *
                row["sistem_operasi"] ** self.weight["sistem_operasi"] *
                row["ukuran_layar"] ** self.weight["ukuran_layar"] *
                row["harga"] ** self.weight["harga"] *
                row["baterai"] ** self.weight["baterai"]
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x["produk"], reverse=True)
        sorted_data = [
            {
                'no': product['no'],
                'score': product['produk']  # Nilai skor akhir
            }
            for product in sorted_produk
        ]
        return sorted_data

class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return sorted(result, key=lambda x: x['score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'laptop': sorted(result, key=lambda x: x['score'], reverse=True)}, HTTPStatus.OK.value

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {
            row["no"]: 
            round(
                row["ram"] * weight["ram"] +
                row["memori_internal"] * weight["memori_internal"] +
                row["sistem_operasi"] * weight["sistem_operasi"] +
                row["ukuran_layar"] * weight["ukuran_layar"] +
                row["baterai"] * weight["baterai"] +
                row["harga"] * weight["harga"] ,2)
            for row in self.normalized_data
        }
        sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result
    
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return sorted(result, key=lambda x: x['Score'], reverse=True), HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'laptop': sorted(result, key=lambda x: x['Score'], reverse=True)}, HTTPStatus.OK.value

class Laptop(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None

        if page > page_count or page < 1:
            abort(404, description=f'Data Tidak Ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next_page,
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = session.query(LaptopModel).order_by(LaptopModel.no)
        result_set = query.all()
        data = [{'no': row.no, 'merek': row.merek, 'ram': row.ram, 'sistem_operasi': row.sistem_operasi,
                 'baterai': row.baterai, 'ukuran_layar': row.ukuran_layar, 'harga': row.harga, 'memori': row.memori_internal}
                for row in result_set]
        return self.get_paginated_result('laptop/', data, request.args), 200

api.add_resource(Laptop, '/laptop')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)
