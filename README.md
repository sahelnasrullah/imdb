# IMDb Scraping Project

## Purpose and Goals
This project aims to automate the collection of data about:
1. Upcoming movies in a specific region for current and following year.
2. IMDb's Top 250 list, including title, rating, and description.

The collected data can be used to analyze trends in the movie industry, build recommendation systems, or keep track of popular and upcoming films aswell as using it for personal use like building a personal "movie generator". 

## Tools and Technologies
- **Programming Language:** Python
- **Web Scraping Framework:** Scrapy
- **API Testing Tool:** Postman
- **Development Environment:** VSCode

## Key Challenges and Solutions
### 1. Automating URL Discovery
To avoid manually collecting URLs, the process of navigating from the homepage to relevant pages is automated. This saves time and makes the script more robust.

### 2. Handling JavaScript-Driven Content
Websites that load content dynamically (e.g., via user interaction) require a different approach than traditional scraping. This was resolved by:
- Identifying API endpoints using browser developer tools (DevTools).
- Testing API requests in Postman to confirm their functionality.
- Integrating API calls into the Scrapy spider to directly fetch JSON data.

## Limitations and Future Improvements
- **Limitations:**  
  - Region-specific data requires additional configuration to ensure accurate targeting.

- **Future Improvements:**  
  - Extend functionality to scrape other categories, such as genres, TV series or trending movies.
  - Implement scheduled scraping to enable continuous data collection.
  - Export data to a database or integrate with a data visualization tool.

## Example Workflow
1. Start from the homepage and from the menu scrape all the URLs for upcoming movies.
2. Use Scrapy to collect movie data, such as title, rating, and description.
3. Handle dynamic content by integrating API calls, tested and verified in Postman, directly into the spider.

## Example Output in json format
```json
[
  {
    "title": "The Shawshank Redemption",
    "rating": "9.3",
    "description": "Two imprisoned men bond over a number of years..."
  },
  {
    "title": "The Godfather",
    "rating": "9.2",
    "description": "The aging patriarch of an organized crime dynasty..."
  }
]
