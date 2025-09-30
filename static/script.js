// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const inputArquivo = document.getElementById('fileInput');
    const nomeArquivo = document.getElementById('file-name');
    const botaoRemoverArquivo = document.getElementById('removeFileBtn');
    const textoEmail = document.getElementById('emailText');

    if (!inputArquivo || !nomeArquivo || !botaoRemoverArquivo || !textoEmail) return;

    inputArquivo.addEventListener('change', () => {
        if (inputArquivo.files.length > 0) {
            nomeArquivo.textContent = inputArquivo.files[0].name;
            botaoRemoverArquivo.style.display = 'inline-block';
            textoEmail.disabled = true;
            textoEmail.style.opacity = '0.6';
        } else {
            redefinirInputArquivo();
        }
    });

    botaoRemoverArquivo.addEventListener('click', () => {
        redefinirInputArquivo();
    });

    function redefinirInputArquivo() {
        inputArquivo.value = '';
        nomeArquivo.textContent = 'Nenhum arquivo selecionado';
        botaoRemoverArquivo.style.display = 'none';
        textoEmail.disabled = false;
        textoEmail.style.opacity = '1';
    }
});
