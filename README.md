To run this:
- `pip3 install -r requirements.txt`
-
    ```
    python beautiful_soup_script.py --help
    ```
    **Output:**
    ```
    usage: link_extractor.py [-h] [-m MAX_URLS] url

    Link Extractor Tool with Python

    positional arguments:
    url                   The URL to extract links from.

    optional arguments:
    -h, --help            show this help message and exit
    -mu MAX_URLS,   --max-urls MAX_URLS           Number of max URLs to crawl, default is 10000.
    -md MAX_DEPTH,   --max-depth MAX_DEPTH         Number of max Depth of the webpage urls to crawl, default is 10000.
    ```
- For instance, to extract all links from testjaiin.wordpress.com by scraping only 4 urls from the webpage urls:
    ```
    python beautiful_soup_script.py  https://testjaiin.wordpress.com  -md 4
    ```
    This will result in a large list, here is the last 5 links:
    ```
    [*] Crawling: https://testjaiin.wordpress.com
    [*] Internal link: https://testjaiin.wordpress.com
    [*] Internal link: https://testjaiin.wordpress.com/blog-2
    [*] Internal link: https://testjaiin.wordpress.com/about
    [*] Internal link: https://testjaiin.wordpress.com/contact
    [*] Internal link: https://testjaiin.wordpress.com/team
    [*] Internal link: http://testjaiin.wordpress.com
    [*] Internal link: https://testjaiin.wordpress.com/wp-admin/customize.php
    [*] Crawling: https://testjaiin.wordpress.com/team
    [*] Crawling: https://testjaiin.wordpress.com/wp-admin/customize.php
    [*] Internal link: https://testjaiin.wordpress.com/start
    [*] Internal link: https://testjaiin.wordpress.com/log-in/link
    [*] Crawling: https://testjaiin.wordpress.com/start
    [*] Crawling: https://testjaiin.wordpress.com/log-in/link
    [*] Crawling: https://testjaiin.wordpress.com
    [*] Crawling: http://testjaiin.wordpress.com
    [*] Crawling: https://testjaiin.wordpress.com/about
    [*] Crawling: https://testjaiin.wordpress.com/blog-2
    [*] Internal link: https://testjaiin.wordpress.com/2020/07/01/feedback
    [*] Internal link: https://testjaiin.wordpress.com/author/jayavardhan1234
    [*] Internal link: https://testjaiin.wordpress.com/2020/06/25/getting-things-done
    [*] Internal link: https://testjaiin.wordpress.com/2020/06/24/example-post-3
    [*] Crawling: https://testjaiin.wordpress.com/2020/06/24/example-post-3
    [*] Internal link: https://testjaiin.wordpress.com/category/uncategorized
    [*] Internal link: https://testjaiin.wordpress.com/2020/06/24/example-post-2
    [*] Crawling: https://testjaiin.wordpress.com/category/uncategorized
    [*] Internal link: https://testjaiin.wordpress.com/2020/06/24/example-post
    [*] Crawling: https://testjaiin.wordpress.com/2020/06/24/example-post
    [*] Crawling: https://testjaiin.wordpress.com/2020/06/24/example-post-2
    [*] Crawling: https://testjaiin.wordpress.com/author/jayavardhan1234
    [*] Crawling: https://testjaiin.wordpress.com/2020/06/25/getting-things-done
    [*] Internal link: https://testjaiin.wordpress.com/2020/06/25/tel:9928342147
    [*] Crawling: https://testjaiin.wordpress.com/2020/06/25/tel:9928342147
    [*] Crawling: https://testjaiin.wordpress.com/2020/07/01/feedback
    [*] Crawling: https://testjaiin.wordpress.com/contact
    [*] Internal link: https://testjaiin.wordpress.com/tel:1234567890
    [*] Crawling: https://testjaiin.wordpress.com/tel:1234567890
    [+] Total Internal links: 18
    [+] Total External links: 0
    [+] Total Error links: 0
    [+] Total URLs: 18
    -------------------------------------------------------------
    took -> 183.48366689682007 seconds to crawl entire website
    -------------------------------------------------------------
    ```
    This will also save these URLs in `testjaiin.wordpress.com_links.csv` for both external and internal urls.
