<?php     
    function getSelect ($con, $pagina, $login, $row, $rowperpage)
    {
        if ($pagina == 'index')
        {
            if ($rowperpage == 'all')
            {
                $result = mysqli_query($con,"SELECT * from db_nintendo_br"); 
            }
            else
            {
                $result= mysqli_query($con,"SELECT * from db_nintendo_br order by nsuid asc limit $row, $rowperpage");;
            }
        }
        else if ($pagina == 'promo')
        {
            if ($rowperpage == 'all')
            {
                $result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid");
            }
            else
            {
                $result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid order by db_nintendo_br.nsuid asc limit $row, $rowperpage");
            }            
        }
        else
        {
            if ($rowperpage == 'all')
            {
                $result = mysqli_query($con,"SELECT * from db_nintendo_br, user_favs where db_nintendo_br.nsuid = user_favs.FK_nsuid and user_favs.FK_user_id='$login'");
            }
            else
            {
                $result = mysqli_query($con,"SELECT * from db_nintendo_br, user_favs where db_nintendo_br.nsuid = user_favs.FK_nsuid and user_favs.FK_user_id='$login' order by db_nintendo_br.nsuid asc limit $row,$rowperpage");
            }
        }
        return $result;
    } 

    function SiteBuild($pagina)
    {
        include 'conexao.php';         
        $con = iniciarConexao();
        $html = ''; 

        //limite de post por página
        $rowperpage = 42;

        //receber nome de usuário do cookie
        $login = getLogin();

        //recebe a quantidade de jogos da página
        $result = getSelect($con, $pagina, $login, 0, 'all');
        $quantidade=$result->num_rows;
        $html.= "<h4 style='font-size:1.2vw;'> Quantidade de jogos listados: <span id='qtpromo'>$quantidade</span></h4>"; 
        $html.= "<div class='grid-container'>";
                
        $result= getSelect($con, $pagina, $login, 0, $rowperpage);
        
        $i=1;
        while ($row = mysqli_fetch_array($result))        
        {                
            $html.=  "<div class='grid-item' id='div" . $i ."'>";         
            $html.=  "<img class='game-pic' src=" . $row['img_url'] . " alt='game-pic'>";
            $html.=  "<h3><em class='title'>" . $row['titulo'] . "</em></h3>";    
            
            
            if ($pagina=='promo')
            {
                $html.= "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";	
                $html.=  "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row['sale_price'],2,',',' ') . "</span>";
                $html.=  "<p>Promoção válida até " . $row['validade_promo'] . "</p>";
            }
            else
            {
                $offer = mysqli_query($con,"SELECT * from jogos_em_promo where jogos_em_promo.DB_Nintendo_BR_nsuid = '".$row['nsuid']."'");           
                if ($offer->num_rows > 0)
                {
                    $row2 = mysqli_fetch_array($offer);
                    $html.= "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";
                    $html.= "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row2['sale_price'],2,',',' ') . "</span>";
                    $html.= "<p>Promoção válida até " . $row2['validade_promo'] . "</p>";
                }
                else
                {
                    $html.= "<p class='price'>R$ " . number_format($row['msrp'],2,',',' ') . "</p>";
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

            $html.= "<img class='hearts' id='cor". $i ."' alt='favorito' onclick='SalvarFavorito(". $row['nsuid'] ."," . $i . ");' src=$img>";
            $html.= "</div>";
            $i++;             	
        }       
        $html.= "<input type='hidden' id='all' value='$quantidade'>";
        echo $html;
        mysqli_close($con);     
    }  
    
    function getLogin ()
    {
        if (isset($_COOKIE["login"]))
        {
            $login = $_COOKIE["login"]; 
        }
        else
        {
            $login = ''; 
        } 
        return $login;
    }
?>