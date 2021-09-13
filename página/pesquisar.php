<?php    
    function getSelectBusca ($con, $pagina, $login, $busca)
    {
        if ($pagina == 'index')        
        {        
            
            $result= mysqli_query($con,"SELECT * from db_nintendo_br WHERE titulo LIKE '%$busca%'");            
        }
        else if ($pagina == 'promo')        {
            
            $result = mysqli_query($con,"SELECT * from db_nintendo_br, jogos_em_promo where db_nintendo_br.nsuid = jogos_em_promo.DB_Nintendo_BR_nsuid AND db_nintendo_br.titulo LIKE '%$busca%'");                 
        }
        else
        {           
            $result = mysqli_query($con,"SELECT * from db_nintendo_br, user_favs where db_nintendo_br.nsuid = user_favs.FK_nsuid and user_favs.FK_user_id='$login' and db_nintendo_br.titulo LIKE '%$busca%'");
        }
        return $result;
    } 

    include 'conexao.php'; 
    include 'sitebuild.php';        
    $con = iniciarConexao();
    
    $pagina= $_POST['pagina'];
    $busca= $_POST['busca'];  

    $html = '';     

    //receber nome de usuário do cookie
    $login = getLogin();

    //recebe a quantidade de jogos da página
    $result= getSelectBusca($con, $pagina, $login, $busca);        
    $quantidade=$result->num_rows;
    if ($quantidade>0)
    {       
        //$html.= "<h4 style='font-size:1.2vw;'> Quantidade de jogos listados: <span id='qtpromo'>$quantidade</span></h4>"; 
        $html.= "<div class='grid-container'>";
                
        $result= getSelectBusca($con, $pagina, $login, $busca);
        
        $i=1;
        while ($row = mysqli_fetch_array($result))       
        {                
            $html.=  "<div class='grid-item' id='div" . $i ."'>";         
            $html.=  "<img class='game-pic' src=" . $row['img_url'] . " alt='game-pic'></img>";
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
            $isfav= mysqli_query($con,"SELECT * FROM user_favs WHERE FK_nsuid= '".$row['nsuid']."' AND FK_user_id='".$login."'");
            if ($isfav->num_rows == 0)
            {
                $img='https://murosfc.github.io/icones/corvazio.png';
            }
            else
            {
                $img='https://murosfc.github.io/icones/corcheio.png';
            }

            $html.= "<img class='hearts' id='cor". $i ."' alt='favorito' onclick='SalvarFavorito(". $row['nsuid'] ."," . $i . ");' src=$img></img>";
            $html.= "</div>";
            $i++;             	
        }       
        $html.= "<input type='hidden' id='pagina' value='$pagina'>";
        $html.= "<script type='text/javascript'>document.getElementById('qtpromo').textContent = $quantidade;</script>";
    }
    else 
    {
        $html.="<h4 id='errobusca' style='color: red;'><strong>Nenhum resultado encontrado para ao busca de <span>".$busca."</spam></strong></h4>";
    }
    echo $html;
    mysqli_close($con); 
?>