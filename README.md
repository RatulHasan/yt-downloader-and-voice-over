# Youtube video downloader and AI voice generator

### To run the project, you need to follow the following steps:
1) Clone the repository: Start by cloning the repository to your local machine using the following command:

```bash
  git clone https://github.com/RatulHasan/yt-downloader-and-voice-over.git
```
2) Navigate to the project directory: Once the repository is cloned, navigate to the project directory using the following command:

```bash
cd yt-downloader-and-voice-over
```
Rename the file `.env.example` to `.env`
```bash
mv .env.example .env
```
### ⚠️ Note: The voice generator requires an OpenAI API key to work.
```bash
OPENAI_API_KEY=your_openai_api_key
```
### Setting up a virtual environment and installing dependencies:
To set up the project and install the required dependencies, follow these steps:
1) Set up a virtual environment: Virtual environments help isolate the project's dependencies from your system's Python installation. Open a terminal or command prompt and navigate to the project directory. Then create a new virtual environment by running the following command:

```bash
python3 -m venv venv
```
This command will create a new virtual environment named "venv" in the current directory.

2) Activate the virtual environment: Activate the virtual environment to start using it. The commands to activate the virtual environment vary depending on your operating system:

On Windows:
```bash
venv\Scripts\activate.bat
```
On macOS and Linux:

```bash
source venv/bin/activate
```
3) Install project dependencies: Once the virtual environment is activated, you can install the required packages. Typically, Python projects include a requirements.txt file listing all the dependencies. Run the following command to install the dependencies specified in the file:

```bash
pip3 install -r requirements.txt
```
- If you add any new dependencies to the project, you can update the requirements.txt file using the following command:

```bash
pip3 freeze > requirements.txt
```

### To run the voice generator, you need to follow the following steps:
```bash
python3 ./voice_over.py
```
### To run the youtube video downloader, you need to follow the following steps:
```bash
python3 ./downloadYT.py
```