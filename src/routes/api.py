from flask import Blueprint, jsonify, current_app, request
from src.controllers.openai import generate_project_names
import requests
api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    current_app.logger.debug(f'data received: {data}')
    names = generate_project_names(
        data['ideaDescription'],
        data['creativityLevel'],
        data['keywords'])
    current_app.logger.debug(f'names generated: {names}')
    available_names = [
        name for name in names if check_domain_avalibility(name)]
    current_app.logger.debug(f'available names: {available_names}')

    # if no names are available, try generating names again up to 3 times
    if len(available_names) == 0:
        for _i in range(3):
            names = generate_project_names(
                data['ideaDescription'],
                data['creativityLevel'],
                data['keywords'])
            available_names = [
                name for name in names if check_domain_avalibility(name)]
            if len(available_names) > 0:
                break

    # get search results count for each name
    output = []
    for name in available_names:
        output.append({
            'name': name,
            'searchResultsCount': get_google_search_results(name)
        })

    return jsonify(output)


def check_domain_avalibility(domain):
    url = f"https://api.whoapi.com/?domain={domain}&r=taken&apikey={current_app.config['WHOAPI_KEY']}"  # noqa: E501
    response = requests.get(url)
    return response.json()['taken'] == 0


def get_google_search_results(domain):
    url = f"https://www.googleapis.com/customsearch/v1?key={current_app.config['GOOGLE_API_KEY']}&cx=d632532c9f01045e5&q={domain}"  # noqa: E501
    # get search results count
    response = requests.get(url)
    return response.json()['searchInformation']['totalResults']
