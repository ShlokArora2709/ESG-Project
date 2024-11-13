# ESG Data Scraping and Analysis

This project is designed to automate the process of collecting ESG (Environmental, Social, and Governance) data for various companies. It consists of two main scripts:

1. **`scrapping_script.py`** - A Selenium-based web scraper that collects ESG ratings data for companies from the MSCI website.
2. **`article Scrapping.ipynb`** - An asynchronous Python notebook that searches for online articles related to ESG factors for each company, providing deeper insights into each ESG category.

---

## Files and Their Functions

### 1. `scrapping_script.py`

This Python script uses Selenium with Firefox to navigate the MSCI ESG Ratings platform and retrieve the ESG ratings of companies based on two-letter search terms (e.g., "AA", "AB", ..., "ZZ"). The main steps of this script are:

- **Initialize Selenium WebDriver**: Configures the Firefox browser profile for web automation.
- **Generate Search Terms**: Creates two-letter combinations as search terms to cover a broad range of companies.
- **Scrape Company ESG Ratings**: For each valid search result:
    - Retrieve the company's name and ESG rating.
    - If the company data isn't already in `esg_data.csv`, it is added to prevent duplicate entries.
- **Save Results**: The collected data is stored in `esg_data.csv`, structured with columns for company name and ESG rating.

This script enables us to gather an initial set of ESG rating data from MSCI, focusing on efficient data collection and storage to avoid duplicates.

### 2. `article Scrapping.ipynb`

The notebook collects additional data on ESG-related news articles for each company. Using asynchronous functions, it pulls online articles related to specific ESG factors (Environmental, Social, and Governance) to enrich the data beyond MSCI ratings.

- **ESG Factors Dictionary**: Defines relevant subtopics under each ESG category, like "Carbon footprint" under Environmental, or "Business ethics" under Governance.
- **Fetch Articles Asynchronously**: 
    - Utilizes Google search to find relevant articles on each ESG factor for each company.
    - Filters out content from PDFs and avoids irrelevant text, focusing on extracting readable content.
- **Update DataFrame with Articles**: Adds links and content summaries of articles for each company and ESG category into the DataFrame.

This notebook helps provide a richer narrative for each company's ESG performance by exploring public sentiment and news on each factor.

---

Together, these two scripts provide a comprehensive view of companies' ESG standings: one collects standardized ratings, while the other gathers recent discussions and news articles for a well-rounded analysis.
