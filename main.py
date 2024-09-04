import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import system_prompt
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_json_res_small(sys_prompt:str, user_prompt:str):
    
    model = "gpt-4o-mini"
    
    # logger.info(f"Generating json response small with model {model}")
    print(f"Generating json response small with model {model}")
    messages = [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
    
    response = client.chat.completions.create(
                # model="gpt-4o-mini-2024-07-18",
                # model="gpt-4o-mini",
                # model = "gpt-4o",
                # model="gpt-3.5-turbo-0125",
                # model="gpt-4-turbo",
                # model = "gpt-4-turbo-preview",
                model=model,
                messages=messages,
                # max_tokens=max_tokens,
                temperature=0,
                response_format={"type": "json_object"}
            )
    
    json_res = json.loads(response.choices[0].message.content)
    return json_res


def get_transcript(audio_file):
    print ("Transcribing audio file")
    audio_file= open(audio_file, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    
    return transcription.text
    # print(transcription.text)
    
def analyze_text(text):
    print ("Analyzing text")
    json_resp = get_json_res_small(system_prompt, text)
    return json_resp
    
# def create_sentiment_pie_chart(sentiment_data):
#     # Extract sentiment distribution data
#     labels = ['Positive', 'Negative', 'Neutral']
#     sizes = [sentiment_data['positive'],
#              sentiment_data['negative'],
#              sentiment_data['neutral']]

#     # Create a pie chart
#     fig, ax = plt.subplots(figsize=(6, 6))
#     ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#4CAF50', '#F44336', '#FFC107'], startangle=140)
#     ax.set_title('Sentiment Distribution')
    
#     return fig


def create_advanced_sentiment_pie_chart(sentiment_data):
    # Extract sentiment distribution data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [sentiment_data['positive'],
             sentiment_data['negative'],
             sentiment_data['neutral']]

    # Explode the largest slice
    explode = [0.1 if size == max(sizes) else 0 for size in sizes]

    # Create a pie chart with advanced features
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%', 
           colors=['#4CAF50', '#F44336', '#FFC107'], startangle=140)
    ax.set_title('Sentiment Distribution')
    
    return fig

def create_donut_sentiment_pie_chart(sentiment_data):
    # Extract sentiment distribution data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [sentiment_data['positive'],
             sentiment_data['negative'],
             sentiment_data['neutral']]
    
    # Colors for each segment
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    # Explosion effect for all slices
    explode = (0.05, 0.05, 0.05)
    
    # Create a pie chart with advanced features
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, 
           pctdistance=0.85, explode=explode)
    
    # Draw a circle at the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Ensure that the pie is drawn as a circle
    ax.axis('equal')  
    plt.tight_layout()
    
    return fig

def create_vibrant_donut_sentiment_pie_chart(sentiment_data):
    # Extract sentiment distribution data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [sentiment_data['positive'],
             sentiment_data['negative'],
             sentiment_data['neutral']]
    
    # Vibrant colors for each segment
    colors = ['#FF6F61', '#6B5B95', '#88B04B']  # Brighter and more vibrant colors
    
    # Explosion effect for all slices
    explode = (0.05, 0.05, 0.05)
    
    # Create a pie chart with advanced features
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90, 
           pctdistance=0.85, explode=explode)
    
    # Draw a circle at the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Ensure that the pie is drawn as a circle
    ax.axis('equal')  
    plt.tight_layout()
    
    return fig
    
    
def create_sharp_donut_sentiment_pie_chart(sentiment_data):
    # Extract sentiment distribution data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [sentiment_data['positive'],
             sentiment_data['negative'],
             sentiment_data['neutral']]
    
    # Filter out slices with 0% size
    filtered_data = [(label, size) for label, size in zip(labels, sizes) if size > 0]
    if not filtered_data:
        # Return an empty plot if no data to display
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center',
                fontsize=14, fontweight='bold', color='red')
        ax.axis('off')
        return fig
    
    filtered_labels, filtered_sizes = zip(*filtered_data)
    
    # Colors: Green for Positive, Red for Negative, Yellow for Neutral
    colors = ['#4CAF50', '#F44336', '#FFC107']
    
    # Explosion effect for slices
    explode = (0.1,) * len(filtered_sizes)  # Emphasize each slice
    
    # Create a pie chart with advanced features
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        filtered_sizes, colors=colors, labels=filtered_labels, autopct='%1.1f%%', startangle=90, 
        pctdistance=0.85, explode=explode, shadow=True
    )
    
    # Customize the appearance of the percentage labels
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
    
    # Draw a circle at the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Add a title
    plt.title('Sentiment Distribution', fontsize=12, fontweight='bold')
    
    # Add a legend
    ax.legend(wedges, filtered_labels, title='Sentiments', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Ensure that the pie is drawn as a circle
    ax.axis('equal')
    plt.tight_layout()
    
    return fig


# def create_sharp_donut_sentiment_pie_chart_2(sentiment_data, save_path=None):
#     # Extract sentiment distribution data
#     labels = ['Positive', 'Negative', 'Neutral']
#     sizes = [sentiment_data['positive'],
#              sentiment_data['negative'],
#              sentiment_data['neutral']]
    
#     # Filter out slices with 0% size
#     filtered_data = [(label, size) for label, size in zip(labels, sizes) if size > 0]
#     if not filtered_data:
#         # Return an empty plot if no data to display
#         fig, ax = plt.subplots(figsize=(6, 6))
#         ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center',
#                 fontsize=14, fontweight='bold', color='red')
#         ax.axis('off')
#         if save_path:
#             plt.savefig(save_path, transparent=True)
#         return fig
    
#     filtered_labels, filtered_sizes = zip(*filtered_data)
    
#     # Colors: Green for Positive, Red for Negative, Yellow for Neutral
#     colors = ['#4CAF50', '#F44336', '#FFC107']
    
#     # Explosion effect for slices
#     explode = (0.1,) * len(filtered_sizes)  # Emphasize each slice
    
#     # Create a pie chart with advanced features
#     fig, ax = plt.subplots(figsize=(6, 6))
#     wedges, texts, autotexts = ax.pie(
#         filtered_sizes, colors=colors, labels=filtered_labels, autopct='%1.1f%%', startangle=90, 
#         pctdistance=0.85, explode=explode, shadow=True
#     )
    
#     # Customize the appearance of the percentage labels
#     for autotext in autotexts:
#         autotext.set_color('black')
#         autotext.set_fontsize(10)
    
#     # Draw a circle at the center to create a donut chart
#     centre_circle = plt.Circle((0, 0), 0.70, fc='white')
#     fig.gca().add_artist(centre_circle)
    
#     # Add a title
#     plt.title('Sentiment Distribution', fontsize=12, fontweight='bold')
    
#     # Add a legend
#     ax.legend(wedges, filtered_labels, title='Sentiments', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    
#     # Ensure that the pie is drawn as a circle
#     ax.axis('equal')
#     plt.tight_layout()
    
#     if save_path:
#         plt.savefig(save_path, transparent=True)
    
#     return fig

def main(audio_path):
    
    transcription = get_transcript(audio_path)
    print (f"Transcription: {transcription}\n")
    analysis_report = analyze_text(transcription)
    print (f"Analysis Report: {analysis_report}")
    fig = create_sharp_donut_sentiment_pie_chart(analysis_report['sentiment_distribution'])
    plt.show()
    
    
    
if __name__ == "__main__":
    main("118.wav")
    
