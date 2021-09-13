function ValidarCadastrar()
    {    
        if (document.getElementById("pass").value == document.getElementById("validasenha").value)
        {
            user=('user',document.getElementById("user").value);
            pass=('pass',document.getElementById("pass").value); 
            cadastrar(user,pass);      
        }
        else 
        {
            alert ("As senha não são iguais\nCorrija e tente novamente.");
        }   

    }

function getCookie(cname) 
    {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
        }
        return "";
    }

function getToken(cname) 
{
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';').splice(1).join(';');    
    if (ca.length > 0) 
    {
        return ca;
    }    
    return "";
}    

function logout()
    {
        document.cookie = "login =;path=/";
        document.location.reload();
    }

function ChecaLogin()
{
    if (getCookie('login') == '')
    {
        document.getElementById('login').innerHTML = "<a href='login.html'>Login</a>";
    }
    else
    {        
        document.getElementById('login').innerHTML = "Logado como: "+ getCookie('login') +"  <a href='javascript:logout()' id='logout'>(logout)</a>"; 
    }
    
}

function SalvarFavorito(nsuid,i)
    {
        imgid="cor"+i;
        login = getCookie('login');
        token = getToken('login');                
        if (login == '')
        {
            alert("Você precisa estar logado para poder salvar favoritos");
        }
        else
        {  
            if (document.getElementById(imgid).src == "https://murosfc.github.io/icones/corvazio.png")
            {
                document.getElementById(imgid).src = "https://murosfc.github.io/icones/corcheio.png";
                EnviaAjax (nsuid,'add', login, token);        
                    
            }
            else
            {
                document.getElementById(imgid).src = "https://murosfc.github.io/icones/corvazio.png"; 
                EnviaAjax (nsuid,'remov', login, token);                     
            }
        }
    }

//add remove favoritos
function EnviaAjax (nsuid,  tipo, login, token)
{
    dados= new FormData();    
    dados.append ('nsuid',nsuid);
    dados.append ('user',login);
    dados.append ('tipo', tipo); 
    dados.append ('token', token); 
    
    $.ajax({
        type: 'POST',
        url: 'addremovfav.php',
        data: dados,
        processData: false,
        contentType: false,
        success: function (resposta)
        {
            console.log(resposta);
        }
    })                    
} 

function FiltraFavoritos()
{
    var itens = parseInt (document.getElementById('qtpromo').textContent);
    var nodes = document.getElementsByClassName('grid-item');  
    var qt_nao_promo = 0;
    if (document.getElementById('favempromo').checked) 
    {
        for (i=0; i < nodes.length; i++)
        {
            node = nodes[i].getElementsByClassName('sale-price');
            if (node.length == 0)
            {                
                nodes[i].style.display = 'none';
                qt_nao_promo +=1 ;                                
            }                             
        }
        document.getElementById('qtpromo').innerHTML = itens - qt_nao_promo;         
    }
    else
    {
        document.getElementById('qtpromo').innerHTML = nodes.length;
        for (i=0; i < nodes.length; i++)
        {
            nodes[i].style.display = ''; 
        } 
    }
} 

//load more
$(document).ready(function()
{

// Load more data
$('.load-more').click(function(){
    var row = Number($('#row').val());
    var allcount = Number($('#all').val());
    var pagina = $('#pagina').val();
    row = row + 42;

    if(row <= allcount){
        $("#row").val(row);
        $('#pagina').val(pagina);

        $.ajax({
            url: 'loadmore.php',
            type: 'post',
            data: {row:row, pagina:pagina},
            beforeSend:function(){
                $(".load-more").text("Loading...");
            },
            success: function(response){

                // Setting little delay while displaying new content
                setTimeout(function() {
                    // appending posts after last post with class="grid-item"
                    $(".grid-item:last").after(response).show().fadeIn("slow");

                    var rowno = row + 3;

                    // checking row value is greater than allcount or not
                    if(rowno > allcount){

                        // Change the text and background
                        $('.load-more').text("Hide");
                        $('.load-more').css("background","darkorchid");
                    }else{
                        $(".load-more").text("Load more");
                    }
                }, 2000);


            }
        });
    }else{
        $('.load-more').text("Loading...");

        // Setting little delay while removing contents
        setTimeout(function() {

            // When row is greater than allcount then remove all class='grid-item' element after 3 element
            $('.grid-item:nth-child(3)').nextAll('.grid-item').remove().fadeIn("slow");

            // Reset the value of row
            $("#row").val(0);

            // Change the text and background
            $('.load-more').text("Load more");
            $('.load-more').css("background","#15a9ce");

        }, 2000);


    }

});
});
function BuscarJogos()
{
    var conteudobusca = document.getElementById('conteudo-busca').value; 
    var pagina = document.getElementById('pagina').value;    
    if (conteudobusca != '')
    {       
        dados= new FormData();
        dados.append('pagina', pagina);
        dados.append('busca', conteudobusca);  
        ApagaBusca();           
        $.ajax({            
            type: 'POST',
            url: 'pesquisar.php',
            data: dados,
            processData: false,
            contentType: false,
            success: function (resposta)
            {
                $("#qtpromo:last").after(resposta).show().fadeIn("slow");
            }
        })    
    } 
    else 
    {
        location.reload();
        return false;
    }   
}

//Apagar elementos que não devem ser exibidos após buscar
function ApagaBusca()
{
    document.querySelectorAll('.grid-container').forEach(e => e.remove()); 
    document.querySelectorAll('#errobusca').forEach(e => e.remove());
    document.querySelectorAll('.load-more').forEach(e => e.remove()); 
    document.querySelectorAll('#row').forEach(e => e.remove());
    document.querySelectorAll('#qtgames').forEach(e => e.remove());     
}

