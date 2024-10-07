"""
A mushroom expert chatbot that responds to user queries about mushrooms.
"""
import gradio as gr
import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import base64
import PIL.Image
import time
import random

#  Basic configuration
load_dotenv()
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Start a chat session without history
chat = model.start_chat(history=[])

# Function to convert an image to a base64 string
def image_to_base64(image_path):
    with open(image_path, 'rb') as img:
        encoded_string = base64.b64encode(img.read())
    return encoded_string.decode('utf-8')

# Function to create a query message that optionally includes an image
def query_message(txt, img):
    if not img:
        return (txt,None)
    base64_image = image_to_base64(img)
    data_url = f"data:image/jpeg;base64,{base64_image}"
    return f"{txt} ![]({data_url})"

# Function to analyze a mushroom image using the Gemini model
def analyze_mushroom_image(image):
    try:
        # Open the image using PIL
        img = PIL.Image.open(image)
        
        # Prepare the prompt for the Gemini model
        prompt = (
            "You are a world-renowned mycologist. Analyze the following image of a mushroom and provide a JSON response with the following fields common_name, genus, confidence, visible (cap, hymenium, stipe), color, and edible. The image is given")

        # Call the Gemini model to analyze the image
        response = model.generate_content(
            [img, prompt],  # Pass the image directly if your model supports it
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            },
            generation_config=genai.types.GenerationConfig(temperature=0.8),
        )

        # Assuming the response contains a field 'output' with the desired JSON
        mushroom_info = response.text
        print(mushroom_info)
        return  mushroom_info

    except Exception as e:
        print(f"Error analyzing mushroom image: {e}")
        return { }

# Function to handle the chatbot response based on user input and optional image
def llm_response(history, question, img):
    print("question", question)
    response = ""

    # Check if the question mentions Amanita Muscaria or a red mushroom (requirement)
    if "Amanita Muscaria" in question or "red mushroom" in question :
        warning_message = (
                "The Amanita Muscaria contains a neurotoxin that can cause delirium. "
                "It's important to prepare it correctly to avoid adverse effects. "
                "Are you familiar with the proper preparation methods?"
        )
        return warning_message

    if "hello" in question or "hey" in question :
        hello_message = "Hello! How can I help you today? What do you want to know about mushrooms?" 
        return hello_message

    if "bye" in question or "goodbye"  in question :
        bye_message = "Goodbye! Have a great day! Comeback if you have more questions about mushrooms." 
        return bye_message

    if not img:
        print("not image and history is ", history)
        prompt = f"You are a world-renowned mycologist. Provide a detailed response to the following: {question}. Remember to keep the conversation focused on mushrooms and guide the user towards related topics."
        response = chat.send_message(prompt)
        return response
    else:
        mushroom_info = analyze_mushroom_image(img)
        if question:  # If the text is not empty, there was a question
            prompt = (f"You are a world-renowned mycologist. Based on the image of the given mushroom with the following specs : {mushroom_info} please answer the following question: "
                       f"{question}. Remember to keep the conversation focused on mushrooms.")
            response = chat.send_message(prompt)
            return response
        else:
            prompt = (f"You are a world-renowned mycologist. Based on the image of the given mushroom with the following specs : {mushroom_info}. Take this data and make a detailed summary of the mushroom. Remember to keep the conversation focused on mushrooms.")
            response = chat.send_message(prompt)
            return response

# Function to stream the chatbot response character by character with a specific delay
def stream_response(history, question, img, delay=0.01):
    print('inside stream response')
    response = llm_response(history, question, img)
    full_response = response.text
    
    print('full response type', type(full_response))
    streamed_text = ""

    print('history', history)
    print('full response', full_response)
    for char in full_response:
        streamed_text += char
        yield history + [(question, streamed_text)]  
        time.sleep(delay)
    
    history.append((question, response.text))

# Use Gradio to create interface (Blocks) for the mushroom expert chatbot
with gr.Blocks() as demo:
    history = gr.State([])  # This will store the history
    gr.Markdown("<h1 align='center'>🍄 Your Personal Mushroom Expert 🍄</h1>")  # Title

    with gr.Row():
        image_box = gr.Image(type="filepath")  # Upload an image
        chatbot = gr.Chatbot(scale=2, height=550)  # Chatbot interface with history

    # Create a row for Textbox and Submit button to be next to each other
    with gr.Row():
        btn_clear = gr.Button("Clear Chat", scale=1)  # Submit button
        text_box = gr.Textbox(placeholder="Enter text and press enter, or upload an image", container=False, scale=2)
        btn_submit = gr.Button("Submit", scale=1)  # Submit button


    btn_submit.click(stream_response, [history, text_box, image_box], chatbot).then(
        lambda: gr.update(value=""), None, [text_box]  # Clear text input after submission
    )
    btn_clear.click(fn=lambda: ([], gr.update(value="")), outputs=[chatbot, text_box])

 
if __name__ == "__main__":
    demo.launch()


