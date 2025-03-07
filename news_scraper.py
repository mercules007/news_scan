import requests
from bs4 import BeautifulSoup
import cloudscraper
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class NewsScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.scraper = cloudscraper.create_scraper()
    
    def get_news_links(self):
        """হোমপেজ থেকে নিউজ লিংক সংগ্রহ করে"""
        response = self.scraper.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        news_links = []
        for link in soup.find_all("a", class_="link"):  # ক্লাস নাম পরিবর্তন করা লাগতে পারে
            news_links.append(self.base_url + link["href"])
        return news_links[:10]  # প্রথম 10 টি লিংক নেবে

    def scrape_news(self, url):
        """নিউজ লিংক থেকে ডাটা সংগ্রহ করে"""
        response = self.scraper.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = soup.find("h1").text.strip() if soup.find("h1") else "শিরোনাম পাওয়া যায়নি"
        date = soup.find("time").text.strip() if soup.find("time") else "তারিখ পাওয়া যায়নি"
        author = soup.find("span", class_="author").text.strip() if soup.find("span", class_="author") else "লেখকের নাম পাওয়া যায়নি"
        paragraphs = soup.find_all("p")
        content = "\n".join([para.text.strip() for para in paragraphs])
        image_tag = soup.find("img")
        image_url = image_tag["src"] if image_tag else "ছবি পাওয়া যায়নি"
        
        return {
            "title": title,
            "date": date,
            "author": author,
            "content": content,
            "image_url": image_url,
            "url": url
        }
    
    def run(self):
        """বট চালানোর মেইন ফাংশন"""
        print("[+] নিউজ লিংক খোঁজা হচ্ছে...")
        news_links = self.get_news_links()
        
        for link in news_links:
            print(f"[+] স্ক্র্যাপ করা হচ্ছে: {link}")
            news_data = self.scrape_news(link)
            print("Title:", news_data["title"])
            print("Release date:", news_data["date"])
            print("author:", news_data["author"])
            print("image:", news_data["image_url"])
            print("content:", news_data["content"][:500], "...")  # ৫০০ ক্যারেক্টার পর্যন্ত দেখাবে
            print("=" * 50)
            time.sleep(2)  # রিকুয়েস্টের মধ্যে বিরতি রাখছে

if __name__ == "__main__":
    bot = NewsScraper("https://www.prothomalo.com")  # এখানে টার্গেট নিউজ সাইটের URL দাও
    bot.run()
