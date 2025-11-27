from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from io import BytesIO
import PyPDF2
import docx
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

app = Flask(__name__)
# Em produção, usar variáveis de ambiente para a chave secreta
app.secret_key = os.environ.get('SECRET_KEY', 'remedio pra asma')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def text_to_binary(text):
    """Converte texto para representação binária."""
    binary_parts = []
    for char in text:
        try:
            binary = format(ord(char), '08b')
            binary_parts.append(binary)
        except Exception:
            continue
            
    return ' '.join(binary_parts)

def extract_text_from_pdf(file_path):
    text = ''
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + '\n'
    except Exception as e:
        raise Exception(f'Erro ao ler PDF: {str(e)}')
    return text

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise Exception(f'Erro ao ler DOCX: {str(e)}')
    return text

def extract_text_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception:
             raise Exception('Falha na codificação do arquivo TXT (tente UTF-8 ou Latin-1)')
    except Exception as e:
        raise Exception(f'Erro ao ler TXT: {str(e)}')
    return text

def create_pdf_with_binary(binary_text, original_filename):
    """Cria PDF usando canvas básico do ReportLab"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, height - inch, f"Fonte: {original_filename}")
    
    font_size = 8
    c.setFont("Courier", font_size)
    
    # Margens e área útil
    margin = 0.75 * inch
    text_width = width - (2 * margin)
    y_position = height - (1.5 * inch)
    line_height = 10
    
    char_width = 0.6 * font_size 
    chars_per_line = int(text_width / char_width)
    
    words = binary_text.split(' ')
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 <= chars_per_line:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            c.drawString(margin, y_position, ' '.join(current_line))
            y_position -= line_height
            
            current_line = [word]
            current_length = len(word) + 1
            
            if y_position < margin:
                c.showPage()
                c.setFont("Courier", font_size)
                y_position = height - margin
    
    if current_line:
        c.drawString(margin, y_position, ' '.join(current_line))
    
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado.', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            
            file_extension = filename.rsplit('.', 1)[1].lower()
            text = ''
            
            if file_extension == 'pdf':
                text = extract_text_from_pdf(filepath)
            elif file_extension == 'docx':
                text = extract_text_from_docx(filepath)
            elif file_extension == 'txt':
                text = extract_text_from_txt(filepath)
            
            if os.path.exists(filepath):
                os.remove(filepath)
            
            if not text or not text.strip():
                flash('Não foi possível extrair texto legível deste arquivo.', 'error')
                return redirect(url_for('index'))
            
            binary_text = text_to_binary(text)
            pdf_buffer = create_pdf_with_binary(binary_text, filename)
            
            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f'binary_{os.path.splitext(filename)[0]}.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            flash(f'Erro no processamento: {str(e)}', 'error')
            return redirect(url_for('index'))
            
    else:
        flash('Tipo de arquivo não suportado. Use PDF, DOCX ou TXT.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)