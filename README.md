# NEWSCast

A web-based News Discovery and AI Podcast Platform developed using **Python Flask**, **SerpApi**, **Groq**, **Edge TTS**, and **FFmpeg** to search, explore, read, and listen to news efficiently.

---

## 📌 Overview

NEWSCast is designed to simplify the way users discover and consume news by combining news search, topic-based news discovery, related source aggregation, article access, and AI-generated podcasts into a single platform.

The application provides users with a simple workflow for discovering current news, exploring multiple sources, reading original articles, and converting selected news stories into AI-generated podcasts.

The system currently supports:

* **English**
* **Hindi**

NEWSCast is built using a modular service-based architecture. News retrieval, article extraction, source aggregation, AI processing, podcast generation, and translation are handled as separate responsibilities.

The main goal is to create a platform where users can move from:

```text
News Discovery
      ↓
News Exploration
      ↓
Source Comparison
      ↓
Article Reading
      ↓
AI Podcast Generation
      ↓
Listening + Transcript

✨ Features
🌐 Language Selection

Users select their preferred language before entering the main application.

Currently supported:

1. English
2. Hindi

The project is being developed toward a dynamic translation system where English user-facing text can be translated into Hindi automatically instead of maintaining a large manually predefined translation dictionary.

📰 News Search

Users can search for news topics or keywords.

NEWSCast retrieves relevant news using SerpApi / Google News.

Search results can contain:

1. News headline
2. Publisher/source
3. Publication date
4. News snippet
5. Thumbnail
6. Original article link

Example search:

Artificial Intelligence

The application then retrieves relevant news stories related to the search query.

🌍 News Categories

NEWSCast provides quick access to major news categories.

Currently available categories:

1. World
2. India
3. Technology
4. Sports

Selecting a category retrieves relevant current news.

🔎 Related Sources

NEWSCast can search for additional coverage related to a selected news story.

The source system can:

1. Search for related coverage
2. Retrieve multiple publishers
3. Exclude the currently selected article when appropriate
4. Collect related news sources
5. Build a structured source bundle

The source aggregation process is:

Selected News Story
        ↓
Related Source Search
        ↓
Multiple News Sources
        ↓
Source Bundle



📄 Original Article Access

Users can open the original article from the publisher.

NEWSCast is designed as a news discovery and aggregation platform and does not replace the original publisher's article.

The user can continue to the original source whenever they want to read the complete article.


📑 Article Extraction

NEWSCast attempts to retrieve article content from the original publisher.

The article extraction system uses:

1. requests
2. trafilatura

The general process is:

Original Article URL
        ↓
HTTP Request
        ↓
Article Extraction
        ↓
Extracted Article Content

Some publishers may block automated requests or restrict access.

When complete article content cannot be retrieved, NEWSCast can fall back to information that is actually available, such as:

1. Headline
2. Snippet
3. Publisher
4. Metadata

The application does not assume unavailable article content.

🤖 AI Podcast Generation

One of the main features of NEWSCast is converting a selected news story into an AI-generated podcast.

The podcast generation system uses Groq to generate the podcast script from the collected source information.

The complete process is:

News Story
      ↓
Primary Article
      +
Related Sources
      ↓
Source Bundle
      ↓
Groq
      ↓
Podcast Script
      ↓
Speaker Segments
      ↓
Edge TTS
      ↓
Individual Audio Segments
      ↓
FFmpeg
      ↓
Final Podcast Audio


The generated podcast can contain:

1. Multiple speakers
2. News discussion
3. AI-generated dialogue
4. Generated audio
5. Transcript
6. Source list


🎙️ Multiple Podcast Voices

NEWSCast currently supports multiple English and Hindi voices.

English Voices
en-IN-NeerjaNeural
en-IN-PrabhatNeural


Hindi Voices
hi-IN-SwaraNeural
hi-IN-MadhurNeural

Different voices can be assigned to different speakers in the podcast.


📝 Podcast Transcript

After a podcast is generated, NEWSCast displays the generated transcript along with the audio.

This allows users to:

1. Listen to the podcast
2. Read the conversation
3. Follow the discussion without audio
4. Review what was generated



📚 Source-Based AI Generation

The AI podcast is not generated from the topic name alone.

NEWSCast first collects information from the selected news story and related sources.

The AI then receives a structured source bundle.

Primary Article
       +
Related Sources
       ↓
Source Bundle
       ↓
AI Processing
       ↓
Podcast Script

This architecture is intended to keep the generated podcast connected to the retrieved news information.




🔄 Complete Application Workflow

The overall NEWSCast workflow is:

                         NEWSCast
                            │
                            ▼
                   Language Selection
                            │
                            ▼
                        Home Page
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
           Search                      Categories
              │                           │
              ▼                           ▼
        Search Results               Topic Results
              │                           │
              └─────────────┬─────────────┘
                            ▼
                       News Story
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
           Read Article        Generate Podcast
                                       │
                                       ▼
                                Source Collection
                                       │
                                       ▼
                                  Source Bundle
                                       │
                                       ▼
                                      Groq
                                       │
                                       ▼
                                Podcast Script
                                       │
                                       ▼
                                    Edge TTS
                                       │
                                       ▼
                                     FFmpeg
                                       │
                                       ▼
                                Podcast Audio
                                       │
                              ┌────────┴────────┐
                              │                 │
                              ▼                 ▼
                            Audio          Transcript
                                                │
                                                ▼
                                             Sources




🏗️ System Architecture

NEWSCast follows a modular service-based architecture.

                         ┌──────────────────────┐
                         │       NEWSCast       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Flask Application  │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
     ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
     │ News Services │      │  Translation  │      │  AI Services  │
     └───────┬───────┘      │    Service    │      └───────┬───────┘
             │              └───────────────┘              │
             ▼                                             ▼
        ┌─────────┐                                  ┌─────────┐
        │ SerpApi │                                  │  Groq   │
        └────┬────┘                                  └────┬────┘
             │                                            │
             ▼                                            ▼
     ┌───────────────┐                            ┌───────────────┐
     │ News Results  │                            │ Podcast Script│
     └───────┬───────┘                            └───────┬───────┘
             │                                            │
             ▼                                            ▼
     ┌──────────────────┐                         ┌───────────────┐
     │ Article Service  │                         │    Edge TTS   │
     └────────┬─────────┘                         └───────┬───────┘
              │                                          │
              ▼                                          ▼
     ┌──────────────────┐                         ┌───────────────┐
     │ Source Service   │                         │ Audio Segments│
     └────────┬─────────┘                         └───────┬───────┘
              │                                          │
              ▼                                          ▼
     ┌──────────────────────┐                     ┌───────────────┐
     │ Source Bundle Service│                     │    FFmpeg     │
     └──────────┬───────────┘                     └───────┬───────┘
                │                                         │
                └────────────────────┐                    ▼
                                     │              Final Podcast
                                     ▼
                              Source-Grounded AI



🧩 Backend Architecture

The backend is divided into multiple services.

Flask Application
       │
       ├── News Service
       │      └── SerpApi / Google News
       │
       ├── Article Service
       │      └── Requests + Trafilatura
       │
       ├── Source Service
       │      └── Related News Sources
       │
       ├── Source Bundle Service
       │      └── Primary Article + Related Sources
       │
       ├── Translation Service
       │      └── English → Hindi
       │
       ├── AI Service
       │      └── Groq
       │
       └── Podcast Service
              ├── Edge TTS
              └── FFmpeg

This separation allows each part of the system to be modified independently.



🔧 Services
news_service.py

Responsible for retrieving news through SerpApi / Google News.

It handles information such as:

Headlines
Publishers
Dates
Snippets
Thumbnails
Article links
Search queries
News categories
article_service.py

Responsible for retrieving and extracting article content from original publisher pages.

It uses:

requests
trafilatura

If article extraction fails, the service can return available fallback information instead of treating unavailable content as available.

source_service.py

Responsible for searching for related news coverage.

It helps NEWSCast find additional sources related to the selected article.

The service can also filter out the currently selected article and irrelevant results.

source_bundle_service.py

Responsible for combining the primary article and related sources into a structured bundle.

Conceptually:

PRIMARY ARTICLE
       +
RELATED SOURCE 1
       +
RELATED SOURCE 2
       +
RELATED SOURCE 3
       ↓
SOURCE BUNDLE

The resulting bundle is provided to the AI service.

translation_service.py

The planned translation service is responsible for dynamically translating user-facing content.

The project is moving away from a manually maintained translation dictionary.

The intended architecture is:

English UI Text
       ↓
Translation Service
       ↓
Hindi UI Text

This means newly added English interface text can be translated without manually adding another translation entry.

ai_service.py

Responsible for generating podcast scripts using Groq.

The AI receives the source bundle and generates the podcast based on the available information.

The service is designed around source grounding so that the model has the retrieved news information available when generating the podcast.

podcast_service.py

Responsible for converting the generated podcast script into audio.

The service handles:

Podcast script parsing
Speaker identification
Voice selection
Text-to-speech generation
Audio segment creation
Audio combination
Final podcast generation



🌐 Translation Architecture

NEWSCast is being redesigned so that the application does not depend on a manually predefined translation dictionary.

The previous approach would require entries such as:

"Home"        → "होम"
"Search"      → "खोजें"
"Technology"  → "प्रौद्योगिकी"

Every new UI string would then require another manual translation entry.

The intended architecture is:

              English UI Text
                     │
                     ▼
             Translation Service
                     │
                     ▼
                Hindi Text

The translation service should:

Accept English text
Translate it into Hindi
Return translated text
Handle translation failures
Fall back to English when necessary
Avoid requiring every UI string to be manually predefined

The translations/ folder is intended to be removed once the dynamic translation architecture is implemented.

🧠 AI Source Grounding

Source grounding is an important part of the NEWSCast architecture.

Instead of doing:

Topic
 ↓
AI
 ↓
Podcast

NEWSCast uses:

Topic
 ↓
News Search
 ↓
Primary Article
 +
Related Sources
 ↓
Source Bundle
 ↓
AI
 ↓
Podcast

This gives the AI access to the retrieved information before generating the podcast.

If article extraction is unavailable, the application should use the information that is actually available, such as:

Headline
Snippet
Publisher
Metadata

The system should not treat missing article content as if it had successfully retrieved the complete article.



🎙️ Podcast Generation Architecture

The podcast system consists of multiple stages.

Step 1 — Select Story

The user selects a news story.

Step 2 — Collect Sources

NEWSCast retrieves the primary article and related sources.

Step 3 — Build Source Bundle

The collected information is structured into a source bundle.

Step 4 — Generate Script

Groq generates the podcast conversation using the source bundle.

Step 5 — Parse Speakers

The generated script is divided into speaker segments.

Step 6 — Generate Speech

Edge TTS converts each speaker segment into audio.

Step 7 — Combine Audio

FFmpeg combines the generated segments.

Step 8 — Display Podcast

The final page provides:

Audio player
Transcript
Sources

The complete pipeline is:

Selected Story
      ↓
Source Bundle
      ↓
Groq
      ↓
Podcast Script
      ↓
Speaker Parser
      ↓
Edge TTS
      ↓
Audio Segments
      ↓
FFmpeg
      ↓
Final MP3
      ↓
Podcast Page





🛠️ Technologies Used
Technology	                                                  Purpose
Python	                                                      Backend application development
Flask	                                                      Web application framework
HTML	                                                      Web page structure
CSS	                                                          User interface styling
JavaScript	                                                  Frontend interaction
SerpApi	                                                      News search and Google News data
Groq	                                                      AI podcast script generation
Edge TTS	                                                  Text-to-speech generation
FFmpeg	                                                      Audio processing and combining
Requests	                                                  HTTP requests for article retrieval
Trafilatura	                                                  Article content extraction
python-dotenv	                                              Environment variable management






📁 Project Structure

The intended organized project structure is:

NEWSCast/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── services/
│   ├── news_service.py
│   ├── article_service.py
│   ├── source_service.py
│   ├── source_bundle_service.py
│   ├── translation_service.py
│   ├── ai_service.py
│   └── podcast_service.py
│
├── templates/
│   ├── language.html
│   ├── home.html
│   ├── search.html
│   ├── topic.html
│   └── podcast.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
├── audio/
│
└── tests/
    ├── test_news.py
    ├── test_article.py
    ├── test_sources.py
    ├── test_bundle.py
    ├── test_ai.py
    └── test_tts.py

The project is still under active development. Some test files may currently exist in the project root and can be moved into the tests/ directory as part of project cleanup.



🗂️ Frontend Structure

The frontend uses HTML templates, CSS, and JavaScript.

templates/
│
├── language.html
│      └── Language Selection
│
├── home.html
│      └── Main News Dashboard
│
├── search.html
│      └── Search Results
│
├── topic.html
│      └── Selected News Story / Topic
│
└── podcast.html
       └── Generated Podcast

Frontend assets are organized under:

static/
│
├── css/
│   └── style.css
│
├── js/
│   └── script.js
│
└── images/




🔗 Flask Routes

The current application contains routes for the major user flows.

/
│
├── /language
│
├── /set-language
│
├── /home
│
├── /search
│
├── /topic
│
├── /generate-podcast
│
├── /audio/<filename>
│
└── /news-topic/<topic_name>
Main Route Responsibilities
Route	                                                        Purpose
/	                                                            Entry point
/language	                                                    Language selection
/set-language	                                                Store selected language
/home	                                                        Main news dashboard
/search	                                                        Search news
/topic	                                                        Display selected news story
/generate-podcast	                                            Generate podcast
/audio/<filename>	                                            Serve generated audio
/news-topic/<topic_name>	                                    Display category news




⚙️ Installation
1. Clone the repository
git clone https://github.com/Chinmayee-Senapati/NewsCast.git
2. Open the project
cd NewsCast
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment
Windows
venv\Scripts\activate
Linux/macOS
source venv/bin/activate
5. Install dependencies
pip install -r requirements.txt



🔐 Environment Configuration

NEWSCast requires API credentials for external services.

Create a .env file in the project root:

SERPAPI_KEY=your_serpapi_key
GROQ_API_KEY=your_groq_api_key

The .env file should remain private.

Never commit API keys to GitHub.



📄 .env.example

A .env.example file can be used to show the required configuration without exposing real credentials.

Example:

SERPAPI_KEY=your_serpapi_key
GROQ_API_KEY=your_groq_api_key



▶️ Running the Application

After installing the dependencies and configuring the environment variables, start the Flask development server:

python app.py

The application should be available at:

http://127.0.0.1:5000

Open the URL in a browser to use NEWSCast.




🧪 Testing

Individual services can be tested independently.

Current test areas include:

News Retrieval
Article Extraction
Source Search
Source Bundle
AI Generation
Text-to-Speech

Example test files:

test_news.py
test_article.py
test_sources.py
test_bundle.py
test_ai.py
test_tts.py

Python syntax can be checked using:

python -m py_compile .\app.py; Get-ChildItem .\services\*.py | ForEach-Object { python -m py_compile $_.FullName }



📊 Development Status
✅ Completed
Flask application
Language selection
English UI
Hindi support
News search
Google News integration through SerpApi
World news
India news
Technology news
Sports news
Topic pages
News story pages
Original article links
Related source search
Source aggregation
Source bundle generation
Article extraction
Article extraction fallback handling
AI podcast script generation
Groq integration
English podcast generation
Hindi podcast generation
Multiple podcast voices
Edge TTS integration
Audio segment generation
FFmpeg audio combination
Podcast audio playback
Podcast transcript
Podcast source list
GitHub repository

🚧 Currently Being Improved
Dynamic English → Hindi translation
Removal of predefined translation dictionaries
Removal of the legacy translations/ folder
Light UI refinement
CSS cleanup
CSS organization
Test organization
Improved error handling
Improved application architecture
UI/UX refinement




🎯 Project Objectives

The main objectives of NEWSCast are:

Make news discovery easier
Provide a simple news search experience
Allow users to explore news by category
Provide access to original news sources
Aggregate related news coverage
Help users compare information from multiple sources
Convert news stories into AI-generated podcasts
Support multilingual news consumption
Make news accessible through both text and audio
Keep AI-generated content connected to retrieved sources
Maintain a modular and maintainable architecture



💡 Project Philosophy

NEWSCast is being developed around several core principles.

Simplicity

News discovery and consumption should be simple and straightforward.

Source Awareness

AI-generated content should remain connected to the underlying news sources.

Multilingual Access

Users should be able to consume news in their preferred language.

AI Assistance

AI should assist users in consuming news rather than replace the original news sources.

Modularity

Each major responsibility should be separated into its own service.

News Retrieval
      ↓
Article Extraction
      ↓
Source Aggregation
      ↓
Translation
      ↓
AI Processing
      ↓
Podcast Generation

This makes the system easier to maintain and allows individual components to evolve independently.



🔒 Security

NEWSCast uses external APIs that require sensitive credentials.

The following security practices should be followed:

Never commit .env
Never hardcode API keys
Never expose API keys in frontend JavaScript
Never upload API keys to GitHub
Keep credentials on the backend
Validate user input
Handle API failures safely
Avoid exposing internal errors to users
Keep generated files and sensitive data out of version control

The .gitignore file should include:

.env
venv/
__pycache__/
*.pyc
audio/




🔮 Future Improvements
📰 News Features

Potential future improvements include:

More news categories
Trending news
Advanced search
Search filters
Personalized news feeds
Better source comparison
More detailed topic pages
Improved news recommendations



🤖 AI Features

Potential AI improvements include:

AI-generated news summaries
Multi-story podcast episodes
Custom podcast duration
Different podcast formats
More advanced source comparison
AI-generated topic summaries
Personalized podcast styles
Improved source-grounding controls


🌐 Language Features

Potential language improvements include:

Additional Indian languages
Dynamic translation for more languages
Improved translation quality
Language-specific podcast generation
More regional TTS voices



👤 User Features

Potential user features include:

User accounts
Saved stories
Reading history
Search history
Podcast history
Personalized news preferences
Favorite topics
Saved podcasts


📱 Platform Improvements

Potential platform improvements include:

Responsive mobile design
Progressive Web App support
Mobile application
Better accessibility
Improved performance
Caching
Production deployment
Cloud hosting
Better error monitoring



📸 Screenshots

Screenshots of the NEWSCast interface can be added here.

Suggested screenshots include:

Language Selection
Home Page
Search Results
Topic Page
News Story
Related Sources
Podcast Generation
Podcast Player
Podcast Transcript




🧭 User Experience Flow

The intended user experience is:

1. Open NEWSCast
        ↓
2. Select Language
        ↓
3. Enter Home Page
        ↓
4. Search for News
   OR
   Select a News Category
        ↓
5. Explore News Results
        ↓
6. Select a Story
        ↓
7. View Story Information
        ↓
8. Read Original Article
   OR
   Generate Podcast
        ↓
9. Listen to Podcast
        ↓
10. Read Transcript
        ↓
11. View Sources



📦 External Services

NEWSCast currently depends on several external services.

Service	                                    Purpose
SerpApi	                        News search / Google News results
Groq	                          AI podcast script generation
Microsoft Edge TTS	                     Text-to-speech
FFmpeg	                                Audio processing

Because these services are external, API availability, quotas, response formats, and access restrictions may affect application behavior.



⚠️ Limitations

Current limitations may include:

1. Some publishers block automated article extraction.
2. Article content may not always be available.
3. Search results depend on SerpApi.
4. AI generation depends on Groq availability and API limits.
5. Text-to-speech depends on available Edge TTS voices.
6. Generated podcasts depend on the information available from retrieved sources.
7. Translation quality may vary when dynamic translation is introduced.
8. The application is currently intended primarily for development and learning purposes.



🏆 Project Highlights

NEWSCast combines several technologies into one complete workflow:

Flask
  +
SerpApi
  +
Article Extraction
  +
Source Aggregation
  +
Dynamic Translation
  +
Groq
  +
Edge TTS
  +
FFmpeg
  ↓
NEWSCast

The project demonstrates the integration of:

1. Web development
2. API integration
3. News retrieval
4. Web scraping/article extraction
5. Source aggregation
6. AI integration
7. Natural language processing
8. Text-to-speech
9. Audio processing
10. Multilingual application design
11. Modular backend architecture


NEWSCast

Stay informed. Stay ahead.

A news discovery and AI podcast platform built using Python, Flask, SerpApi, Groq, Edge TTS, and FFmpeg.
