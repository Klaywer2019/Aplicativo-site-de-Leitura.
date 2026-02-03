#include <iostream>
#include <string>

// Função rúnica de embaralhamento (Criptografia simples para teste)
std::string aplicarRuna(std::string texto) {
    for(int i = 0; i < texto.length(); i++) {
        texto[i] = texto[i] + 3; // Desloca os caracteres (Estilo Cifra de César)
    }
    return texto;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Erro: Nenhuma runa enviada!";
        return 1;
    }

    // O Python manda o texto pelo primeiro argumento
    std::string mensagem = argv[1];
    std::string mensagemCriptografada = aplicarRuna(mensagem);

    // O C++ devolve o texto embaralhado para o Python ler
    std::cout << mensagemCriptografada;

    return 0;
}
