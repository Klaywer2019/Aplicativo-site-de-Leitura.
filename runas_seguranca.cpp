#include <iostream>
#include <string>

// A função agora é inteligente: ela soma 3 pra esconder ou subtrai 3 pra mostrar
std::string processarRuna(std::string texto, char modo) {
    for(int i = 0; i < texto.length(); i++) {
        if (modo == 'c') {
            texto[i] = texto[i] + 3; // Protocolo Selar 🔐
        } else if (modo == 'd') {
            texto[i] = texto[i] - 3; // Protocolo Revelar 🔓
        }
    }
    return texto;
}

int main(int argc, char* argv[]) {
    // Agora o Python manda 2 coisas: o modo ('c' ou 'd') e o texto
    if (argc < 3) {
        std::cout << "Erro: Faltam argumentos rúnicos!";
        return 1;
    }

    char modo = argv[1][0]; // Pega o modo: 'c' (cripto) ou 'd' (descripto)
    std::string mensagem = argv[2]; // Pega o código da obra
    
    // Executa a magia e cospe o resultado pro Python capturar
    std::cout << processarRuna(mensagem, modo);

    return 0;
}
