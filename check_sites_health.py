from datetime import datetime
import os
import re
import requests
import whois


def load_urls4check(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as file:
        urls_for_check = file.read().split('\n')
        return urls_for_check


def is_server_respond_with_200(url):
    server_respond = requests.get(url)
    return server_respond.status_code


def get_domain_name(url):
    domain_name = re.findall(r'\w+.\w+$', url)
    return domain_name


def get_domain_expiration_date(domain_name):
    domain_info = whois.whois(domain_name)
    expirated_date = domain_info.expiration_date
    if isinstance(expirated_date, list):
        return expirated_date[0]
    else:
        return expirated_date


def check_domain_expiration_date(expirated_date):
    if (expirated_date - datetime.now()).days <= 30:
        return 0
    else:
        return 1
      

if __name__ == '__main__':
    file_path = input('Enter full path for file with URLs for check: ')
    list_of_urls4check = load_urls4check(file_path)
    if list_of_urls4check is not None:
        for urls in list_of_urls4check:
            response = is_server_respond_with_200(urls)
            if response == 200:
                print('The server {} responds with a status 200'.format(urls))
            else:
                print("The server {} doesn't respond with a status 200".format(urls))
            domain_name = get_domain_name(urls)
            expiration_date = get_domain_expiration_date(domain_name[0])
            checked_domain = check_domain_expiration_date(expiration_date)
            if checked_domain == 0:
                print('The domain {} expires less than a month'.format(urls))
            else:
                print('The domain {} expires more than a month'.format(urls))      
    else:
        print('Incorrect path to file or file name.')
