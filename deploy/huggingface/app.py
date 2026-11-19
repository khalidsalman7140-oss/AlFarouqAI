"""Optional demo template; not deployed or runtime-tested with Gradio in this release."""
import os
import gradio as gr
from alfarouqai import Client,Config
def analyze(text):
    return Client().run('text.analyze',text=text).to_dict()
demo=gr.Interface(fn=analyze,inputs=gr.Textbox(label='Text / النص'),outputs=gr.JSON(),title='AlFarouq AI — Khalid Salman',description='Local text analysis. Original code proprietary; no public reuse grant.')
if __name__=='__main__':demo.launch(server_name='0.0.0.0',server_port=7860,share=False)
