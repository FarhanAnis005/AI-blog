# YouTube Audio to Blog Converter

This is a Django application that extracts audio from YouTube videos, converts the audio to text, and sends the text to a Large Language Model (LLM) to generate a blog. The generated blog is then saved within the application.

## Features

- Extracts audio from YouTube videos.
- Converts audio to text using Speech-to-Text (STT) models.
- Sends the transcribed text to a Large Language Model (LLM) to generate a blog.
- Saves the generated blog within the application.

## Planned Enhancements

- Transition from closed-source to open-source AI models for Speech-to-Text (STT) and LLM.
- Host open-source models on a temporary server on Kaggle.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/FarhanAnis005/AI-blog.git
    cd AI-blog
    ```

2. **Create and activate a virtual environment**:
    ```bash
    # On Windows
    python -m venv env
    .\env\Scripts\activate

    # On macOS/Linux
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run database migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Start the development server**:
    ```bash
    python manage.py runserver
    ```

6. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

1. **Upload a YouTube video URL**:
    - Navigate to the upload page.
    - Enter the YouTube video URL.

2. **Process the video**:
    - The application will extract the audio from the video.
    - The audio will be converted to text using the STT model.
    - The transcribed text will be sent to the LLM to generate a blog.

3. **View the generated blog**:
    - The generated blog will be saved and can be viewed within the application.

## To-Do List

- [ ] Transition to open-source Speech-to-Text (STT) models.
- [ ] Transition to open-source Large Language Models (LLMs).
- [ ] Set up a temporary server on Kaggle for hosting open-source models.

## Contact

For any questions or suggestions, please reach out to us at [farhananis005@gmail.com](mailto:farhananis005@gmail.com).

