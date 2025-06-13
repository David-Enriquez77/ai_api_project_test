import os
import onnxruntime as ort

# Build the path to the ONNX model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "iris.onnx")
MODEL_PATH = os.path.abspath(MODEL_PATH)

# Load the ONNX model using onnxruntime
session = ort.InferenceSession(MODEL_PATH)
