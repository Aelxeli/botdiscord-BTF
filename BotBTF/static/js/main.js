const socket = io();

function updateRealtime(key, value) {
    socket.emit('update_config', { [key]: value });
    
    // Update preview
    if (key === 'prefix') {
        document.getElementById('preview-prefix').innerText = value;
    }
}

function updateColor(key, hex) {
    // Convert hex to 0x format
    const discordColor = hex.replace('#', '0x');
    document.getElementById(key).value = discordColor;
    socket.emit('update_config', { [key]: discordColor });
    
    // Update preview border
    if (key === 'color_purple') {
        document.getElementById('embed-preview').style.borderLeftColor = hex;
    }
}

function updateKeywords(value) {
    const keywords = value.split(',').map(k => k.trim()).filter(k => k !== "");
    socket.emit('update_config', { 'special_keywords': keywords });
}

socket.on('config_updated', (config) => {
    console.log('Configuração sincronizada:', config);
    // Aqui poderíamos atualizar todos os inputs se necessário
});
