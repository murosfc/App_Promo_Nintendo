<?php     
    include 'conexao.php';
    
    $user = $_POST['user'];
    $pass = MD5($_POST['pass']);
    $validasenha = md5($_POST['validasenha']);
    $mail = $_POST['email'];
  
    if ($pass == $validasenha)
    {   
        if($user == '' || $user == null)
        {
            echo"<script language='javascript' type='text/javascript'>
            alert('O campo login deve ser preenchido');window.location.href='
            cadastro.html';</script>";
        }
        else 
        {
            $con = iniciarConexao();
            $result = mysqli_query($con, "SELECT * FROM users WHERE id='$user'");

            if ($result->num_rows == 0)
            {
                $sql = "INSERT INTO users VALUES ('$user', '$pass', '$mail', null)";
                if ($con->query($sql) === TRUE) 
                {
                    echo '<script>alert ("Usuário ' . $user . ' registrado com sucesso");window.location.href="index.html";</script>';
                } 
                else 
                {
                    echo '<script>alert ("Erro! \nFalha ao cadastrar, tente novamente.\nAo persistir o erro contate o admin");window.location.href="cadastro.html";</script>';
                }
            }
            else 
            {
                echo '<script>alert ("Usuário ' . $user . ' já está em uso, tente outro.");window.location.href="cadastro.html";</script>';
            }                 
        }  
    }      
    else
    {
        echo "<script>alert ('Senhas digitadas não conferem');window.location.href='cadastro.html';</script>";
    }
?>