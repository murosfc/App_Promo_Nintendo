<?php
    include 'sitebuild.php';
    include 'conexao.php';   
    $con = iniciarConexao();  

    $rowperpage = 42; //numeros de post por página
    $rows = $_POST['row']; //último post, valor enviado pela página quando ocorre o click no "carregar mais"
    $pagina = $_POST['pagina'];    
    
    //receber nome de usuário do cookie
    if (isset($_COOKIE["login"]))
    {
        $login = $_COOKIE["login"]; 
    }
    else
    {
        $login = ''; 
    }
    //verifica quantos intes tem no site    
    $itens = getSelect($con, $pagina, $login, 0, 'all');
    $quantidade=$itens->num_rows;  

    $html = '';
    $i=$rows+1;
    //echo "<div class='grid-container'>"; 
    // selecting posts
    $result= getSelect($con, $pagina, $login, $rows, $rowperpage);
    while($row = mysqli_fetch_array($result))
    {
        $html.=  "<div class='grid-item' id='div" . $i ."'>";         
        $html.=  "<img class='game-pic' src=" . $row['img_url'] . " alt='game-pic'>";
        $html.=  "<h3><em class='title'>" . $row['titulo'] . "</em></h3>";    
        
        
        if ($pagina=='promo')
        {
            $html.=  "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";	
            $html.=  "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row['sale_price'],2,',',' ') . "</span>";
            $html.=  "<p>Promoção válida até " . $row['validade_promo'] . "</p>";
        }
        else
        {
            $offer = mysqli_query($con,"SELECT * from jogos_em_promo where jogos_em_promo.DB_Nintendo_BR_nsuid = '".$row['nsuid']."'");           
            if ($offer->num_rows > 0)
            {
                $row2 = mysqli_fetch_array($offer);
                $html.=  "<span class='price'><s>R$ " . number_format($row['msrp'],2,',',' ') . "</s></span>";
                $html.=  "&nbsp;&nbsp;&nbsp;&nbsp;<span class='sale-price'>R$ " . number_format($row2['sale_price'],2,',',' ') . "</span>";
                $html.=  "<p>Promoção válida até " . $row2['validade_promo'] . "</p>";
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

        $html.= "<img class='hearts' id='cor". $i ."' alt='favorito' onclick='SalvarFavorito(". $row['nsuid'] ."," . $i . ");' src=$img>";
        $html.= "</div>";
        $html.="\n";
        $i++;             	
    }            
    //$html.= "</div>";
    $html.= "<input type='hidden' id='all' value='$quantidade'>";  
    echo $html;           
    mysqli_close($con);    
?>