const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('file');
const fileText = document.getElementById('fileText');

// Previne comportamento padrão de abrir o arquivo no navegador
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Adiciona classe para destaque visual ao arrastar
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

// Remove destaque ao sair ou soltar
['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropArea.classList.add('active');
}

function unhighlight() {
    dropArea.classList.remove('active');
}

// Lida com o arquivo solto
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    // Atribui os arquivos ao input invisível para envio no formulário
    fileInput.files = files; 
    updateFileName(files[0]);
}

// Lida com seleção manual (clique no botão)
fileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        updateFileName(this.files[0]);
    }
});

function updateFileName(file) {
    // Atualiza o texto com o nome do arquivo e um ícone de sucesso
    fileText.innerHTML = `<i class="fa-solid fa-check-circle" style="color: #28a745;"></i> ${file.name}`;
}