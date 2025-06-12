import os
import onnxruntime as ort

# Construye la ruta absoluta al modelo iris.onnx
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "iris.onnx")
MODEL_PATH = os.path.abspath(MODEL_PATH)

# Carga la sesión de inferencia ONNX (se carga solo una vez)
session = ort.InferenceSession(MODEL_PATH)
