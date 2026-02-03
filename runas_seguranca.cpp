#include <iostream>
#include <string>
#include <algorithm> // Para std::reverse

// Função que simula uma criptografia rúnica simples
// Na vida real, usaria algoritmos de criptografia robustos como AES
std::string criptografarRuna(const std::string& textoClaro) {
    std::string textoCifrado = textoClaro;
    std::reverse(textoCifrado.begin(), textoCifrado.end()); // Inverte o texto
    for (char &c : textoCifrado) {
        c += 1; // Desloca cada caractere por 1 (exemplo simples)
    }
    return textoCifrado;
}

// Função que simula a descriptografia
std::string descriptografarRuna(const std::string& textoCifrado) {
    std::string textoClaro = textoCifrado;
    for (char &c : textoClaro) {
        c -= 1; // Desfaz o deslocamento
    }
    std::reverse(textoClaro.begin(), textoClaro.end()); // Inverte de volta
    return textoClaro;
}

int main() {
    std::cout << "--- Oraculo de C++ Ativado ---" << std::endl;
    std::string mensagemSecreta = "Mensagem Secreta do Reino Celeste";
    
    std::string cifrado = criptografarRuna(mensagemSecreta);
    std::cout << "Texto Cifrado: " << cifrado << std::endl;
    
    std::string decifrado = descriptografarRuna(cifrado);
    std::cout << "Texto Decifrado: " << decifrado << std::endl;
    
    return 0;
}
