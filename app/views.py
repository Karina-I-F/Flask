from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app
from app.models import User, Ads
from app.validator import validate
from schema import USER, AD


# проверяет приложение
@app.route('/health/', methods=['GET'])
def health_check():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

    return {'status': 'OK'}


# авторизует пользователя
@app.route('/api/v1.0/login', methods=['POST'])
@validate('json', USER)
def login():
    user = User.authenticate(**request.json)
    token = user.get_token()
    return {'access_token': token}


class UserView(MethodView):
    # возвращает одного пользователя
    def get(self, user_id):
        user = User.by_id(user_id)
        return jsonify(user.to_dict())

    # добавляет нового пользователя
    @validate('json', USER)
    def post(self):
        user = User(**request.json)
        user.add()
        token = user.get_token()
        return jsonify(user.to_dict(), {'access_token': token})


class AdsView(MethodView):
    # возвращает все объявления
    def get(self):
        ads = Ads.query.all()
        ads_list = [x.title for x in ads]
        return jsonify({'Содержит объявления': ads_list})

    # добавляет новое объявление
    @jwt_required()
    @validate('json', AD)
    def post(self):
        user_id = get_jwt_identity()
        ad = Ads()
        ad.title = request.json.get('title')
        ad.description = request.json.get('description')
        ad.user_id = user_id
        ad.add()
        json_resp = jsonify({'title': ad.title, 'description': ad.description})
        return json_resp

    # удаляет одно объявление
    @jwt_required()
    def delete(self, ad_id):
        user_id = get_jwt_identity()
        ad = Ads.query.get_or_404(ad_id)

        if ad.user_id == user_id:
            Ads.by_id(ad_id).delete()
            return jsonify({'Удалено': ad.title})
        else:
            return jsonify({'Status': 'Не удалено! Это может сделать только автор объявления.'}), 400

    # изменяет одно объявление
    @jwt_required()
    def put(self, ad_id):
        user_id = get_jwt_identity()
        ad = Ads.query.get_or_404(ad_id)
        if ad.user_id == user_id:
            updated = []
            if request.json.get('title'):
                ad.title = request.json.get('title')
                updated.append({'Обновлён заголовок': ad.title})
            if request.json.get('description'):
                ad.description = request.json.get('description')
                updated.append({'Обновлено описание': ad.description})
            ad.add()
            if not updated:
                return jsonify('Изменений нет.')
            return jsonify(updated)
        else:
            return jsonify({'Status': 'Не изменено! Это может сделать только автор объявления.'}), 400


app.add_url_rule('/api/v1.0/users/<int:user_id>',
                 view_func=UserView.as_view('get_user'),
                 methods=['GET'])
app.add_url_rule('/api/v1.0/register',
                 view_func=UserView.as_view('create_user'),
                 methods=['POST'])

app.add_url_rule('/api/v1.0/ads',
                 view_func=AdsView.as_view('get_ads'),
                 methods=['GET'])
app.add_url_rule('/api/v1.0/ads/',
                 view_func=AdsView.as_view('create_ad'),
                 methods=['POST'])
app.add_url_rule('/api/v1.0/ads/<int:ad_id>',
                 view_func=AdsView.as_view('target_ads'),
                 methods=['PUT', 'DELETE'])
