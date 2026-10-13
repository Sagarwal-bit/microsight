import os
from pathlib import Path

import streamlit as st
import torch
import torch.nn as nn
from PIL import Image
from torchvision.models import vit_b_16, ViT_B_16_Weights

st.set_page_config(
    page_title="MicroSight | Histopathology AI Prototype",
    page_icon="🔬",
    layout="centered",
)

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "microsight_vit_final.pth"

st.title("🔬 MicroSight")
st.subheader("AI-Assisted Histopathology Image Analysis Prototype")
st.write(
    "Upload a histopathology image to see the prediction from the trained "
    "Vision Transformer (ViT-B/16) prototype."
)

st.warning(
    "Research prototype only. This tool is not a medical device and must not "
    "be used to diagnose, rule out, or make treatment decisions about cancer."
)

@st.cache_resource(show_spinner="Loading the trained ViT model…")
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at: {MODEL_PATH}. "
            "Check that models/microsight_vit_final.pth exists in the repository."
        )

    # Git LFS pointer files are small text files, not the actual model weights.
    with open(MODEL_PATH, "rb") as f:
        header = f.read(200)
    if b"git-lfs.github.com/spec/v1" in header:
        raise RuntimeError(
            "The model path contains a Git LFS pointer, not the actual model. "
            "Ensure the hosting environment downloads Git LFS objects, or host "
            "the .pth file on an accessible model-storage service."
        )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )

    if not isinstance(checkpoint, dict) or "model_state_dict" not in checkpoint:
        raise RuntimeError(
            "Unexpected checkpoint format. Expected a dictionary containing "
            "'model_state_dict', as saved by the Kaggle notebook."
        )

    model = vit_b_16(weights=None)
    model.heads.head = nn.Linear(model.heads.head.in_features, 2)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    # Matches the notebook's ViT_B_16_Weights.DEFAULT preprocessing.
    transform = ViT_B_16_Weights.DEFAULT.transforms()
    class_names = checkpoint.get("class_names", {0: "Class 0", 1: "Class 1"})
    class_names = {int(k): str(v) for k, v in class_names.items()}

    return model, transform, class_names, checkpoint


try:
    model, transform, class_names, checkpoint = load_model()
    st.success("Trained ViT-B/16 model loaded.")
    if "test_accuracy" in checkpoint:
        st.caption(
            f"Notebook-reported test accuracy: {float(checkpoint['test_accuracy']):.2f}% "
            "(evaluation metric; not a guarantee for an individual image)"
        )
except Exception as exc:
    st.error("The model could not be loaded.")
    st.code(str(exc))
    st.info(
        "Check that the model file is present and that Git LFS delivered the "
        "actual .pth file. If the file is a Git LFS pointer, the app cannot infer."
    )
    st.stop()

uploaded = st.file_uploader(
    "Upload a histopathology image",
    type=["png", "jpg", "jpeg", "tif", "tiff", "bmp"],
    help="For this prototype, use an image similar to the image patches used in training.",
)

if uploaded is not None:
    try:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded image", use_container_width=True)

        if st.button("Analyze image", type="primary", use_container_width=True):
            with st.spinner("Running inference…"):
                tensor = transform(image).unsqueeze(0)
                with torch.inference_mode():
                    logits = model(tensor)
                    probabilities = torch.softmax(logits, dim=1)[0]
                    predicted_idx = int(torch.argmax(probabilities).item())
                    confidence = float(probabilities[predicted_idx].item()) * 100

            predicted_label = class_names.get(predicted_idx, f"Class {predicted_idx}")
            st.subheader("Prediction")
            st.metric("Predicted class", predicted_label, f"{confidence:.2f}% confidence")
            st.write("Class scores")
            score_data = {
                class_names.get(i, f"Class {i}"): float(probabilities[i].item())
                for i in range(len(probabilities))
            }
            st.bar_chart(score_data, y_label="Probability")
            st.caption(
                "Confidence is the model's softmax score, not a calibrated probability "
                "of disease. Results can be wrong and require expert review."
            )
    except Exception as exc:
        st.error(f"Could not process this image: {exc}")

st.divider()
st.caption("MicroSight — AI-Assisted Histopathology Image Analysis Prototype")
