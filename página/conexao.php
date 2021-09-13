<?php
    function iniciarConexao()
    {
        $servername = "localhost:3306";
        $username = "root";
        $password = "abricó";
        $database = "db_apppromonintendo";

        // Create connection
        $con = new mysqli($servername, $username, $password, $database);

        // Check connection
        if ($con->connect_error) {
        die("Connection failed: " . $con->connect_error);
        }
        return $con;
    }   
?>