import os
import re
import openai
import urllib.parse
from fpdf import FPDF
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

# Load env vars
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt template
BASE_PROMPT = (
    "Summarize this transcript in {language}, keeping it under 250 words. "
    "Include key points, and provide a chapter-wise breakdown if possible. "
    "Also, return a list of 5-10 important keywords."
)


def extract_video_id(url):

    parsed_url = urllib.parse.urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        query = urllib.parse.parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.lstrip("/")
    else:
        return None


def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            return "Could not extract a valid YouTube video ID.", None
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_list])
        return transcript, transcript_list
    except Exception as e:
        return f"Error fetching transcript: {e}", None


# Ask GPT for summary + keywords
def generate_summary(transcript, language):
    prompt = BASE_PROMPT.format(language=language)
    try:
        # pylint: disable=no-member
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You summarize YouTube video transcripts.",
                },
                {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript}"},
            ],
            temperature=0.7,
            max_tokens=800,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating summary: {e}"


def highlight_keywords(summary, keywords):
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        summary = pattern.sub(f"**{keyword}**", summary)
    return summary


def extract_keywords(summary):
    try:
        # pylint: disable=no-member
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Extract 5-10 important keywords from this text.",
                },
                {"role": "user", "content": summary},
            ],
            temperature=0.3,
            max_tokens=100,
        )
        return re.findall(r"\b\w+\b", response["choices"][0]["message"]["content"])
    except Exception as e:
        return []


# Generate PDF
def create_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    return pdf


# --- Streamlit UI ---
st.set_page_config(page_title="🎥 YouTube Summarizer", layout="centered")
st.title("YouTube Video Summarizer 🎥")

youtube_url = st.text_input("🔗 Enter YouTube Video URL:")
language = st.selectbox(
    "🌍 Choose summary language:", ["English", "Hindi", "Spanish", "French", "German"]
)

if youtube_url:
    with st.spinner("📤 Fetching transcript..."):
        transcript, transcript_data = extract_transcript_details(youtube_url)

    if transcript.startswith("Error"):
        st.error(transcript)
    else:
        with st.spinner("🤖 Generating summary..."):
            summary = generate_summary(transcript, language)

        with st.spinner("🔍 Extracting keywords..."):
            keywords = extract_keywords(summary)
            highlighted_summary = highlight_keywords(summary, keywords)

        st.subheader("📝 Video Summary")
        st.markdown(highlighted_summary)

        st.subheader("🔑 Keywords")
        st.write(", ".join(keywords))

        # Download PDF
        pdf = create_pdf(summary)
        pdf_output_path = "outputs/summary.pdf"
        pdf.output(pdf_output_path)

        with open(pdf_output_path, "rb") as f:
            st.download_button(
                "📥 Download Summary as PDF", f, file_name="youtube_summary.pdf"
            )
