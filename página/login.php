<?php
    include 'conexao.php';
    $login = $_POST['user'];
    $entrar = $_POST['entrar'];    
    $senha = md5($_POST['pass']);
    
    if (isset($entrar)) {

        $con = iniciarConexao();
        $result = mysqli_query($con, "SELECT * FROM users WHERE id='$login' AND pass='$senha'") or die("erro ao selecionar"); 
        srand();
        $token = md5(mt_rand()); 
        echo $token;      
        mysqli_query($con, "UPDATE users SET token=$token WHERE id='$login' AND pass='$senha'");
        if ($result->num_rows <=0 ){
            echo"<script language='javascript' type='text/javascript'>
            alert('Login e/ou senha incorretos');window.location
            .href='login.html';</script>";
            die();
        }
        else{
            setcookie("login",$login.";".$token, time()+7200);
            header("Location:index.php");
        }
        mysqli_close($con);
    }
    
?>