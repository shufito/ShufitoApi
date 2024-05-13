from fastapi import FastAPI
from pydantic import BaseModel
import imgkit
import base64
import tempfile
import base64
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = FastAPI()

@app.get("/")
async def home():
    return "Hello World"

class DataInput(BaseModel):
    canal: str
    hoje: str
    ontem: str
    mes: str
    quantidade: str

@app.post("/generate_image_base64")
async def generate_image_base64(data: list[DataInput]):
    # Transformar o JSON em um DataFrame pandas
    df = pd.DataFrame([item.dict() for item in data])
    
    # Gerar uma tabela a partir do DataFrame
    table_html = df.to_html()
    
    # Criar uma figura e um eixo
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    
    # Plotar a tabela sem bordas
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    
    # Salvar a imagem em uma memória temporária
    temp_file = BytesIO()
    plt.savefig(temp_file, format='png')
    temp_file.seek(0)
    
    # Converter a imagem em base64
    image_base64 = base64.b64encode(temp_file.read()).decode('utf-8')
    
    # Fechar o plot
    plt.close()
    
    return {"image_base64": image_base64, "table_html": table_html}

class HTMLInput(BaseModel):
    content: str

@app.post("/generate_html_base64")
async def generate_html_base64(html_input: HTMLInput):
    # HTML input content
    html_content =  html_input.content
    # Options for HTML to image conversion
    options = {
        'format': 'png'
    }

    # Convert HTML to image
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        imgkit.from_string(html_content, temp_file.name, options=options)
        temp_file.seek(0)
        image_content = temp_file.read()

    # Get base64 content of the image
    base64_image = base64.b64encode(image_content).decode('utf-8')

    return base64_image