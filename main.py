import json
from collections import defaultdict
from itertools import islice

import requests
from robotexclusionrulesparser import RobotExclusionRulesParser, _end_of_line_regex
from tqdm import tqdm

input_filename = 'top-1m.csv'
output_filename = 'robot-txt.json'
num_sites = 5000


class RulesParser(RobotExclusionRulesParser):
    def __init__(self, domain, rank, url, robots_txt):
        super().__init__()
        self.domain = domain
        self.rank = rank
        self.url = url

        self.lines = []
        self.comments = []
        self.line_count = 0
        self.missing = False
        self.html = False

        self.parse(robots_txt)

    def parse(self, text):
        if not text:
            self.missing = True
            return
        elif '<html' in text or '<body' in text:
            self.html = True
            return

        super().parse(text)

        self.lines = _end_of_line_regex.sub('\n', text).split('\n')
        for line in self.lines:
            line = line.strip()
            self.line_count += 1
            if line.startswith('#'):
                self.comments.append(line[1:].strip())


def load_robots_txt(filename=output_filename):
    with open(filename, 'r') as f:
        for line in tqdm(f, total=num_sites):
            yield RulesParser(**json.loads(line))


def scrape_csv(file_name):
    with open(file_name) as file_in:
        head = list(islice(file_in, num_sites))

    for line in tqdm(head, total=num_sites):
        site_ranking, site_domain = line.strip().split(',')
        robot_url = 'https://{domain}/robots.txt'.format(domain=site_domain)

        try:
            with requests.get(robot_url, timeout=3) as response:
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
                                   'robots_txt': robot_text,
                                   }) + '\n')


def main():
    scrape_csv(input_filename)

    totals = defaultdict(int)
    for robots_txt in load_robots_txt():
        if robots_txt.missing:
            totals['missing'] += 1
        if robots_txt.html:
            totals['html'] += 1
        if len(robots_txt.sitemaps) > 0:
            totals['sitemaps'] += 1
        totals['all'] += 1

    print(totals)


if __name__ == '__main__':
    main()
