import requests
from bs4 import BeautifulSoup
from newspaper import Article

def extract_content(url):
    try:
        # First, try to use newspaper3k, which is designed for content extraction
        article = Article(url)
        article.download()
        article.parse()
        return article.text  # Returns the main text content of the article

    except Exception as e:
        print("Newspaper3k failed; attempting manual extraction.")
        
        # If newspaper3k fails, use requests and BeautifulSoup
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Custom extraction using common blog post structures
                # Look for common HTML tags or classes used in blog content
                content = ''
                for tag in ['p', 'article', 'div']:
                    paragraphs = soup.find_all(tag)
                    if paragraphs:
                        content += '\n'.join([p.get_text() for p in paragraphs])
                        break
                
                return content.strip()
            else:
                return f"Failed to retrieve the page, status code: {response.status_code}"
                
        except Exception as e:
            return f"Error during manual extraction: {e}"

# Replace 'your_blog_url_here' with the URL you want to scrape
url = "https://medium.com/@fedkiit/how-pepsico-delivers-on-massive-demand-23c86f34f71b"
content = extract_content(url)
print(content)
