function SalvarFavorito(nsuid,i)
{
    imgid="cor"+i;    
    if (document.getElementById(imgid).src == "https://murosfc.github.io/icones/corvazio.png")
    {
        document.getElementById(imgid).src = "https://murosfc.github.io/icones/corcheio.png";
        EnviaAjax (nsuid,i,'add');        
             
    }
    else
    {
        document.getElementById(imgid).src = "https://murosfc.github.io/icones/corvazio.png"; 
        EnviaAjax (nsuid,i,'remov');                     
    }
}

function EnviaAjax (nsuid,i,tipo)
{
    dados= new FormData();
    dados.append ('nsuid',nsuid);
    dados.append ('user','xlip');
    dados.append ('tipo', tipo);

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

function CriarSite()
{
    $.ajax({
        type: 'POST',
        url: 'sitebuild.php',
        data: {},
        success: function (resposta)
        {
            console.log(resposta);
        }
    })    
}