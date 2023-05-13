'use strict';

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

		console.log(`listaClassi ${listaClassi}`)
		
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
	}
	else{
		container.innerHTML=``;
	}
}

function validateEmail(input){
	let pattern = /[a-z0-9]+@[a-z]+\.[a-z]{2,3}/;
	if(input.match(pattern)){
		return false;
	}
	else{
		return true;
	}
}

const switchDiv = (divAttuale,divNuovo) =>{
	document.getElementById(divAttuale).style.display="none";
	document.getElementById(divNuovo).style.display="block";
	

}

const control = async () => {
	let nome= document.getElementById("nomeInput").value !== "" ? document.getElementById("nomeInput").value: null;
	let cognome= document.getElementById("cognomeInput").value !== "" ? document.getElementById("cognomeInput").value: null;
	let cf= document.getElementById("cfInput").value.length === 16 ? document.getElementById("cfInput").value: null;
	let dataN= document.getElementById("dateInput").value;
	let email= document.getElementById("emailInput").value;
	let ruolo = getValueRadio("ruolo");
	let genere = getValueRadio("gender");
	let classe = ruolo==="studente" ?  document.getElementById("classInput").value : null;
	let materia = ruolo==="docente" ? document.getElementById("subInput").value : null;
	let nickname= document.getElementById("nicknameInput").value !== "" ? document.getElementById("nicknameInput").value: null;
	let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
	
	let now = new Date()
	console.log(dataN)

	let dataSplit = dataN.split("-")
	console.log(`data split = ${dataSplit}\n controllo data maggiore ${parseInt(dataSplit[0]) > parseInt(now.getFullYear())}\n controllo lunghezza data ${dataSplit[0].length !== 4}`)
	//'%y/%m/%d %H:%M:%S'
	let dataFin = `${now.getFullYear()}-${now.getMonth()}-${now.getDate()}`
	if(cf === null){
		alert("CF NON VALIDO");
	}
	else if(validateEmail(email)){
		alert("Email non valida")
	}
	else if(parseInt(dataSplit[0]) > (parseInt(now.getFullYear())-13) || dataSplit[0].length !== 4 || parseInt(dataSplit[0]) <(parseInt(now.getFullYear())-100) ){
		alert("Data Non valida")
	}
	else if (nome === null || cognome === null || email === null || nickname === null || password === null)
		alert("Campi mancanti")
	else {
		let jsonDataPerson=`{
			"name" : "${nome}",
			"surname" : "${cognome}",
			"cf" : "${cf}",
			"gender" : "${genere}",
			"email" : "${email}",
			"birthday" : "${dataN}",
			"sub" : "${materia}"
		}`;
		let jsonDataClasse = ""
		if (ruolo === "studente") {
			jsonDataClasse = `{
				"Carrel" : "${classe.substring(1)}",
				"Year" : ${classe.substring(0, 1)}
			}`
		}
		else {
			jsonDataClasse = null
		}


		let jsonAccount = `{
			"Nick" : "${nickname}",
			"Pass" : "${password}",
			"Ruolo" : "${ruolo}",
			"DataReg" : "${dataFin}"
		}`;
		console.log(`json Persone= ${jsonDataPerson}\njson Account = ${jsonAccount}`);
		verify(jsonDataPerson,jsonAccount,jsonDataClasse);
	}
};


const verify = async (jsonPerson,jsonAccount,jsonDataClasse) => {
	let data;
	let str = ""
	if (jsonDataClasse === null){
		
		str = `{
			"person": ${jsonPerson},
			"acc" : ${jsonAccount}
		}`
		console.log(str)
		data = await fetch(`./api/reg1/other`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	}
	else{
		str = `{
			"classm":${jsonDataClasse},
			"person":${jsonPerson},
			"acc" : ${jsonAccount}
		}`
		console.log(str)
		
		data = await fetch(`./api/reg1/student`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str
		})
		.then(res => res.json())
		.catch(e => console.error(e));
	}
	let result = data;
	console.log(result);

	if (result.hasOwnProperty('message')){
		if (result.message !== "perfetto"){
			alert(result.message)
		}
		else{
			window.location.href = "./login";
		}
	}
	else{
		alert("Errore Generico")
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