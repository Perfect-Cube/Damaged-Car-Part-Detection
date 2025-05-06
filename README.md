

![car1](https://github.com/user-attachments/assets/e9790aab-cbad-4434-badd-3ce06078c197)
![car2](https://github.com/user-attachments/assets/4dea6260-f1e0-4ca3-a329-f74d36e6c628)
![car3](https://github.com/user-attachments/assets/23c52919-0b78-4598-ba8c-3bf2dbcfebb1)
![car4](https://github.com/user-attachments/assets/e35238cd-f66a-40f2-888d-ea8fb3ef0246)



# Damaged-Car-Part-Detection

-DOWNLOAD OLLAMA THEN CMD
```
ollama run gemma3:4b
```


__1. Starts a web page where you can upload a photo__

The st.file_uploader widget in Streamlit displays a button that lets you pick an image file from your computer. Once you select a file, Streamlit reads it into memory as bytes you can work with in Python 
Streamlit Docs
.

__2. Shows the original car image__

After uploading, the app uses st.image(...) to display the picture right on the page so you can confirm you picked the right photo 
Streamlit Docs
.

__3. Detects damaged areas using a pre-trained model__

Under the hood, it loads a “DETR” object-detection model (a Transformer trained to find objects) via Hugging Face’s pipeline("object-detection"). When you pass the image to this pipeline, it returns a list of boxes, each with coordinates, a label (like “car”), and a confidence score 
Hugging Face
.

__4. Draws red rectangles around suspected damage__

Using Pillow’s ImageDraw, the code takes those box coordinates and draws solid red rectangles around them. It also writes the model’s label and confidence above each box so you know how sure the model is 
GeeksforGeeks
.

__5. Converts the highlighted image to a text string__

To send the image to the local Ollama service, it’s first saved into an in-memory buffer and then encoded into a Base64 string. This turns the binary image data into plain text you can include inside a JSON request 
Stack Overflow
.

__5. Asks Ollama for a damage report__

The app sends an HTTP POST to http://localhost:11434/api/chat, including:

model: which Ollama model to run (e.g. gemma3:4b)

messages: a list of “system” and “user” prompts, where the user prompt has a text question plus the Base64 image in an "images" array.
Ollama returns a JSON response containing a natural-language description of any visible damage 
Stack Overflow
.

__6. Displays the text report, then the annotated image__

Finally, the app writes the text reply from Ollama under “📝 Damage Analysis Report” and shows the same highlighted image below it—so you get both a written assessment and a clear visual indication of where the damage is.

By combining a simple web interface (Streamlit), an off-the-shelf vision model (DETR), and a local LLM service (Ollama), this code gives you a one-click solution: upload a car photo, and immediately see both where it’s damaged and what that damage looks like in words.
