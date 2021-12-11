import os
import shutil

import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML
from flask import Flask, redirect, render_template, request, send_file, url_for

# user can input a topic and a number
# download first n images from google image search
GOOGLE_IMAGE = \
    'https://www.google.com/search?q='

# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search

QUERY = \
    '&safe=strict&sxsrf=ALeKk01gsJC0DMC32-V0naiI6atL-e3Fbg:1605183344756&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi10cD4_fzsAhXJZSsKHZFFDdAQ_AUoAXoECCMQAw&biw=1680&bih=970'


SAVE_FOLDER = 'images'

cwd = os.getcwd()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def search_images():
    data = request.form['data']
    n_images = request.form['n_images']
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    result = download_images(data, n_images)
    path = archive_files(result)
    return send_file(path, as_attachment=True)


@app.route('/clear')
def clear_images():
    shutil.rmtree(SAVE_FOLDER)
    return redirect(url_for("index"))


def archive_files(result):
    path = SAVE_FOLDER + '/' + result
    shutil.make_archive(os.path.join(cwd, path),
                        'zip', os.path.join(cwd, path))
    path = path+".zip"
    return path


def download_images(data, n_images):
    # ask for user input
    # data = input('What are you looking for? ')
    # n_images = int(input('How many images do you want? '))
    n_images = int(n_images)
    print('Start searching...')

    # get url query string
    searchurl = GOOGLE_IMAGE + data + QUERY
    print(searchurl)

    page = requests.get(searchurl).text

    # find all img tags where class='t0fcAb'
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all(
        'img', limit=n_images)
    # extract the link from the img tag
    imagelinks = []
    for re in results:
        link = re.get('src')
        imagelinks.append(link)
        print(link)

    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open image link and save as file
        try:
            response = requests.get(imagelink)
            image_path = SAVE_FOLDER + '/' + data
            if not os.path.exists(image_path):
                os.mkdir(image_path)

            imagename = image_path + '/' + data + str(i+1) + '.jpeg'
            with open(imagename, 'wb') as file:
                file.write(response.content)
        except:
            pass

    result = data
    return result
