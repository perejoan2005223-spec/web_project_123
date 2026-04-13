from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

from blog.models import Department, Professor, Subject, Prof_Subject, Publication, Professor_Publication


class Command(BaseCommand):
    help = 'Scrapes professor data from the university directory'

    def handle(self, *args, **kwargs):
        url = 'https://grauinformatica.udl.cat/es/pla-formatiu/professorat/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        rows = soup.find_all('tr')
        for row in rows:
            data_elems = row.find_all('td')
            if len(data_elems) >= 4:
                a_tag = data_elems[0].find('a')
                prof_name = a_tag.text.strip()
                relative_url = a_tag['href']
                prof_url = 'https://grauinformatica.udl.cat' + relative_url
                dept_name = data_elems[3].text.strip()

                department_obj, created = Department.objects.get_or_create(name_dept=dept_name)
                prof_obj, created = Professor.objects.get_or_create(department=department_obj, name_prof=prof_name, profile_pic_url="")


                prof_request = requests.get(prof_url)
                prof_soup = BeautifulSoup(prof_request.text, "lxml")
                docencia_table = prof_soup.find('div', class_='zonaDocencia')
                if docencia_table:
                    docencia_rows = docencia_table.find_all('tr')
                    for docencia_row in docencia_rows:
                        docencia_cells = docencia_row.find_all('td')

                        if len(docencia_cells) >= 3:
                            subject_name = docencia_cells[2].text.strip()
                            subject_obj, created = Subject.objects.get_or_create(name_sub=subject_name, description="", credits=6)
                            profsub_obj, created = Prof_Subject.objects.get_or_create(professor=prof_obj,subject=subject_obj, year=2026)
                    #TODO: I've set the credit num = 6 and the year = 2026 to everything by default and must change it soon
                recerca_zone = prof_soup.find('div', class_='zonaRecerca')
                if recerca_zone:
                    recerca_tables = recerca_zone.find_all('table')
                    if len(recerca_tables) >= 3:
                        publication_rows = recerca_tables[2].find_all('tr')
                        for publication_row in publication_rows:
                            publication_cells = publication_row.find_all('td')
                            if len(publication_cells) >= 2:
                                title_pub = publication_cells[0].text.strip()
                                pub_year = publication_cells[1].text.strip()
                                publication_obj, created = Publication.objects.get_or_create(title_pub=title_pub, publish_year=pub_year, url="")
                                profpub_obj, created = Professor_Publication.objects.get_or_create(professor=prof_obj, publication=publication_obj, author_order=0)




        self.stdout.write(self.style.SUCCESS('Successfully scraped professors!'))