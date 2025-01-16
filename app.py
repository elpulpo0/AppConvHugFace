import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "interface_gradio"))

from interface_gradio.gradio import conv

if __name__ == "__main__":
    conv.launch()
