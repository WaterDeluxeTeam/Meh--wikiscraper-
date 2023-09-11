import json
import wikipediaapi
import time
import os
from tqdm import tqdm

def scrape_wikipedia_category(category_name, output_filename, max_articles=None):
    def get_articles(category, depth):
        if depth > max_depth or (max_articles is not None and len(articles) >= max_articles):
            return

        subcategories = list(category.categorymembers.values())

        for subcategory in subcategories:
            if subcategory.ns == wikipediaapi.Namespace.CATEGORY:
                get_articles(subcategory, depth + 1)
            elif subcategory.ns == wikipediaapi.Namespace.MAIN:
                article_title = subcategory.title

                # Check if the article has already been scraped
                if article_title not in articles:
                    article_start_time = time.time()
                    article_text = subcategory.text if subcategory.text else "No content available."
                    article_end_time = time.time()

                    # Calculate scraping speed in Mbps
                    article_size_bytes = len(article_text.encode('utf-8'))
                    article_speed_mbps = (article_size_bytes * 8) / ((article_end_time - article_start_time) * 1e6)

                    articles[article_title] = {
                        "text": article_text,
                        "speed_mbps": article_speed_mbps
                    }

                    print(f"Scraping: {article_title} ({article_speed_mbps:.2f} Mbps)")

                    # Periodically save the data
                    if len(articles) % save_interval == 0:
                        with open(output_filename, 'w', encoding='utf-8') as file:
                            json.dump(articles, file, ensure_ascii=False, indent=4)

                    pbar.update(1)

                    # Check if the maximum article count has been reached
                    if max_articles is not None and len(articles) >= max_articles:
                        break

    user_agent = "YourUserAgent/1.0"  # Replace with your user agent information
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

    category = wiki_wiki.page(f"Category:{category_name}")

    max_depth = 2  # Adjust the depth as needed
    articles = {}
    save_interval = 10  # Adjust the interval for saving data

    # Create a tqdm instance for progress bar
    pbar = tqdm(total=0, unit="article", position=0, leave=True)

    # Check if the output file already exists
    if os.path.exists(output_filename):
        print(f"Skipping scraping for '{category_name}'. File '{output_filename}' already exists.")
    else:
        get_articles(category, depth=0)

        # Save the final data
        with open(output_filename, 'w', encoding='utf-8') as file:
            json.dump(articles, file, ensure_ascii=False, indent=4)

    # Close the progress bar
    pbar.close()

def main():
    ai_output_filename = 'ai_concepts.json'
    tech_output_filename = 'tech_concepts.json'
    human_evolution_output_filename = 'human_evolution_concepts.json'

    # Define the maximum number of articles to scrape for each category
    max_articles_per_category = {
        "Artificial_intelligence": 1000,  # Adjust as needed
        "Technology": 1000,  # Adjust as needed
        "Human_evolution": 1000  # Adjust as needed
    }

    # Add a list of categories you want to scrape
    categories_to_scrape = [
        ("Artificial_intelligence", ai_output_filename),
        ("Technology", tech_output_filename),
        ("Human_evolution", human_evolution_output_filename)
    ]

    for category_name, output_filename in categories_to_scrape:
        max_articles = max_articles_per_category.get(category_name)
        print(f"Processing category: {category_name}")
        scrape_wikipedia_category(category_name, output_filename, max_articles)
        print(f"{category_name} Wikipedia articles saved to '{output_filename}'.")

if __name__ == "__main__":
    main()
