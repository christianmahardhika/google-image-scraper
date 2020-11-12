import os
import requests  # to sent GET requests
from bs4 import BeautifulSoup  # to parse HTML

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


def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()


def download_images():
    # ask for user input
    data = input('What are you looking for? ')
    n_images = int(input('How many images do you want? '))

    print('Start searching...')

    # get url query string
    searchurl = GOOGLE_IMAGE + data + QUERY
    print(searchurl)

    page = requests.get(searchurl).text

    # find all img tags where class='t0fcAb'
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.findAll('img', {'class': 't0fcAb'}, limit=n_images)
    # extract the link from the img tag
    imagelinks = []
    for re in results:
        link = re.get('src')
        imagelinks.append(link)

    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open image link and save as file
        response = requests.get(imagelink)
        image_path = SAVE_FOLDER + '/' + data
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        imagename = image_path + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == '__main__':
    main()
