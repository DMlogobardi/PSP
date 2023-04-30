'use strict';

const loadItems = async (url) =>{ await fetch(url)
		.then(res => res.json())
		.catch(e => console.error(e));
}

const switchRole = async (ruolo) => {
	let container = document.getElementById("classOrSub");
	if (ruolo === `doc`){
		container.innerHTML=`
			<h4>
				<label for="subInput" class="form-label" >Materia</label>
			</h4>
			<input type="text" class="form-control" id="subInput"  placeholder="Insert subject" required>
		`
	}
	else if(ruolo ==='stud'){
		let listaClassi=await loadItems("./class")		
		console.log(listaClassi)
		try {
			let forOutput=`<select name="classInput" id="classInput">`;
			for (let classe of listaClassi){
				forOutput+=`<option value="${classe.Year}${classe.Carrel}">${classe.Year}-${classe.Carrel}</option>`
			}
			forOutput+="</select>";
			container.innerHTML=`
			<h4>    
				<label for="classInput" class="form-label" >Classe</label>
			</h4>
			${forOutput}
			`;
		} catch (error) {
			console.log(listaClassi.message)
		}
			
		
	}
	else{
		container.innerHTML=``;
	}
}

const switchDiv = (divAttuale,divNuovo) =>{
	document.getElementById(divAttuale).style.display="none";
	document.getElementById(divNuovo).style.display="block";
	

}

const control = async () => {
	let nome= document.getElementById("nomeInput").value;
	let cognome= document.getElementById("cognomeInput").value;
	let cf= document.getElementById("cfInput").value.length === 16 ? document.getElementById("cfInput").value: null;
	let DataN= document.getElementById("dateInput").value;
	let email= document.getElementById("emailInput").value;
	let ruolo = getValueRadio("ruolo");
	let genere = getValueRadio("gender");
	let classe = ruolo==="studente" ?  document.getElementById("classInput").value : null;
	let materia = ruolo==="docente" ? document.getElementById("subInput").value : null;
	let nickname= document.getElementById("nicknameInput").value;
	let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
	let today = new Date();
	if(cf === null){
		alert("CF NON VALIDO");
	}
	else if (DataN > today){
		alert("Data errata");
	} 
	else if(prefissoTel.substring(0, 1)){
		alert("PREFISSO NON VALIDO");
	}
	else {
		let jsonDataPerson=`{
			"name" : "${nome}",
			"surname" : "${cognome}",
			"cf" : "${cf}",
			"gender" : "${genere}",
			"email" : "${email}",
			"birthday" : "${DataN}",
			"sub" : "${materia}"
		}`;
		if (ruolo ==="studente") {
			let jsonDataClasse = `{
				"Carrel" : ${classe.substring(1)},
				"Year" : ${classe.substring(0, 1)}
			}`
		}
		else {
			let jsonDataClasse = null
		}


		let jsonAccount = `{
			"Nick" : "${nickname}",
			"Pass" : "${password}",
			"Ruolo" : ${ruolo},
			"DataReg" : ${today}
		}`;
		console.log(`json Persone= ${jsonDataPerson}\njson Account = ${jsonAccount}`);
		verify(jsonDataPerson,jsonAccount,jsonDataClasse);
	}
};


const verify = async (jsonPerson,jsonAccount,jsonDataClasse) => {

	if (jsonDataClasse === null){
		console.log(`{
			"People": ${jsonPerson},
			"account" : ${jsonAccount}
		}`)

		const data = await fetch(`./api/reg1/other`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"People": jsonPerson,
				"account" : jsonAccount
			})
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	}
	else{
		console.log(`{
			"classm":${jsonDataClasse},
			"person":${jsonPerson},
			"acc" : ${jsonAccount}
		}`)
		
		const data = await fetch(`./api/reg1/student`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"classm": jsonDataClasse,
				"person": jsonPerson,
				"acc" : jsonAccount
			})
		})
		.then(res => res.json())
		.catch(e => console.error(e));
	}
    let result = data;
	console.log(result);
	if (result.success === false){
		alert(result.message)
	}
	else{
		
	}
	/*
	{
		success:booleano
		message:""
	}	
	*/ 
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
const getValueRadio = (id) => {
	var radios = document.getElementsByName(id);
	for (var i = 0, length = radios.length; i < length; i++) {
		if (radios[i].checked) {
			// do whatever you want with the checked radio
			console.log(radios[i].value);
			// only one radio can be logically checked, don't check the rest
			return radios[i].value;
		}
	}
};



const loadDataField = () => {
	let div = document.getElementById("campoData");
	let dataAttuale = new Date();
	let annoAttuale, meseAttuale, giornoAttuale;
	annoAttuale=dataAttuale.getFullYear();
	meseAttuale=dataAttuale.getMonth();
	giornoAttuale=dataAttuale.getDay();
	div.innerHTML=`
	<div class="mb-3">
		<h4>
			<label for="dateInput" class="form-label " >Data di nascita</label>
		</h4>
	<input type="date" class="form-control" id="dateInput" max="${annoAttuale}-${meseAttuale}-${giornoAttuale}" required>
	</div>`
};