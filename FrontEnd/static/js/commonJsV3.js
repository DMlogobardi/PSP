'use strict';

const loadItems = async (url) => await fetch(url)
    .then(res => res.json())
    .catch(e => console.error(e));



const haveId = () =>{
    let id = sessionStorage.getItem("userId");
    let nick = sessionStorage.getItem("username");
    let ruolo = sessionStorage.getItem("ruolo");
    console.log(id);
    if(id === null) 
        return;
    if (!noFake(id,nick) && (ruolo === null)) 
        return;
    if (ruolo === "Admin") {
        let navbarNoLog = document.getElementById("divNoLog");
        let navbarLog = document.getElementById("divAdmin");
        navbarNoLog.style.display= "none";
        navbarLog.style.display="block"
        console.log("Admin LOGGATO")
    }
    else{
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

const  noFake = async(id = null, nick = null ) =>{
    if (id === null || nick === null || id < 1)
        return false;
    else {
        let data = await loadItems(`./api/checkLog/${id}`)
        console.log(data)
        if (data.hasOwnProperty('nick'))
            if(data.nick === nick){
                console.log("Controllo input falsi verificato")
                return true;
            }
                
    }
    return false
        
}

