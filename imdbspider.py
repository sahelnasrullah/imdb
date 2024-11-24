import scrapy
import requests
import json

class BookspiderSpider(scrapy.Spider):
    name = "imdbspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com"]

    def parse(self, response):
        """
        Parse the main IMDb page to extract links for specific sections such as calendar and top charts.
        """
        # Extract links from the navigation menu
        links = response.css("ul.ipc-list.navlinkcat__list.ipc-list--baseAlt a::attr(href)").getall()

        # Iterate through each link to follow and process further
        for link in links:
            full_url = "https://www.imdb.com" + link  # Create full URL

            # Check if the link is related to the calendar section
            if "/calendar/" in full_url:
                yield response.follow(full_url, callback=self.parse_page)
            
            # Check if the link is related to charts or top lists, excluding calendar links
            elif "/chart/" in full_url or "/top/" in full_url:
                if "/calendar/" not in full_url:  # Avoid duplicates
                    yield response.follow(full_url, callback=self.parse_chart_page)

    def parse_page(self, response):
        """
        Parse the calendar page to extract movie names and release dates.
        """
        # Extract list of dates
        list_of_dates = response.css("h3.ipc-title__text::text").getall()

        # Extract list of movie names
        list_of_names = response.css("div.ipc-metadata-list-summary-item__tc a.ipc-metadata-list-summary-item__t::text").getall()

        # Combine names and dates and yield the data
        for movie, date in zip(list_of_names, list_of_dates):
            yield {
                'name': movie,
                'date': date
            }

    def parse_chart_page(self, response):
        """
        Parse the top charts page and extract movie IDs for further processing.
        """
        # Fetch JSON data from the API
        api_data = self.get_json()
        links = []

        # Extract movie IDs from the API response
        for item in api_data["data"]["titles"]:
            link = item.get('id')  # Extract 'id' key
            links.append(link)

        # Construct URLs for each movie and follow them
        url_top = 'https://www.imdb.com/showtimes/title/'
        for l in range(len(links)):
            main_url = url_top + links[l]
            yield response.follow(main_url, callback=self.parse_chart_page2)

    def parse_chart_page2(self, response):
        """
        Parse the individual movie pages to extract detailed information.
        """
        # Extract the movie name
        name = response.css("td.overview-top a::text").get()        

        # Extract the movie description
        description = response.css("div.outline::text").get()

        # Extract the movie rating
        rating = response.css('span.value::text').get() 
        yield {
            'name': name,
            'rating': float(rating) if rating else None,
            'description': description
        }            

    
    def get_json(self):
        url = "https://api.graphql.imdb.com/"

        payload = json.dumps({
        "operationName": "UserRatingsAndWatchOptions",
        "variables": {
            "locale": "sv-SE",
            "idArray": [
            "tt9218128",
            "tt17526714",
            "tt6263850",
            "tt14948432",
            "tt28015403",
            "tt1262426",
            "tt28607951",
            "tt0172495",
            "tt18559464",
            "tt16366836",
            "tt9603208",
            "tt27911000",
            "tt10128846",
            "tt29623480",
            "tt14513804",
            "tt1877830",
            "tt20969586",
            "tt20221436",
            "tt12584954",
            "tt29268110",
            "tt20215234",
            "tt32359447",
            "tt27599851",
            "tt7737800",
            "tt11315808",
            "tt27657135",
            "tt26753003",
            "tt8368368",
            "tt2347285",
            "tt24807110",
            "tt5040012",
            "tt27403986",
            "tt0816692",
            "tt11976134",
            "tt18412256",
            "tt14857528",
            "tt27196021",
            "tt23468450",
            "tt18272208",
            "tt27131358",
            "tt8864596",
            "tt31193791",
            "tt21191806",
            "tt21823606",
            "tt2049403",
            "tt3954936",
            "tt15245240",
            "tt10655524",
            "tt26446278",
            "tt5822536",
            "tt4281724",
            "tt33175825",
            "tt20502488",
            "tt0316768",
            "tt27410895",
            "tt0437086",
            "tt0068646",
            "tt15239678",
            "tt14858658",
            "tt13622970",
            "tt13186482",
            "tt0111161",
            "tt22375054",
            "tt21097228",
            "tt24871974",
            "tt17279496",
            "tt5112584",
            "tt0241527",
            "tt15552142",
            "tt11687002",
            "tt23558280",
            "tt10403420",
            "tt14257582",
            "tt27534307",
            "tt27218960",
            "tt15398776",
            "tt32063050",
            "tt27717667",
            "tt22022452",
            "tt13560574",
            "tt22048412",
            "tt22741760",
            "tt15474916",
            "tt2396431",
            "tt10171472",
            "tt7131622",
            "tt24176060",
            "tt15939198",
            "tt28075881",
            "tt2381941",
            "tt5177120",
            "tt0069947",
            "tt12037194",
            "tt9603212",
            "tt30841606",
            "tt17505010",
            "tt27510174",
            "tt0099785",
            "tt14577874",
            "tt20202324"
            ],
            "includeUserRating": False,
            "location": {
            "latLong": {
                "lat": "59.92",
                "long": "10.75"
            }
            },
            "includeWatchedData": False,
            "fetchOtherUserRating": False
        },
        "extensions": {
            "persistedQuery": {
            "version": 1,
            "sha256Hash": "9672397d6bf156302f8f61e7ede2750222bd2689e65e21cfedc5abd5ca0f4aea"
            }
        }
        })
        headers = {
        'accept': 'application/graphql+json, application/json',
        'accept-language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'session-id=142-9980977-5639800; session-id-time=2082787201l; ad-oo=0; ubid-main=131-7540068-6324335; ci=eyJhY3QiOiJDUUltRDBBUUltRDBBRjRBQkNFTmdTLWdBQUFBQUFBQUFCYW1HNndCMkdvc05UNGF0aHJERFh1R3dZYkR3MlREWmVHMFlicUFBRUFBQUFBIiwiZ2N0IjoiQ1FJbUQwQVFJbUQwQUY0QUJDRU5CQ0ZnQU5MZ0FBQUFBQmFnSG1RUGdBRkFBTkFBeUFCd0FFRUFKQUFsQUJPQUNvQUZvQU1vQWFBQnFBRDBBSVVBUkFCR2dDWUFKd0FVQUFwQUJVQUM3QUdFQVlnQXpBQnVnRGtBT1lBZmdCQUFDRUFFUkFJNEFqd0JOQUNsQUZhQUxnQWFvQThRQi1nRVJBSXRBUndCSFFDVEFFdEFKd0FVMEFySUJYZ0RBZ0dLQU02QWNJQTRnQjFBRDlBSDhBUkFBalVCSG9DalFGaGdMekFYdUF3UUJsZ0R6QUFBZ0FBRkFvQU1BQVFmUUNRQVlBQWctZ09nQXdBQkI5QWxBQmdBQ0Q2QlNBREFBRUgwQXdBR0FBSVBvQ2dBTUFBUWZRR0FBWUFBZy1nUUFBd0FCQjlBUUFQQUJBQUNRQUZRQU5ZQXdnREVBR1lBT1lBZ0FCU2dEVkFKYUFWa0Fyd0J3Z0ZoZ0EuY0FBQUFBQUFBQUEiLCJwdXJwb3NlcyI6WyIxIiwiMiIsIjQiLCI3IiwiOSIsIjEwIiwiMTEiXSwidmVuZG9ycyI6WyI2OCIsIjc3IiwiNzU1IiwiNzkzIiwiODA0IiwiMTEyNiIsIjUwMDI1IiwiNTAwMzAiXX0; uu=eyJpZCI6InV1ZTY0MDcwNjY1NDMxNDkzZWE2NDgiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=; session-token=DzcVs/xCsJWU1Clw0YBGqngU/mRYV+bW5j48Fm0W5VxW4wxlbQ1RRK6Tb1FWy/NlUNIbLSYxMn76MYzjD3QaWV2WoaV/bIhmFOdGohsXEX9W2UgGgXPQOFoids32r54Wny0OF5AgeOHo6OyQLhyePAWYpHntih+O4OrBxDM2Ha6CISrsF/+OdjShRTr8gbUVWyozDJw58ON+j2RKsmD3bMMWwfcXhzew6X8A3ekib0ToJavdWrM+MvCZdB0J1Kij14YMxVcqgl6Wup6mKJUj1dbIOGHrenmNN2Jp8/pc2PUYELamxvU8su2zHSh7FUwGb64xqsSyp5nsVCqntYeS+mOA+P+k/TM8',
        'origin': 'https://www.imdb.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.imdb.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-amzn-sessionid': '142-9980977-5639800',
        'x-imdb-client-name': 'imdb-web-next',
        'x-imdb-client-rid': 'WYRK7MESFG9XB1Q1ET9A',
        'x-imdb-user-country': 'SE',
        'x-imdb-user-language': 'sv-SE',
        'x-imdb-weblab-treatment-overrides': '{"IMDB_NAV_PRO_FLY_OUT_NOV_PROMO_1087903":"T1"}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

