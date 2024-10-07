# 🍄 Your Personal Mushroom Expert Chatbot

Welcome to the **Mushroom Expert Chatbot** project! This chatbot leverages the power of the Gemini generative AI model to provide expert knowledge on mushrooms, including identification, edibility, and preparation methods. 


## Features

- **Image Analysis**: Upload images of mushrooms for analysis.
  - **Console Output**: The chatbot prints the JSON response to the console for debugging purposes.
  - **Context Retention**: Remembers the analysis details for future interactions.
  - **Dynamic Responses**: Answers questions related to the uploaded image.
  - **Image Summary**: If no questions are asked, provides a summary based on the image analysis.

- **Mushroom Information**: Access detailed insights about various mushroom species.
- **Interactive Chat Interface**: Engage in a conversational format for asking questions about mushrooms.
- **Safety Warnings**: Receives alerts for potentially toxic mushroom species to ensure user safety.
- **Clear Chat Functionality**: Easily reset the chat for a fresh start.


## Key Functions

- **image_to_base64()**: Converts an image into a base64-encoded string for embedding in the chatbot response.
- **analyze_mushroom_image()**: Analyzes the uploaded mushroom image using the Gemini AI model, providing details.
- **llm_response()**: Generates chatbot responses based on the conversation history, a question, and an optional image.
- **stream_response()**: Streams the chatbot’s response character by character for a more dynamic interaction.

## Installation

To run this project, you need to have Python installed. Follow the steps below to set up the project:

1. Clone this repository:
    ```bash
    git clone  https://github.com/bakalianosm/Mushroom-Expert-Chatbot.git
    cd mushroom-expert-chatbot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables. Create a `.env` file in the project root directory and add your Gemini API key:
    ```plaintext
    API_KEY=your_api_key_here
    ```

## Usage

To run the chatbot, execute the following command in your terminal:
```bash
python MushroomExpert.py
```

This will launch a local server, and you can access the chatbot by navigating to http://localhost:7860 in your web browser.