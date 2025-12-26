# 📊 Review Trend Analyzer

An AI-powered system that analyzes Google Play Store reviews to extract trending topics and generate actionable insights for product teams.

## 🎯 Overview

This project processes daily batches of app reviews (Swiggy/Zomato) from June 2024 onwards, using Google Gemini AI and semantic embeddings to identify trending topics, deduplicate similar themes, and generate comprehensive trend reports.[conversation_history:3][conversation_history:7]

## ✨ Features

- **Automated Review Processing**: Scrapes and processes Google Play Store reviews daily
- **AI-Powered Topic Extraction**: Uses Google Gemini 2.5 Flash for intelligent topic identification
- **Smart Deduplication**: Employs sentence transformers and cosine similarity to merge related topics
- **Trend Analysis**: Generates time-series reports showing topic frequency evolution
- **High Recall Design**: Ensures no critical issues are missed in the analysis

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **AI/ML**: Google Gemini API, Sentence Transformers, Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: google-play-scraper
- **Environment**: python-dotenv

## 📁 Project Structure

review-trend-analyzer/
├── data/
│ └── reviews.csv # Review dataset
├── output/
│ └── trend_report.csv # Generated trend reports
├── venv/ # Virtual environment (not tracked)
├── .env # API keys (not tracked)
├── .gitignore
├── config.py # Configuration and API setup
├── scraper.py # Review scraper
├── analyzer.py # Topic extraction and deduplication
├── main.py # Entry point
├── requirements.txt # Dependencies
└── README.md

text

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Setup Steps

1. **Clone the repository**
git clone https://github.com/Tanmay0Bhosale/review-trend-analyzer.git
cd review-trend-analyzer

text

2. **Create virtual environment**
python -m venv venv

text

3. **Activate virtual environment**

Windows:
venv\Scripts\activate

text

Mac/Linux:
source venv/bin/activate

text

4. **Install dependencies**
pip install -r requirements.txt

text

5. **Configure API key**

Create a `.env` file in the project root:
GEMINI_API_KEY=your_api_key_here

text

6. **Add sample data**

Place your `reviews.csv` file in the `data/` folder with columns:
- `reviewId`: Unique identifier
- `userName`: Reviewer name
- `content`: Review text
- `score`: Rating (1-5)
- `thumbsUpCount`: Likes count
- `reviewCreatedVersion`: App version
- `at`: Review timestamp
- `replyContent`: Developer response
- `repliedAt`: Response timestamp

## 💻 Usage

### Basic Usage

Process reviews for a specific date:
python main.py

text

### Custom Date Processing

python main.py --date 2024-06-15

text

### Output

The script generates `output/trend_report.csv` with:
- Topics as rows
- Dates as columns
- Frequency counts showing trend evolution

## 📊 How It Works

1. **Data Loading**: Reads reviews from CSV file
2. **Preprocessing**: Filters reviews by date and prepares text
3. **Topic Extraction**: Uses Gemini AI to extract key topics from each review
4. **Deduplication**: Groups similar topics using semantic similarity (cosine threshold: 0.75)
5. **Trend Generation**: Creates time-series frequency table
6. **Report Output**: Saves CSV report for product team analysis

## 🔧 Configuration

Edit `config.py` to modify:
- `SEED_TOPICS`: Initial topic categories
- `SIMILARITY_THRESHOLD`: Deduplication sensitivity (default: 0.75)
- `GEMINI_MODEL`: AI model version (default: `gemini-2.5-flash`)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Tanmay Bhosale**
- GitHub: [@Tanmay0Bhosale](https://github.com/Tanmay0Bhosale)

## 🙏 Acknowledgments

- Google Gemini API for topic extraction
- Sentence Transformers for semantic similarity
- Google Play Scraper for review data

---

⭐ Star this repository if you find it helpful!