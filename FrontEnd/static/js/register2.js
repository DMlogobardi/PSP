'use strict';

const loadItems =
	async (url) => await fetch(url)
		.then(res => res.json())
		.catch(e => console.error(e));


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
		let classes = JSON.parse(listaClassi);
		console.log(classes)
		
		try {
			let forOutput=`<select name="classInput" id="classInput">`;
			for (let classe of classes){
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
			alert(classes.message)
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
	let classe = ruolo==="stud" ?  document.getElementById("classInput").value : null;
	let materia = ruolo==="doc" ? document.getElementById("subInput").value : null;
	let nickname= document.getElementById("nicknameInput").value;
	let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
	let targa = document.getElementById("targaInput").value;
	let prefissoTel = document.getElementById("prefInput").value;
	let telNum = document.getElementById("telInput").value;
	let today = new Date();
	if(cf === null){
		alert("CF NON VALIDO");
	}
	else if (DataN > today){
		alert("CF NON VALIDO");
	} 
	else if(prefissoTel.substring(0, 1)){
		alert("PREFISSO NON VALIDO");
	}
	else {
		let jsonDataPerson=`{
			"name" : "${nome}",
			"surname" : "${cognome}",
			"classm" : "${classe}",
			"cf" : "${cf}",
			"gender" : "${genere}",
			"email" : "${email}",
			"birthday" : "${DataN}",
			"sub" : "${materia}"
		}`

		let jsonTelefono=`{
			"prefix" : "${prefissoTel}",
			"number" : "${telNum}"
		}
		`;

		let jsonVeicolo=`{
			"type" : "${null}",
			"plate" : "${null}",
			"owner" : "${null}"
		}
		`;

		let jsonAccount = `{
			"nickname" : "${nickname}",
			"password" : "${password}"
		}`;
		console.log(`json Persone= ${jsonDataPerson}\njson Account = ${jsonAccount}`);
		verify(jsonDataPerson,jsonAccount,jsonTelefono,jsonVeicolo);
	}
};


const verify = async (jsonPerson,jsonAccount,jsonTelefono,jsonVeicolo) => {
	const data = await fetch(`./api`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"People": jsonPerson,
				"account" : jsonAccount,
				"telephone" : jsonTelefono,
				"vehicles" : jsonVeicolo
			})
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	if (data.success === true)
		window.location.href = "./qr";
};

const showPwd = async () => {
	var input = document.getElementById('passwordInput');
		if (input.type === "password") 
		  input.type = "text";
		else 
		  input.type = "password";
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