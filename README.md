# 🔎 Shop the Post

## 🚀 Welcome to Amazon Product Search Web App
This web application helps users discover similar products on Amazon based on social media posts. Paste a social media link, and the app will return the top 5 related products on Amazon, perfect for finding alternatives, gifts, or comparing brands!

## 📜 Features

🔗 Paste Social Media Link: Drop a link to a social media post (e.g., Instagram, Pinterest).

🤖 AI-Powered Product Extraction: Analyzes post images, videos, and descriptions to identify product features.

🛍️ Amazon Search Results: Displays the top 5 Amazon products related to your search, organized by categories like tech, beauty, etc.


## 💻 Installation

1. Clone the Repository

git clone https://github.com/akshatjaiin/hack_amazon/
cd hack_amazon


2. Install Dependencies

pip install -r requirements.txt


3. Run the Server

python3 manage.py runserver


4. Or Use the Deployed Version
Access the app directly at shop-the-post.onrender.com.



## ⚙️ Tech Stack

Backend: Django

Frontend: HTML, CSS

AI Integration: OpenAI

Scraping: BeautifulSoup (bs4)

HTTP Requests: requests


## 🛠️ How It Works

1. Input the Social Media Link
User enters a link to a social media post.


2. Data Extraction
The app scrapes images, videos, and text from the social media link.


3. AI Analysis
AI generates JSON metadata (e.g., color, brand, category).


4. Amazon Search
Metadata is used to search for products on Amazon, displaying the top 5 results by category.



## 🌐 Usage

Paste Link
Input a social media post link to start your search.

View Results
View the top 5 similar products on Amazon.


## 📈 Future Enhancements

📱 Social Media Integration: Direct integration with Instagram, TikTok, and Pinterest.

🔍 Advanced Filters: Filter products by price, rating, etc.

🌎 Multi-Language Support: Support for additional languages.


## 🤝 Contributing

1. Fork the Repository


2. Create a Branch

git checkout -b feature/your-feature-name


3. Make Changes and Commit

git commit -m "Add your message here"


4. Push the Branch

git push origin feature/your-feature-name


5. Create a Pull Request



**Contributions are welcome!**


