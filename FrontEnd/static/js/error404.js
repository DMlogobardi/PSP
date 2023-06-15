const bottoniCard = () =>{
    let id = sessionStorage.getItem("userId");
    let nick = sessionStorage.getItem("username");
    let ruolo = sessionStorage.getItem("ruolo");
    console.log(id);
    if(id === null) 
        return;
    if (!noFake(id,nick) && (ruolo === null)) 
        return;
    if (ruolo === "Admin") {
        document.getElementById("bottoni").style.display= "none";;
        let cardbarLog = document.getElementById("bottoniAdmin");
        
        cardbarLog.style.display="block";
        console.log("Admin LOGGATO")
    }
    else{
        let cardNoLog = document.getElementById("bottoni");
        let cardbarLog = document.getElementById("bottoniUser");
        cardNoLog.style.display= "none";
        cardbarLog.style.display="block"
        console.log("LOG GIA FATTO")
    }    
};
window.setTimeout("bottoniCard()", 200);

const changeWin = async (url) =>window.location.href = `${url}`;
