import yt_dlp

def download(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'bin/ffmpeg.exe',  # Update this path to the location of your ffmpeg executable
        'outtmpl': f'{output_path}/song.%(ext)s',  # Specify the output file name and path
    }

    def dwl_vid(video_url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    link_of_the_video = url
    zxt = link_of_the_video.strip()
    dwl_vid(zxt)

if __name__ == '__main__':
    download('https://www.youtube.com/watch?v=PeCujsILwvw&ab_channel=ViniVici', 'music')