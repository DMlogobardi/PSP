'use strict';

const switchDiv = (divAttuale,divNuovo) =>{
	document.getElementById(divAttuale).style.display="none";
	document.getElementById(divNuovo).style.display="block";

}


const showPwd = (input,bottone) => {
	let checkb = document.getElementById(bottone);
	let pwdDiv = document.getElementById(input);
		if (checkb.checked === true) 
		  pwdDiv.type = "text";
		else 
		  pwdDiv.type = "password";
};


const control = async () => {

	let nickname = document.getElementById("nicknameInput").value !== "" ? document.getElementById("nicknameInput").value: null;
	let password = document.getElementById("passwordInput").value !== "" ? CryptoJS.SHA256(document.getElementById("passwordInput").value) : null;
    let passwordConf = document.getElementById("passwordConfirm").value !== "" ? CryptoJS.SHA256(document.getElementById("passwordConfirm").value) : null;
    
    if(nickname === null){
        alert("Nickname vuoto");
        switchDiv('bloccoPass','bloccoNick');
    }
    else if(password === null){
        alert("Password mancante");
    }

    else if(passwordConf === null){
        alert("Seconda password mancante");
    }
    else if(password.value !== passwordConf.value){
        alert("Password diverse");
    }
    else{
        cambioPass(nickname,password)
    }
};



const cambioPass = async (nick="",password="")=>{
    let req =`
    {"passw": "${password}"}`;

    let data = await fetch(`./api/forgotPassword/${nick}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: req
        }
        )
        .then(res => res.json())
        .catch(e => console.error(e));
    if (data=== true){
        alert("Password modificata")
        window.location.href = `./login`
    }
    else{
        alert(data)
    }
}