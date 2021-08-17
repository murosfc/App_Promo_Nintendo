<?php 

    function getSelect ($con, $pagina)
    {
        if ($pagina == 'index')
        {
            $result = mysqli_query($con,"SELECT * from db_nintendo_br");
        }
        else if ($pagina == 'promo')
        {
            $result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid");
        }
        else
        {
            $result = mysqli_query($con,"SELECT * from db_nintendo_br, user_favs where db_nintendo_br.nsuid = user_favs.FK_nsuid and user_favs.FK_user_id='xlip'");
        }
        return $result;
    } 

    function SiteBuild($pagina)
    {
        include 'conexao.php';   
        $con = iniciarConexao();
        
        $result=getSelect($con, $pagina);         
        $quantidade_promo=$result->num_rows;           
        echo "<h4> Quantidade de jogos em promoção: <mark>$quantidade_promo<mark></h4>";

        echo "<div class='grid-container'>";
        $i=1;
        $result=getSelect($con, $pagina); 
        while ($row = mysqli_fetch_array($result))
        {                
        echo "<div class='grid-item' id='div" . $i ."'>";
        echo "<h3>" . $row['titulo'] . "</h3>";  
        echo "<img class='game-pic' src=" . $row['img_url'] . " alt=" . $row['titulo'] . "></img>";    
                            
        echo "<p>De <s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></p>";	
        echo "<p>Por R$ " . number_format($row['sale_price'],2,',',' ') . "</p>";

        /* Mostrar porcentagem de desconto
        if ($row['msrp'] > 0) {
            echo "<p>Desconto de <b>" . number_format((($row['msrp']-$row['sale_price'])/$row['msrp']*100),0,',',' ') . "%</b></p>";
        } 
        else {
            echo "<br />";
        } 
        */

        echo "<p> Promoção válida até " . $row['validade_promo'] . "</p>";
        
        $isfav= mysqli_query($con,"SELECT * FROM user_favs WHERE ".$row['nsuid']."=FK_nsuid");
        if ($isfav->num_rows == 0)
        {
            $img='https://murosfc.github.io/icones/corvazio.png';
        }
        else
        {
            $img='https://murosfc.github.io/icones/corcheio.png';
        }

        echo "<img id='cor". $i ."' alt='favorito' onclick='SalvarFavorito(". $row['nsuid'] ."," . $i . ");' src=$img></img>";
        echo "</div>";
        $i+=1;             	
        }            
        echo "</div>";           
        mysqli_close($con);
    }
?>       