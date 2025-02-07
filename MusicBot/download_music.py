import yt_dlp
import os

def download(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/song.%(ext)s',  # Specify the output file name and path
    }

    def dwl_vid(video_url):
        # Ensure the directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output_file = f'{output_path}/song.mp3'
        if os.path.exists(output_file):
            os.remove(output_file)  # Delete the existing file if it exists
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    link_of_the_video = url
    zxt = link_of_the_video.strip()
    dwl_vid(zxt)

if __name__ == '__main__':
    download('https://www.youtube.com/watch?v=PeCujsILwvw&ab_channel=ViniVici', 'music')