<!DOCTYPE html>
<html lang="pt-br" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>Promoções Nintendo eshop BR</title>
        <meta name="color-scheme" content="light dark">
        <meta name="theme-color" content="#fff">        
        <link rel="stylesheet" href="estilo.css">
        
        <script src="jquery-3.6.0.min.js" type="text/javascript"></script>
        <script src="scripts.js" type="text/javascript"></script>     
        <link rel="icon" href="favicon.ico"> 
       
    </head>
    
    <body onload="ChecaLogin()">             
            <div id='topo'>
                <h1 style="font-size:1.5vw;">Jogos</h1>              
                <div id='hidden' style="display: none;">1</div>
                <nav>
                    <ul>
                        <li><a href='index.php'>HOME</a></li>
                        <li><a href='promo.html'>PROMOÇÕES</a></li>
                        <li><a href='favoritos.html'>FAVORITOS</a></li>                
                    </ul>
                </nav>              
                <div id='form-search'>
                    <label for="pesquisar">Pesquisar</label>
                    <input type="text" id="conteudo-busca" name="pesquisar">                 
                    <button id="click-pesquisar" onclick="BuscarJogos()"><img src="/icones/lupa-cinza.png"></button>
                </div>                 
                <span class="login" id="login"></span>                                  
            </div>        
            <?php
                include 'sitebuild.php';                   
                sitebuild('index')       
            ?>                        
            </div> <!-- fecha div aberta no sitebuild.php> -->
            <h2 class="load-more">Load More</h2>
            <input type="hidden" id="row" value="0"> 
            <input type="hidden" id="pagina" value="index">
            <input type="hidden" id="qtgames" value="0">                   
    </body>
</html>

