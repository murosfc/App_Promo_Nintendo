<?php
    include 'conexao.php';
    
    $con= iniciarConexao();

    $nsuid= $_POST['nsuid'];
    $user = $_POST['user'];
    $tipo = $_POST['tipo'];

    if ($tipo == 'add')
    {
        $sql = "INSERT IGNORE INTO user_favs VALUES ('$nsuid', '$user')";
    }
    else 
    {
        $sql = "DELETE FROM user_favs WHERE FK_nsuid=$nsuid and FK_user_id='$user'";
    }
    
    if ($con->query($sql) === TRUE) 
    {
        echo "New record created/deleted successfully";
    } 
    else 
    {
        echo "Error: " . $sql . "<br>" . $con->error;
    }

    $con->close();      
?>