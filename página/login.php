<?php
    include 'conexao.php';
    $login = $_POST['user'];
    $entrar = $_POST['entrar'];
    $senha = md5($_POST['pass']);
    
    if (isset($entrar)) {

        $con = iniciarConexao();
        $result = mysqli_query($con, "SELECT * FROM users WHERE id='$login' AND pass='$senha'") or die("erro ao selecionar");
        if ($result->num_rows <=0 ){
            echo"<script language='javascript' type='text/javascript'>
            alert('Login e/ou senha incorretos');window.location
            .href='login.html';</script>";
            die();
        }else{
            setcookie("login",$login);
            header("Location:index.html");
        }
    }
?>