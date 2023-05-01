'use strict';

const loadItems = async (url) => await fetch(url)
    .then(res => res.json())
    .catch(e => console.error(e));

const haveId = () =>{
    let id = sessionStorage.getItem("userId");
    let nick = sessionStorage.getItem("username");
    console.log(id);
    if (noFake(id,nick)){
        let navbarNoLog = document.getElementById("divNoLog");
        let navbarLog = document.getElementById("divLog");
        navbarNoLog.style.display= "none";
        navbarLog.style.display="block"
        console.log("LOG GIA FATTO")
    }
};

const logout =() => {
    console.log("logout eseguito");
    sessionStorage.clear();
    window.location.href = "./login";
}

const noFake = (id = null, nick = null ) =>{
    if (id === null || nick === null || id < 1)
        return false;
    else {
        let data = loadItems(`./api/checkLog/${id}`)
        if (data.hasOwnProperty('nick'))
            if(data.nick === nick){
                console.log("Controllo input falsi verificato")
                return true;
            }
                
    }
    return false
        
}