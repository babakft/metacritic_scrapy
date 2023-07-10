# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class SaveData:
    def process_item(self, item, spider):
        """add the crawled link in a file"""
        with open('crawled_link.txt', 'a', newline='') as link:
            link.write(item['url'] + '\n')
            link.close()

        """append data to csv file"""
        with open('crawled_movie.csv', 'a', newline='') as csv_file:
            file = csv.writer(csv_file)
            file.writerow(
                [item['Title'], item['USER_SCORE'], item['Runtime'], item['Languages'], item['METASCORE'],
                 item['Genrs'], item['Countries'], item['Writers'],
                 item['PrincipleCast'], item['Cast'], item['Director'], item['url']])
            csv_file.close()
        return item


class UpdateData:
    def process_item(self, item, spider):
        pass

