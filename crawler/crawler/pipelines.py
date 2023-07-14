# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import pandas as pd


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
        """if already exists update movie detail"""
        with open('crawled_link.txt', 'r') as crawled_link:
            for link in crawled_link:
                if link.rstrip('\n') == item['url']:
                    self.__delete_movie(item)
                    self.__new_movie(item, False)
                    return item
        crawled_link.close()

        self.__new_movie(item, True)
        return item

    @staticmethod
    def __delete_movie(item):
        with open('crawled_movie.csv', 'r', newline='') as inp, open('first_edit.csv', 'w+', newline='') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[11] != item['url']:
                    writer.writerow(row)
        inp.close()
        out.close()

        os.remove('crawled_movie.csv')
        os.rename('first_edit.csv', 'crawled_movie.csv')

    @staticmethod
    def __new_movie(item, write_in_txt):
        with open('crawled_movie.csv', 'a', newline='') as csv_file:
            file = csv.writer(csv_file)
            file.writerow(
                [item['Title'], item['USER_SCORE'], item['Runtime'], item['Languages'], item['METASCORE'],
                 item['Genrs'], item['Countries'], item['Writers'],
                 item['PrincipleCast'], item['Cast'], item['Director'], item['url']])
            csv_file.close()

        if write_in_txt:
            with open('crawled_link.txt', 'a', newline='') as link:
                link.write(item['url'] + '\n')
                link.close()
