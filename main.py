import json
from itertools import islice

import requests
from tqdm import tqdm

input_filename = 'top-1m.csv'
output_filename = 'robot-txt.json'
num_sites = 500


def scrape_csv(file_name):
    with open(file_name) as file_in:
        head = list(islice(file_in, num_sites))

    for line in tqdm(head, total=num_sites):
        site_ranking, site_domain = line.strip().split(',')
        robot_url = 'https://{domain}/robots.txt'.format(domain=site_domain)

        try:
            with requests.get(robot_url, timeout=5) as response:
                robot_text = response.text
                robot_url = response.url
        except requests.exceptions.RequestException as e:
            robot_text = None
            print(e)
        write_json(output_filename, site_ranking, site_domain, robot_url, robot_text)


def write_json(file_name, rank, domain, url, robot_text):
    with open(file_name, 'a') as file_out:
        file_out.write(json.dumps({'rank': rank,
                                   'domain': domain,
                                   'url': url,
                                   'robot_txt': robot_text,
                                   }) + '\n')


def main():
    scrape_csv(input_filename)


if __name__ == '__main__':
    main()
