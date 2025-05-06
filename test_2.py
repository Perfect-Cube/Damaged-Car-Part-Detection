import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, base64, requests, json
from transformers import pipeline

# Configuration
OLLAMA_HOST  = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:4b"

st.set_page_config(page_title="Car Damage Detector (Ollama + DETR)", layout="wide")
st.title("🚗 Car Damage Detector & Reporter")

def image_to_base64(img: Image.Image, fmt="JPEG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

# 1. Upload
uploaded = st.file_uploader("Upload a car image...", type=["jpg","jpeg","png","webp"])
if not uploaded:
    st.stop()
image = Image.open(uploaded).convert("RGB")
st.subheader("Original Image")
st.image(image, use_container_width=True)

# 2. Detect with DETR
detr = pipeline("object-detection", model="shawnmichael/detr-resnet-50_finetuned_car_detection_v2", device=0)  # :contentReference[oaicite:5]{index=5}
detections = detr(image)

# 3. Annotate
annotated = image.copy()
draw = ImageDraw.Draw(annotated)
font = ImageFont.load_default()
for obj in detections:
    if obj["score"] < 0.55: continue
    x1, y1, x2, y2 = obj["box"].values()
    draw.rectangle([x1, y1, x2, y2], outline="red", width=4)
    draw.text((x1, y1-12), f"{obj['label']} ({obj['score']:.2f})", fill="red", font=font)
st.subheader("Detected Damage Highlighted")
st.image(annotated, use_container_width=True)

# 4. Prepare Ollama payload
b64_img = image_to_base64(image)  # :contentReference[oaicite:6]{index=6}
payload = {
    "model": OLLAMA_MODEL,
    "stream": False,
    "messages": [
        {"role": "system",  "content": "You are a car damage assessment assistant."},
        {
            "role": "user",
            "content": "Analyze this image and describe any visible damage, specifying part, location and severity.",
            "images": [b64_img]
        }
    ]
}

# 5. Call Ollama /api/chat
resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=120)
try:
    resp.raise_for_status()
except requests.exceptions.HTTPError as e:
    st.error(f"Request failed: {e}\nResponse: {resp.text}")
    st.stop()

data = resp.json()
report = data.get("message", {}).get("content", "No reply from Ollama.")  # :contentReference[oaicite:7]{index=7}

# 6. Display
st.subheader("📝 Damage Analysis Report")
st.markdown(report)  # :contentReference[oaicite:8]{index=8}
