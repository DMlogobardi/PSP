'use strict';

const loadItems = async (url) => await fetch(url)
    .then(res => res.json())
    .catch(e => console.error(e));



const haveId = () =>{
    let id = sessionStorage.getItem("userId");
    let nick = sessionStorage.getItem("username");
    let ruolo = sessionStorage.getItem("ruolo");
    if(id === null) 
        return;
    if (!noFake(id,nick) && (ruolo === null)) 
        return;
    if (ruolo === "Admin") {
        let navbarNoLog = document.getElementById("divNoLog");
        let navbarLog = document.getElementById("divAdmin");
        navbarNoLog.style.display= "none";
        navbarLog.style.display="block"
    }
    else{
        let navbarNoLog = document.getElementById("divNoLog");
        let navbarLog = document.getElementById("divLog");
        navbarNoLog.style.display= "none";
        navbarLog.style.display="block"
    }    
};


const logout =() => {
    sessionStorage.clear();
    window.location.href = "./login";
}

const  noFake = async(id = null, nick = null ) =>{
    if (id === null || nick === null || id < 1)
        return false;
    else {
        let data = await loadItems(`./api/checkLog/${id}`)
        if (data.hasOwnProperty('nick'))
            if(data.nick === nick){
                return true;
            }
                
    }
    return false
        
}

