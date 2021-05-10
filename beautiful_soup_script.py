import requests
from multiprocessing.pool import ThreadPool as Pool
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import colorama
import time
import re

colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

internal_urls = set()
crawling_urls = set()
external_urls = set()
error_urls = set()
total_urls_visited = 0

print_logs = True
headless = True
parProc = True
pool_size = 10

pool = Pool(pool_size)

if headless:
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=opts)


def is_valid(url, domain_name):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and (parsed.netloc == domain_name) and bool(parsed.scheme)


def clean_url(url, query_string=False, path=False):
    final_url = url
    params = urlparse(final_url).params
    query = urlparse(final_url).query
    if query_string and params:
        final_url = final_url.replace(params, "")
    if path and query != "/":
        final_url = final_url.replace(params, "")
    return final_url.rstrip("/")


def unique_urls(urls):
    output_urls = []
    for url in urls:
        url = re.sub(r'\/+$', '', url)
        # Remove hash part in url
        url = url.split('#')[0]
        # Removing query prams in url
        # url = url.split("?")[0]
        # Removes the trailing slash
        if url[len(url) - 1] == "/":
            url = url.split("/")
            url.pop()
            s = "/"
            url = s.join(url)
        url = urljoin(url, urlparse(url).path.replace('//', '/'))
        output_urls.append(url)

    return list(set(output_urls))


def get_all_website_links(url, max_depth):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    urls = set()
    domain_name = urlparse(url).netloc
    base_url = urlparse(url).scheme + "://" + domain_name
    if headless:
        try:
            sada = browser.get(url)
            time.sleep(3)
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
        except Exception as e:
            print(f"{RED}[!] 404 link: {url}{RESET}")
            internal_urls.remove(url)
            error_urls.add(url)
            return urls
        # request = requests.get(url)
        # if request.status_code == 200:
        #     source = browser.page_source
        #     soup = BeautifulSoup(source, 'html.parser')
        # else:
        #     print(f"{RED}[!] 404 link: {url}{RESET}")
        #     internal_urls.remove(url)
        #     error_urls.add(url)
        #     return urls
    else:
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href in crawling_urls:
            continue

        crawling_urls.add(href)

        if href == "" or href is None:
            continue
        # Specific to Titan eye plus project
        if 'https://www.titaneyeplus.com/customer/account/login/referer' in href:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        href = clean_url(href)
        if not is_valid(href, domain_name):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                if print_logs:
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)

            continue
        if print_logs:
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
        if len(urls) >= max_depth and url != base_url:
            break
    return urls


def worker(link, max_homepage_depth, max_urls, max_depth):
    try:
        crawl(link, max_homepage_depth=max_homepage_depth, max_urls=max_urls, max_depth=max_depth)
    except:
        print('error with item')


def crawl(url, max_homepage_depth=10, max_urls=10000, max_depth=10000, home_url=False):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    url = clean_url(url)
    if print_logs:
        print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    depth = max_homepage_depth if (home_url and parProc) else max_depth
    links = get_all_website_links(url, depth)

    links = unique_urls(links)
    for link in links:
        if total_urls_visited > max_urls:
            break
        if parProc and home_url:
            pool.apply_async(worker, (link, max_homepage_depth, max_urls, max_depth,))
        else:
            crawl(link, max_homepage_depth=max_homepage_depth, max_urls=max_urls, max_depth=max_depth)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")

    parser.add_argument("-mu", "--max-urls", help="Number of max URLs to crawl, default is 10000.", default=10000,
                        type=int)

    parser.add_argument("-md", "--max-depth",
                        help="Number of max Depth of the webpage urls to crawl, default is 10000.", default=10000,
                        type=int)

    parser.add_argument("-mhd", "--max-homepage-depth",
                        help="Number of max Depth of the home page to crawl, default is 10000.", default=10000,
                        type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    max_depth = args.max_depth
    max_homepage_depth = args.max_homepage_depth
    start = time.time()

    crawl(url, max_homepage_depth=max_homepage_depth, max_urls=max_urls, max_depth=max_depth, home_url=True)

    pool.close()
    pool.join()

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total Error links:", len(error_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc
    end = time.time()
    print("-------------------------------------------------------------")
    print(f"took -> {end - start} seconds to crawl entire website")
    print("-------------------------------------------------------------")
    with open(f"{domain_name}_links.csv", "w") as f:
        print("Internal URLS", file=f)
        for internal_link in unique_urls(internal_urls):
            print(internal_link.strip(), file=f)
        print("External URLS", file=f)
        for external_link in external_urls:
            print(external_link.strip(), file=f)
        print("Error URLS", file=f)
        for error_link in unique_urls(external_urls):
            print(error_link.strip(), file=f)
