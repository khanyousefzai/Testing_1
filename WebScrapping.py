from selenium import webdriver
import time
import pandas as pd


class WebScrapping:

    def __init__(self, url, number_of_pages):
        print('Project: Getting data from Multiple pages')
        self.url = url
        self.number_of_pages = number_of_pages

    def dataframe_to_csv(self):
        self.creating_dataframe().to_csv('text.csv', encoding='utf-8')

    """---------------Data Extraction and Creation of Dataframe through Helping Function------------"""
    def data_extracting(self):
        dates = []
        text = []
        for y in range(1985, 2012):
            for i in range(1, self.number_of_pages):
                driver = webdriver.Firefox()
                link = f"{self.url}{y}_{i}.html"
                try:
                    driver.get(link)
                    time.sleep(2)
                    date = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div[3]/div[1]/div/div[1]').text
                    date_new = date.split('- ')[1] + '_' + str(i)
                    text_data = driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div[3]/div[2]').text
                    dates.append(date_new)
                    text.append(text_data)
                    time.sleep(1)
                    driver.close()
                except:
                    print('Path did not exist')
                    driver.close()
        return dates, text

    def creating_dataframe(self):
        date, text = self.data_extracting()
        char_remove = ["\n", "/'"]
        text_final = [i.replace(ch, '') for i in text for ch in char_remove if ch in i]
        dictionary = dict(zip(date, text_final))
        df = pd.DataFrame([dictionary.keys(), dictionary.values()]).T
        df.columns = ['Date', 'Article_Text']
        return df


if __name__ == '__main__':
    # just put the link which is common in every page
    ws = WebScrapping('file:///home/zeus/Downloads/New folder/DMNB_1_', 50)
    ws.dataframe_to_csv()
