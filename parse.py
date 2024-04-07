import time
import requests 
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

counter = 1
data = {}
 
def search_vacancies(url,job_request,driver):
    driver.get(url)
    input_form = driver.find_element(By.ID,'search')
    input_form.send_keys(f'{job_request}')
    driver.find_element(By.CLASS_NAME,'js-main-region').click()
    remote_button = driver.find_element(By.CLASS_NAME,'glyphicon-remote')
    driver.execute_script('arguments[0].scrollIntoView(true);',remote_button)
    remote_button.click()
    driver.find_element(By.ID,'sm-but').click()


def get_vacancies_urls(driver):
    vacancies_urls = driver.find_elements(By.CLASS_NAME,'card-hover')
    url_list = []
    for vacancy in vacancies_urls:
        url_list.append(vacancy.find_element(By.CSS_SELECTOR,'a').get_attribute('href'))
    if len(url_list) == 0:
        url_list = False
        return url_list
    
    return url_list    

def get_vacancies_data(url_list,driver):
    global counter
    for url in url_list:
    
        data[f'{counter}'] = get_detail_about_vacancy(url,driver)
        counter += 1
    return data

def get_detail_about_vacancy(url,driver):
    time.sleep(2)
    soup = get_html_of_page(url,driver)
    name = soup.find('h1',{'class':'mt-0 mb-0'}).text
    requirements = list_of_requirements(soup)
    description = soup.find('div',{'id':'job-description'}).text
    job_url = url
    work_data = {
        'name':name,
        'requirements':requirements,
        'description':description,
        'job_url':job_url
    }
    return work_data

    

def get_html_of_page(url,driver):
    driver.get(url)
    html = driver.page_source
    return bs(html,'html.parser')


def list_of_requirements(soup):
    requirements = soup.find_all('span',{'class':'label label-skill label-gray-100 mr-sm mb-xs mt-xs'})
    require_list = []
    if requirements != None:
        for require in requirements:
            require_list.append(require.text)
    return require_list
            

def clear_all_results(driver):
    driver.close()
    driver.quit()
    

def main(job_request):
    driver = Chrome()
    driver.maximize_window()
    url = 'https://www.work.ua/'
    data = {}
    search_vacancies(url,job_request,driver)
    url_list = get_vacancies_urls(driver)

    if url_list == False:
        return False
    if len(url_list) >= 5:
        data = get_vacancies_data(url_list[0:5],driver)
    else:
        data = get_vacancies_data(url_list,driver)
    clear_all_results(driver)
    if len(data) == 0:
        return False
    return data




