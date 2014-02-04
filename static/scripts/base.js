

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function toggleFavorite(id)
{
    if (endsWith(document.getElementById(id).src,'heart.png')){
        document.getElementById(id).src='./static/images/heart-filled.png';
    }else{
        document.getElementById(id).src='./static/images/heart.png';
    }
}

function pickLogo(id)
{
    window.logoId = id;
    document.getElementById('logoPicker').style.display='block';
    document.getElementById('fade').style.display='block';
}

function cancelLogo()
{
    window.logoId = "";
    document.getElementById('logoPicker').style.display='none';
    document.getElementById('fade').style.display='none';
}

function setLogo(logo)
{
    document.getElementById(window.logoId).src="./static/logos/"+logo;
    window.logoId = "";
    document.getElementById('logoPicker').style.display='none';
    document.getElementById('fade').style.display='none';
}
