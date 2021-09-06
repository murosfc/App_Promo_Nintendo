<?php 

    function getSelect ($con, $pagina, $login)
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
            $result = mysqli_query($con,"SELECT * from db_nintendo_br, user_favs where db_nintendo_br.nsuid = user_favs.FK_nsuid and user_favs.FK_user_id='$login'");
        }
        return $result;
    } 

    function SiteBuild($pagina, $lastdiv)
    {
        include 'conexao.php';   
        $con = iniciarConexao();
        
        
        echo "<div class='grid-container'>";        
        $result=getSelect($con, $pagina, $login); 
        //while ($row = mysqli_fetch_array($result))
        for ($i=$lastdiv;$i<$lastdiv+42 && $row = mysqli_fetch_array($result);$i++)
        {                
            echo "<div class='grid-item' id='div" . $i ."'>";         
            echo "<img class='game-pic' src=" . $row['img_url'] . " alt='game-pic'></img>";
            echo "<h3><em class='title'>" . $row['titulo'] . "</em></h3>";    
            
            
            if ($pagina=='promo')
            {
                echo "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";	
                echo "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row['sale_price'],2,',',' ') . "</span>";
                echo "<p> Promoção válida até " . $row['validade_promo'] . "</p>";
            }
            else
            {
                $offer = mysqli_query($con,"SELECT * from jogos_em_promo where jogos_em_promo.DB_Nintendo_BR_nsuid = '".$row['nsuid']."'");           
                if ($offer->num_rows > 0)
                {
                    $row2 = mysqli_fetch_array($offer);
                    echo "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";
                    echo "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row2['sale_price'],2,',',' ') . "</span>";
                    echo "<p> Promoção válida até " . $row2['validade_promo'] . "</p>";
                }
                else
                {
                    echo "<p class='price'>R$ " . number_format($row['msrp'],2,',',' ') . "</p>";
                }
                
            }        

            /* Mostrar porcentagem de desconto
            if ($row['msrp'] > 0) {
                echo "<p>Desconto de <b>" . number_format((($row['msrp']-$row['sale_price'])/$row['msrp']*100),0,',',' ') . "%</b></p>";
            } 
            else {
                echo "<br />";
            } 
            */        
            
            $isfav= mysqli_query($con,"SELECT * FROM user_favs WHERE FK_nsuid= '".$row['nsuid']."' AND FK_user_id='".$login."'");
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
            $i++;             	
        }            
        echo "</div>";  
        echo "<script language='javascript'>document.getElementById('hidden').innerHTML = ".$i."</script>";        
        mysqli_close($con);
    } 
    $pagina = $_POST['page'];
    $lastdiv = $_POST['lastdiv'];
    SiteBuild($pagina, $lastdiv);
?>