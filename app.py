from flask import Flask, jsonify, request

import requests

from bs4 import BeautifulSoup

import os

app = Flask(__name__)

@app.route('/', methods=['GET'])

def get_images():

    search_term = request.args.get('search')

    url = f"https://www.google.com/search?q={search_term}&source=lnms&tbm=isch"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    image_urls = []

    num_downloaded = 0

    for img in soup.find_all('img'):

        try:

            img_url = img['src']

            response = requests.get(img_url)

            if response.status_code == 200:

                image_urls.append(img_url)

                with open(os.path.join(search_term, os.path.basename(img_url)), 'wb') as f:

                    f.write(response.content)

                num_downloaded += 1

                if num_downloaded == 20:

                    break

        except:

            pass

    return jsonify({'image_urls': image_urls, 'num_images': len(image_urls)})

if __name__ == '__main__':

    app.run(debug=True)

