
function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function execute($method,$url){ 
    xmlhttp=new XMLHttpRequest(); 
    xmlhttp.open($method,$url,false) 
    xmlhttp.send(null); 
} 

function toggleFavorite(id,chan)
{
    if (endsWith(document.getElementById(id).src,'heart.png')){
        document.getElementById(id).src='./static/images/heart-filled.png';
        execute('PUT', './channels/favorites?channel='+chan);
    }else{
        document.getElementById(id).src='./static/images/heart.png';
        execute('DELETE', './channels/favorites?channel='+chan);
    }
}

function pickLogo(id,chan)
{
    window.logoId = id;
    window.logoChan = chan;
    document.getElementById('logoPicker').style.display='block';
    document.getElementById('fade').style.display='block';
}

function cancelLogo()
{
    window.logoId = "";
    window.logoChan = "";
    document.getElementById('logoPicker').style.display='none';
    document.getElementById('fade').style.display='none';
}

function setLogo(logo)
{
    document.getElementById(window.logoId).src="./static/logos/"+logo;
    execute('PUT', './channels/logo?channel='+window.logoChan+'&logo='+logo);
    window.logoId = "";
    window.logoChan = "";
    document.getElementById('logoPicker').style.display='none';
    document.getElementById('fade').style.display='none';
}

function updateDev(dev,action)
{
    if(action == "add"){
        execute('PUT', './device/'+dev);
        location.reload(true);
    }else if(action == "delete"){
        execute('DELETE', './device/'+dev);
        location.reload(true);
    }else{
        execute('GET', './device/'+dev);
        window.location.href = "http://"+window.location.host;
    }
}
