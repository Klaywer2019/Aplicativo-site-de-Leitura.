import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class ValidadorReal {

    // Sua lógica antiga agora serve como um "filtro rápido"
    public boolean validarFormato(String usuario) {
        return usuario.equals("keisejemima") || (usuario.contains("@") && usuario.length() > 5);
    }

    public static void main(String[] args) {
        ValidadorReal validador = new ValidadorReal();

        // Agora o Python manda: [0]acao, [1]email, [2]senha
        if (args.length < 2) {
            System.out.println("negado:faltam_dados");
            return;
        }

        String acao = args[0];

        try {
            // Conecta no arquivo do banco que o Python criou
            Connection conn = DriverManager.getConnection("jdbc:sqlite:reino_celeste.db");

            if (acao.equals("login")) {
                String email = args[1];
                String senha = args[2];

                // O Guardião caça o mestre no banco
                String sql = "SELECT nome FROM usuarios WHERE email = ? AND senha = ?";
                PreparedStatement pstmt = conn.prepareStatement(sql);
                pstmt.setString(1, email);
                pstmt.setString(2, senha);
                ResultSet rs = pstmt.executeQuery();

                if (rs.next()) {
                    // Se o SQL achou, o Java grita pro Python o nome do Mestre
                    System.out.println("autorizado:" + rs.getString("nome"));
                } else {
                    System.out.println("negado:usuario_nao_encontrado");
                }
            } else if (acao.equals("autorizar")) {
                // Pra salvar tesouros, ele só checa o formato por enquanto
                String usuario = args[1];
                if (validador.validarFormato(usuario)) {
                    System.out.println("autorizado");
                } else {
                    System.out.println("negado");
                }
            }
            conn.close();
        } catch (Exception e) {
            // Se o driver não estiver lá ou o banco sumir
            System.out.println("erro:sistema_seguranca_offline");
        }
    }
}
