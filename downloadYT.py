import os
import yt_dlp


def download_video(url, output_path="."):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Use output path for playlist videos
        'format': 'bestvideo+bestaudio/best',  # Download best video and best audio
        'merge_output_format': 'mp4',  # Ensure the output format is mp4
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            file_path = f"{output_path}/{video_title}.mp4"

            # Check if file already exists
            if os.path.exists(file_path):
                print(f"Skipping: {video_title} (Already downloaded)")
            else:
                print(f"Downloading video: {video_title}")
                ydl.download([url])
                print(f"Downloaded: {video_title}")
    except Exception as e:
        print(f"Failed to download video: {e}")


def download_playlist(playlist_url, output_path="."):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            playlist = ydl.extract_info(playlist_url, download=False)
            playlist_title = playlist.get('title', None)

            # Create a folder for the playlist
            if playlist_title:
                playlist_folder = os.path.join(output_path, playlist_title)
                if not os.path.exists(playlist_folder):
                    os.makedirs(playlist_folder)
                print(f"Downloading playlist: {playlist_title}")

                # Loop through each video in the playlist
                for entry in playlist['entries']:
                    if not entry:
                        continue
                    video_url = entry.get('webpage_url', None)  # Get the complete video URL
                    if video_url:
                        download_video(video_url, playlist_folder)  # Pass playlist folder as output path
                print("Playlist download completed!")
            else:
                print("Failed to retrieve playlist title.")
    except Exception as e:
        print(f"Failed to download playlist: {e}")


if __name__ == "__main__":
    url = input("Enter the YouTube video or playlist URL: ").strip()

    # Choose between default and custom output path
    path_choice = input("Do you want to use the default output path './videos' or specify a custom path? (d/c): ").strip().lower()

    if path_choice == 'c':
        folder_name = input("Enter the output folder name: ").strip()
        output_path = os.path.join("./videos", folder_name)
    else:
        output_path = "./videos"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Check if the URL is a playlist or a single video
    if 'playlist' in url:
        download_playlist(url, output_path)
    else:
        download_video(url, output_path)