import os
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from models import setup_db, Dish, Ingredient
from auth import AuthError, requires_auth

MODELS_PER_PAGE = 5


def paginate_model(request, selection):
    if request:
        page = request.args.get('page', 1, type=int)
    else:
        page = 1
    start = (page-1)*MODELS_PER_PAGE
    end = start + MODELS_PER_PAGE
    models = [m.format() for m in selection]
    current_models = models[start:end]
    return current_models


def create_app(test_cfg=None, test_url=False):
    # create and configure the app
    app = Flask(__name__)
    if test_cfg:
        setup_db(app, test_cfg['DATABASE_URL'])
    elif test_url:
        setup_db(app, os.environ['DATABASE_URL_TEST'])
    else:
        setup_db(app, os.environ['DATABASE_URL'])

    CORS(app)
    '''
    Get ingredient by dish
    Get dish by allergen
    '''

    @app.route('/', methods=['POST', 'GET'])
    def health():
        """sanity check"""
        return jsonify("Healthy")

    @app.route('/dish', methods=['GET'])
    def get_dish_all():
        current_dish = paginate_model(request, Dish.query.all())
        result = {
                "success": True,
                "result": current_dish
        }
        return jsonify(result)

    @app.route('/dish/<int:dish_id>', methods=['GET'])
    def get_dish(dish_id):
        dish = Dish.query.get(dish_id)
        if not dish:
            abort(404)
        result = {
                "success": True,
                "result": dish.format()
        }
        return jsonify(result)

    @app.route("/dish", methods=["POST"])
    @requires_auth("post:menu")
    def post_dish(jwt):
        """Adds a dish. Requires authentication and permission"""
        try:
            res = request.get_json()
            if not res:
                abort(404)

            if 'name' in res and 'ingredient' in res:
                ing = res.pop('ingredient')
                dish = Dish(**res)

                if ing:
                    for i in ing:
                        ingredient = Ingredient(**i, dish_id=dish.id)
                        dish.ingredient.append(ingredient)

                dish.insert()
                result = {
                    "success": True,
                    "result": dish.format()
                }
                return jsonify(result)
        except TypeError:
            print(sys.exc_info())
            abort(400)

    @app.route("/dish/<int:dish_id>", methods=["PATCH"])
    @requires_auth("patch:menu")
    def patch_dish(jwt, dish_id):
        dish = Dish.query.get(dish_id)
        if not dish:
            abort(404)

        res = request.get_json()
        if not res or ("name" not in res and "ingredient" not in res):
            abort(400)

        if "name" in res:
            dish.name = res["name"]
        if "ingredient" in res:
            new_ingredients = []
            for i in res["ingredient"]:
                new_ingredient = Ingredient(**i, dish_id=dish.id)
                new_ingredients.append(new_ingredient)
            dish.ingredient = new_ingredients
        dish.update()

        result = {
            "success": True,
            "result": dish.format()
        }
        return jsonify(result)

    @app.route("/dish/<int:dish_id>", methods=["DELETE"])
    @requires_auth("delete:menu")
    def delete_dish(jwt, dish_id):
        dish = Dish.query.get(dish_id)
        if not dish:
            abort(404)

        dish.delete()
        return jsonify({
            "success": True,
            "result": dish_id
            })

    # ingredient
    @app.route('/ingredient', methods=['GET'])
    def get_ingredient_all():
        result = {
                "success": True,
                "result": [ingredient.format() for ingredient in Ingredient.query.all()]
        }
        return jsonify(result)

    @app.route('/ingredient/<int:ingredient_id>', methods=['GET'])
    def get_ingredient():
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            abort(404)

        return jsonify({
            "success": True,
            "result": ingredient.format()
        })

    @app.route('/ingredient', methods=['POST'])
    @requires_auth('post:menu')
    def post_ingredient(jwt):
        res = request.get_json()
        if not res:
            abort(404)

        ingredient = Ingredient(**res)
        ingredient.insert()
        result = {
            "success": True,
            "result": ingredient.format()
        }
        return jsonify(result)

    @app.route('/ingredient/<int:ingredient_id>', methods=['PATCH'])
    @requires_auth('patch:menu')
    def patch_ingredient(jwt, ingredient_id):
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            abort(404)

        res = request.get_json()
        items = ['dish_id', 'name', 'allergen']
        if not any([i in res for i in items]):
            abort(400)
        for item in items:
            setattr(ingredient, item, res[item])
        ingredient.update()

        return jsonify({
            "success": True,
            "result": ingredient.format()
        })

    # def paginate(request, selections):
    #     page = request.args.get('page', 1, type=int)
    #     page_size = 10
    #     start = (page - 1) * page_size
    #     end = start + page_size
    #     items = [s.format() for s in selections]
    #     return len(items), items[start:end]

    @app.route('/dish/search', methods=['POST'])
    def search_dish():
        res = request.get_json()
        search_term = res.get('searchTerm')

        if search_term:
            selection = Ingredient.query.filter(Ingredient.allergen.ilike('%{}%'.format(search_term)))
            # total_ing, ing = paginate(request, selection.all())
            items = [s.format() for s in selection.all()]
            if len(items) == 0:
                return jsonify({
                                'success': True,
                                'result': 'none',
                })

            dish_info = []
            for i in items:
                dish_id = i["dish_id"]
                dish_info.append(Dish.query.get(dish_id).format())

            return jsonify({
                'success': True,
                'result': dish_info,
            })

    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
                        "success": False,
                        "error": 400,
                        "message": "Bad request"
                        }), 400,
                )

    @app.errorhandler(401)
    def Unauthorized(error):
        return (jsonify({
                        "success": False,
                        "error": 401,
                        "message": "Unauthorized request"
                        }), 401,
                )

    @app.errorhandler(403)
    def unauthorized(error):
        return (
            jsonify({"success": False, "error": 403, "message": "forbidden"}),
            403,
                )

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404,
                )

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
                        "success": False,
                        "error": 422,
                        "message": "unprocessable"
                        }), 422
                )

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return (jsonify({
                        "success": False,
                        "error": 500,
                        "message": "Internal Server Error"
                        }), 500,
                )

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
