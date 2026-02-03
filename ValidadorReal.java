public class ValidadorReal {
    // Esse é o método que você já criou
    public boolean validarAcesso(String usuario) {
        // Lógica ultra secreta: só a Keise ou quem tem e-mail válido passa
        return usuario.equals("keisejemima") || (usuario.contains("@") && usuario.length() > 5);
    }

    // O método 'main' é o que permite o Python conversar com o Java
    public static void main(String[] args) {
        ValidadorReal validador = new ValidadorReal();

        if (args.length > 0) {
            String usuarioParaValidar = args[0];
            
            if (validador.validarAcesso(usuarioParaValidar)) {
                System.out.println("autorizado"); // O Python vai ler essa palavra
            } else {
                System.out.println("negado");
            }
        } else {
            System.out.println("erro: nenhum usuario informado");
        }
    }
}
