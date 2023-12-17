from http import HTTPStatus

from flask import Flask, request, abort
from flask_restful import Resource, Api

from modelsApi import Movie as MovieModel
from modelsApi import Laptop as LaptopModel

app = Flask(__name__)
api = Api(app)
      
class Movie(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next = None
        if page > 1:
            prev = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev = None

        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next,
            'prev': prev,
            'Results': list[start:end]
        }

    def get(self):
        movie = MovieModel()
        return self.get_paginated_result('movies/', movie.film_data, request.args), HTTPStatus.OK.value

class Laptop(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next = None
        if page > 1:
            prev = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev = None

        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.')
        return {
            'page': page,
            'page_size': page_size,
            'next': next,
            'prev': prev,
            'Results': list[start:end]
        }

    def get(self):
        Laptop = LaptopModel()
        return self.get_paginated_result('laptop/', Laptop.lpt_data, request.args), HTTPStatus.OK.value


class Rekomendasi(Resource):
    def post(self):
        data = request.get_json()
        ID = data.get('ID')
        length = data.get('length', 10)
        Laptop = LaptopModel()

        if not ID:
            return 'ID is empty', HTTPStatus.BAD_REQUEST.value

        if not Laptop.lpt_data_dict.get(ID):
            return 'ID is not found', HTTPStatus.NOT_FOUND.value

        recom = Laptop.get_recs(ID, int(length))
        results = [{'ID': int(rec[0]), 'Type': rec[1], 'score': round(
            rec[10] * 100, 2)} for rec in recom]

        return {
            'ID': int(ID),
            'Type': Laptop.lpt_data_dict[ID],
            'recom': results
        }, HTTPStatus.OK.value


api.add_resource(Movie, '/movies')
api.add_resource(Rekomendasi, '/rekomendasi')
api.add_resource(Laptop, '/laptop')
api.add_resource(Rekomendasi, '/recom')

if __name__ == '__main__':
    app.run(port='5005', debug=True)