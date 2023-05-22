'use strict';

// print items on Html page
const control = async () => {
	let nickname= document.getElementById("nicknameInput").value;
	let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
	console.log(`nick= ${nickname}, password=${password}`);
	verify(nickname,password);
};


const verify = async (nickname,password) => {
	const data = await fetch(`./api/log/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify( {
					"nick": `${nickname}`,
					"p_ass" : `${password.toString()}`
				}
			)
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	let result = data; 
	console.log(result)
	if (result.hasOwnProperty('userId')){
		sessionStorage.setItem("userId",result.userId);
		sessionStorage.setItem("username",result.nick);
		sessionStorage.setItem("ruolo",result.ruolo);
		if (result.ruolo === 'Admin') 
			changeWin("./admin")
		else if (result.message === "log")
			changeWin("./profile");
		else if (result.message ==="reg2")
			changeWin("./register2")
		
	}
	else
		alert(result.message)
	
};

const showPwd = () => {
	console.log("cambio tipo");
	let checkb = document.getElementById(`showPwdItem`);
	let pwdDiv = document.getElementById(`passwordInput`);
		if (checkb.checked === true) 
			pwdDiv.type = "text";
		else 
			pwdDiv.type = "password";
};


const changeWin = async (url) =>window.location.href = `${url}`;