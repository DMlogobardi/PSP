'use strict';

const haveId = () =>{
    let id= sessionStorage.getItem("userId");
    console.log(id);
    if (id !== null){
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