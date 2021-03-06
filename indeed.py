import requests
from bs4 import BeautifulSoup
JOB = 'python'
LIMIT = 50
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={JOB}&limit={LIMIT}'


def get_last_page():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')

    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company != None:
      company_anchor = company.find("a")
    else:
      company_anchor = "없음"
    if company_anchor is not None:
        company = str(company_anchor)

    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("span", {"class": "location"}).string
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location,"link":f"https://kr.indeed.com/채용보기?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
      print(f"Scrapping indeed page{page + 1}")
      result = requests.get(f"{URL}&start={page*LIMIT}")
      soup = BeautifulSoup(result.text, "html.parser")

      results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
      for result in results:
        job = extract_job(result)
        jobs.append(job)
    print(result.status_code)
    return jobs

    
def get_indeed_jobs():
  last_pages = get_last_page()
  jobs = extract_jobs(last_pages)
  return jobs