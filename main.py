from pytube import YouTube

# Predefined list of URLs
url_list = [
    "https://youtu.be/bsVQL8xl0rc",
    "https://youtu.be/PTIpQbwJLrs"
]

# Loop through each URL and download the corresponding video
for link in url_list:
    link = link.strip()  # Remove any leading/trailing whitespace
    if link:  # Check if the link is not empty
        try:
            # Create a YouTube object
            video = YouTube(link)
            
            # Get the highest resolution stream available
            stream = video.streams.get_highest_resolution()
            
            # Download the video
            stream.download()
            
            print(f"Download completed for: {link}")
        except Exception as e:
            print(f"Failed to download video for: {link}. Error: {e}")
