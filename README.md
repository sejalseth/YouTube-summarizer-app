# YouTube-summarizer-app

🎥 YouTube Video Summarizer using OpenAI & Streamlit
This project is a lightweight, AI-powered web app that allows you to summarize YouTube videos instantly using OpenAI's GPT model. Whether you're a student, researcher, or just trying to save time, this tool helps you extract key points from long videos in seconds.

- Features
Summarize any public YouTube video just by pasting its link

Highlight important keywords in the summary

Choose summary language: English, Hindi, Spanish, French, and more

Chapter-wise breakdown based on video structure and timestamps

Download the summary as a PDF for offline use

User-friendly interface built with Streamlit

- How It Works
The app takes a YouTube link as input.

It uses the YouTube Transcript API to fetch subtitles.

The transcript is sent to OpenAI’s GPT-4o model along with a smart prompt.

The model returns a concise, readable summary in the selected language.

The summary is enhanced with highlighted keywords, formatted neatly, and offered for download as a PDF.

- Tech Stack
Python for backend logic

Streamlit for building the UI

OpenAI (GPT-4o) for summarization

youtube-transcript-api for transcript extraction

FPDF for generating PDF reports

python-dotenv for secure key handling

- Getting Started
Clone the repo, install requirements, and run the app locally using:

bash
Copy
Edit
streamlit run app.py
Add your OpenAI key in a .env file like:

ini
Copy
Edit
OPENAI_API_KEY=your-key-here

This project shows how accessible and powerful Generative AI has become, even for beginners. Feel free to explore, contribute, or customize it further.

