'use strict';

let listaElementi=0;

const canBeHere = () =>{
	let id = sessionStorage.getItem("userId");
	let username = sessionStorage.getItem("username");
	let ruolo = sessionStorage.getItem("ruolo");
	console.log(`id = ${id} username = ${username}`)
	if (id === null && username === null){
		alert("DEVI FARE PRIMA IL LOGIN");
		window.location.href = "./login";
	}
	else if ((username === "Admin") || (ruolo === "Admin") ) {
		alert("NON PUOI ESSERE QUI");
		window.location.href = "./login";
	}
	window.setTimeout("card('Account')", 200);
}

const card = async (tab='')=>{
	let id = sessionStorage.getItem("userId");
	let carta = document.getElementById("carta");
	let stringRis=``;
	let ruolo = sessionStorage.getItem("ruolo");
	let data;
	let titolo = document.getElementById("titolo");
	let filtro = ``;
	let res;
	let idPeople;
	console.log("INGRESSO IN CARD");
	switch (tab) {
		case "Person":
			let strStud="";
			idPeople = sessionStorage.getItem("idPeople");
			filtro = `{
				"idPeople" : ${idPeople}
			}`;
			data = await fetch(`./api/filter/${tab}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: filtro }
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			res = data[0];
			if (!res.hasOwnProperty('idPeople')){
				alert("ERRORE SULLA RACCOLTA DATI");
			}
			else {
				titolo.innerHTML=`<b>DATI PERSONALI</b>`
				stringRis=`
				<li class="list-group-item text-bg-light border-dark"><b>NOME</b>: <r id='name${res.idPeople}'>${res.name}</r> </li>
			    <li class="list-group-item text-bg-light border-dark"><b>COGNOME</b>: <r id='surname${res.idPeople}'>${res.surname}</r></li>
				<li class="list-group-item text-bg-light border-dark"><b>CF</b>: <r id='cf${res.idPeople}'>${res.cf}</r></li>
			    <li class="list-group-item text-bg-light border-dark"><b>SESSO</b>: <r id='gender${res.idPeople}'>${res.gender}</r></li>
			    <li class="list-group-item text-bg-light border-dark"><b>EMAIL</b>: <r id='email${res.idPeople}'>${res.email}</r></li>
			    <li class="list-group-item text-bg-light border-dark"><b>DATA DI NASCITA</b>:<r id='dataN${res.idPeople}'>${res.birthday}</r></li>
				`;
				if (ruolo === "docente"){
					stringRis+=`<li class="list-group-item text-bg-light border-dark"><b>NOME</b>: <r id='materia${res.idPeople}'>${res.sub}</r></li>`
				}
				else if(ruolo === "studente"){
					let strReq = `{
							"idClass" : ${res.idClass}
					}`
					let classe = await fetch(`./api/filter/classm`, {
						method: 'PUT',
						headers: {
							'Content-Type': 'application/json'
						},
						body: strReq}
					)
					.then(res => res.json())
					.catch(e => console.error(e));
					let resClasse = classe[0]
					if (resClasse.hasOwnProperty('year')){
						stringRis+=`
						<li id="classeList" class="list-group-item text-bg-light border-dark">
							<b>CLASSE</b>: <r value="${resClasse.idClass}" id="class">${resClasse.year}-${resClasse.carrel}</r>
						</li>
						`;
						strStud=`
						<div id="bottoneModificaClasse">
							<button type="button" class="btn btn-sm btn-primary" onclick="editClass();">Modifica Classe</button>
						</div>
						`
					}
					else{
						alert("Errore sulla raccolta dati")
					}
				}
				stringRis+=`
				<li class="list-group-item text-bg-light border-dark">
					<button type="button" class="btn btn-sm btn-primary" onclick="editPerson();">Modifica dati personali</button>
				
				${strStud}
				</li>
				`
					
			}

			break;

		case "Phone":
			listaElementi=0;
			idPeople = sessionStorage.getItem("idPeople");
			filtro = `{
				"idPeople" : ${idPeople}
			}`;
			data = await fetch(`./api/filter/${tab}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: filtro}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			res = data;
			for (let tel of res){
				if (!tel.hasOwnProperty('idPeople')){
					alert("ERRORE SULLA RACCOLTA DATI");
					break;
				}
				else {
					console.log(tel)
					titolo.innerHTML="<b>TELEFONI<b>"
					stringRis+=`
					<li class="list-group-item text-bg-light border-dark" id="${tab}${tel.idPhones}"> 
					${tel.prefix} ${tel.number} 
					<span style="display: inline-block; width: 2ch;">&#9;</span> 
					<button type="button" onclick="modifyItem('Phone',${tel.idPhones},['${tel.prefix}',${tel.number}]);">✏️</button>
					<button type="button" onclick="deleteField('Phone',${tel.idPhones});">🗙</button></li>
					`;
				}
				listaElementi++;
			}
			stringRis+=`
			<li id="newElement" class="list-group-item text-bg-light border-dark" style="display: none;">
				<div class="center-70">
					<input type="text" value="+39" id='newPref'>
					<input type="text" placeholder="inserisci telefono" id="newNumber"><br>
					<button type="button" onclick="addElement('Phone');"  class="btn btn-sm btn-primary">Invia</button>
				</div>
			</li>

			<li class="list-group-item text-bg-light border-dark">
				<button type="button" class="btn btn-sm btn-primary" onclick="nuovoElemento();">Aggungi telefono</button>
			</li>
			
			`

			break;
	
		case "Vehicle":
			listaElementi=0;
			idPeople = sessionStorage.getItem("idPeople");
			filtro = `{
				"idPeople" : ${idPeople}
			}`;
			data = await fetch(`./api/filter/${tab}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: filtro}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			res = data;
			for (let veicolo of res){
				if (!veicolo.hasOwnProperty('idPeople')){
					alert("ERRORE SULLA RACCOLTA DATI");
					break;
				}
				else {
					console.log(veicolo)
					titolo.innerHTML=`<b>VEICOLI<b> `
					stringRis+=`
					<li class="list-group-item text-bg-light border-dark" id="${tab}${veicolo.idV}"><b>TIPO</b> : ${veicolo.type}<br>
					<b>TARGA</b> : ${veicolo.plate}<br>
					<b>PROPRIETARIO</b>: ${veicolo.owner}<br>
					<button type="button" onclick="modifyItem('Vehicle',${veicolo.idV},['${veicolo.type}','${veicolo.plate}','${veicolo.owner}']);">✏️</button>
					<button type="button" onclick="deleteField('Vehicle',${veicolo.idV});">🗙</button>
					</li>
					`;
				}
				listaElementi++;
			}
			stringRis+=
			`
			<li id="newElement" class="list-group-item text-bg-light border-dark" style="display: none;">
				<div class="center-70">
					<label for="typeVehicle">Tipo veicolo:</label>
					<select id="typeVehicle" name="type">
						<option value="auto">Auto</option>
						<option value="moto">Moto</option>
						<option value="altro">Altro</option>
					</select><br>
					<input type="text" placeholder="Targa" id='newPlate' >
					<input type="text" placeholder="Proprietario" id="newOwner"><br>
					<button type="button" onclick="addElement('Vehicle');"  class="btn btn-sm btn-primary">Invia</button>
				</div>
			</li>

			<li class="list-group-item text-bg-light border-dark">
				<button type="button" class="btn btn-sm btn-primary" onclick="nuovoElemento();">Aggungi Veicolo</button>
			</li>
			`
			break;
		
		case "Account":
			filtro = `{
				"idAccount" : ${id}
			}`
			data = await fetch(`./api/filter/${tab}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: filtro}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			res = data[0];
			console.log(res)
			if (!res.hasOwnProperty('idPeople')){
				alert("ERRORE SULLA RACCOLTA DATI");
			}
			else {
				sessionStorage.setItem("idPeople",res.idPeople);
				titolo.innerHTML=`<b>DATI ACCOUNT<b>`
				stringRis=`
				<li class="list-group-item text-bg-light border-dark"><b>NICK</b>: ${res.nick}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>RUOLO</b>: ${res.ruolo}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>DATA REGISTRAZIONE</b>: <br>${res.dataReg}</li>
				`;
			}
			break;		
	}
	carta.innerHTML=stringRis;
}

window.onload=canBeHere();

const nuovoElemento = () =>{
	let elemento = document.getElementById("newElement");
	if(elemento.style.display==="block"){
		alert("Inserisci i valori")
	}
	else{
		elemento.style.display="block";

	}
}
const addElement = async (tab) =>{
	let data;
	let str;
	if(tab ==="Phone"){
		let pref = document.getElementById("newPref").value;
		let number = document.getElementById("newNumber").value;
		let id = sessionStorage.getItem("idPeople");
		if(pref === "" || number === ""){
			alert("campi vuoti");
		}
		else if(pref.substring(0,0) === "+"){
			alert("PREFISSO NON VALIDO");
		}
		// FORMATTAZIONE JSON
		else{
			str = `{
				"idPeople" : ${id},
				"prefix" : "${pref}",
				"number" : "${number}"
			}`;

			data = await fetch(`./api/insert/phone`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: str
				}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			card("Phone");
		}
	}
	else if(tab ==="Vehicle"){
		let type = document.getElementById("typeVehicle").value;
		let targa = document.getElementById("newPlate").value;
		let prop = document.getElementById("newOwner").value;
		let id = sessionStorage.getItem("idPeople");
		if(targa === "" || prop === ""){
			alert("campi vuoti");
		}
		// FORMATTAZIONE JSON
		else{
			str = `{
				"idPeople" : ${id},
				"type" : "${type}",
				"plate" : "${targa}",
				"owner" : "${prop}"
			}`;

			data = await fetch(`./api/insert/vehicle`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: str
				}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			card("Vehicle");
		}
	}
}

const deleteField = async (tab="",id=-1)=>{
	console.log("Ingresso in elimina")
	if(listaElementi === 1){
		if(tab === "Vehicle"){
			alert("NON PUOI ELIMINARE IL TUO UNICO VEICOLO")
		}
		else if(tab === "Phone"){
			alert("NON PUOI ELIMINARE IL TUO UNICO NUMERO DI TELEFONO")
		}
	}
	else if(id<0){
		alert("Errore negli ID")
	}
	else{
		console.log("Ingresso in Elimina")
		let str =`[
			${id}
		]`;
		const data = await fetch(`./api/delete/${tab}`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str
		}
		)
		.then(res => res.json())
		.catch(e => console.error(e));
		let result = data;
		console.log(result);
		card(tab);
	}
}

const modifyItem = (tab="",id=0,field=[]) =>{
	let riga = document.getElementById(`${tab}${id}`);
	let str;
	if (tab ==="Phone"){
		str=`
		<input type="text" value="${field[0]}" id="prefix${id}" placeholder="Prefisso">
		<input type="text" value="${field[1]}" id="number${id}" placeholder="Numero">  
		<br>
		<button type="button" onclick="confirmMod('Phone',${id});">✏️</button>
		<button type="button" onclick="deleteField('Phone',${id});">🗙</button></li>`
	}
	else if (tab ==="Vehicle"){
		str=`
		<li class="list-group-item text-bg-light border-dark">
		<label for="typeVehicle">Tipo veicolo:</label>
		<select id="typeVehicle${id}" name="type">
			<option value="auto">Auto</option>
			<option value="moto">Moto</option>
			<option value="altro">Altro</option>
		</select><br>
		<b>TARGA</b> : <input type="text" value="${field[1]}" id="plate${id}" placeholder="Targa"><br>
		<b>PROPRIETARIO</b>: <input type="text" value="${field[2]}" id="prop${id}" placeholder="Proprietario"> <br>
		<button type="button" onclick="confirmMod('Vehicle',${id});">✏️</button>
		<button type="button" onclick="deleteField('Vehicle',${id});">🗙</button>
		</li>
		`;
	}
	riga.innerHTML=str
	console.log(field)
}

const confirmMod=async (tab,id) =>{
	let str;

	if(tab === "Phone"){
		//SET VALORI
		let varPref = document.getElementById(`prefix${id}`).value;
		let varNumber = document.getElementById(`number${id}`).value;
		// CONTROLLI
		if(varPref === "" || varNumber === ""){
			alert("campi vuoti");
			return
		}
		else if(varPref.substring(0,0) === "+"){
			alert("PREFISSO NON VALIDO");
			return
		}
		// FORMATTAZIONE JSON
		str = `{
			"prefix" : "${varPref}",
			"number" : "${varNumber}",
			"idPeople" : "${sessionStorage.getItem("idPeople")}"
		}`;
		console.log(str)
	}
	else if(tab === "Vehicle"){
		//SET VALORI
		let varTarga = document.getElementById(`plate${id}`).value;
		let varTipo = document.getElementById(`typeVehicle${id}`).value; 
		let varProp = document.getElementById(`prop${id}`).value;
		// CONTROLLI
		if ( varTarga === "" || varTipo === "" || varProp === "" ){
			alert("campi vuoti");
			return
		}
		else if (varTipo !== "auto" && varTipo !== "moto" && varTipo !== "altro" ){
			alert("tipo non valido");
			return
		}
		// FORMATTAZIONE JSON
		str = `{
			"plate" : "${varTarga}",
			"type" : "${varTipo}",
			"owner" : "${varProp}",
			"idPeople" : "${sessionStorage.getItem("idPeople")}"
		}`;
		//INVIO

		console.log(str)
	}
	let data = await fetch(`./api/update/${tab}/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	card(tab)
}

const editClass =async ()=>{
	let rigaClasse = document.getElementById("classeList");
	let listaClassi = await loadItems("./class")

		console.log(`listaClassi ${listaClassi}`)
		
			let forOutput=`<select name="classInput" id="class">`;
			for (let classe of listaClassi){
				forOutput+=`<option value="${classe.idClass}">${classe.year}-${classe.carrel}</option>`
			}
			forOutput+="</select>";
			rigaClasse.innerHTML=`
			<b>CLASSE</b>:
			${forOutput}
			`;
	let newBtn = document.getElementById("bottoneModificaClasse");
	newBtn.innerHTML=`
	<button type="button" class="btn btn-sm btn-primary" onclick="confirmClass();">Conferma cambio classe</button>
	`;
}

const confirmClass = async ()=>{
	let idClass = document.getElementById(`class`).value; 
	let id= sessionStorage.getItem("idPeople")
	let name = document.getElementById(`name${id}`).innerHTML;
	let surname = document.getElementById(`surname${id}`).innerHTML;
	let cf = document.getElementById(`cf${id}`).innerHTML;
	let email = document.getElementById(`email${id}`).innerHTML;
	let dataN = document.getElementById(`dataN${id}`).innerHTML;
	let gender = document.getElementById(`gender${id}`).innerHTML;
	let str = `{
		"name":"${name}",
		"surname":"${surname}",
		"cf":"${cf}",
		"gender": "${gender}",
		"email": "${email}",
		"dataN": "${dataN}",
		"idClass":"${idClass}"
	}`; 
	let data = await fetch(`./api/update/Person/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	card("Person")
}
const editPerson = () =>{
	let id= sessionStorage.getItem("idPeople")
	let idClass=-1;
	let materia ="";
	let strMateria=""
	if (sessionStorage.getItem("ruolo") === "studente"){
		idClass = document.getElementById(`class`).value; 
	}
	else{
		materia = document.getElementById(`materia${id}`).innerHTML;
		strMateria = `<li class="list-group-item text-bg-light border-dark"><b>Materia</b>: <br><input type="text" id='materia${id}' value="${materia}"></li>
		`
	}
	let name = document.getElementById(`name${id}`).innerHTML;
	let surname = document.getElementById(`surname${id}`).innerHTML;
	let cf = document.getElementById(`cf${id}`).innerHTML;
	let email = document.getElementById(`email${id}`).innerHTML;
	let dataN = document.getElementById(`dataN${id}`).innerHTML;
	let gender = document.getElementById(`gender${id}`).innerHTML;
	let carta=document.getElementById("carta");
	let str=`
	<li class="list-group-item text-bg-light border-dark"><b>NOME</b>: <br><input type="text" id='name${id}' value="${name}"> </li>
	<li class="list-group-item text-bg-light border-dark"><b>COGNOME</b>: <br><input type="text" id='surname${id}' value="${surname}"></li>
	<li class="list-group-item text-bg-light border-dark"><b>CF</b>: <br><input type="text" id='cf${id}' value="${cf}"></li>
	<li class="list-group-item text-bg-light border-dark"><b>SESSO</b>: <br><input type="text" id='gender${id}' value="${gender}"></li>
	<li class="list-group-item text-bg-light border-dark"><b>EMAIL</b>: <br><input type="text" id='email${id}' value="${email}"></li>
	<li class="list-group-item text-bg-light border-dark"><b>DATA DI NASCITA</b>: <br><input type="text" id='dataN${id}' value="${dataN}"></li>
	${strMateria}
	<li class="list-group-item text-bg-light border-dark">
				<button type="button" class="btn btn-sm btn-primary" onclick="confirmPerson(${idClass});">Conferma modifica</button>
	</li>
	`
	carta.innerHTML=str;
}

const confirmPerson =async (idClass)=>{
	let id = sessionStorage.getItem("idPeople")
	let varnome = document.getElementById(`name${id}`).value;
	let varcognome = document.getElementById(`surname${id}`).value; 
	let varCf = document.getElementById(`cf${id}`).value;
	let varGender = document.getElementById(`gender${id}`).value;
	let varEmail = document.getElementById(`email${id}`).value;
	let varDataNascita = document.getElementById(`dataN${id}`).value;
	let materia=null;
	let str
	if (idClass===0){
		materia = document.getElementById(`materia${id}`).value;
	}
	let now = new Date()
	// CONTROLLI
	let dataSplit = varDataNascita.split("-")
	console.log(`data split = ${dataSplit}\n controllo data maggiore ${parseInt(dataSplit[0]) > parseInt(now.getFullYear())}\n controllo lunghezza data ${dataSplit[0].length !== 4}`)
	
	if(varCf === null){
		alert("CF NON VALIDO");
		return;
	}
	else if(varGender !== "F" && varGender!=="M"){
		alert("Sesso non valido")
		return
	}
	else if(validateEmail(varEmail)){
		alert("Email non valida")
		return
	}
	else if(parseInt(dataSplit[0]) > (parseInt(now.getFullYear())-13) || dataSplit[0].length !== 4 || parseInt(dataSplit[0]) < (parseInt(now.getFullYear())-100) ){
		alert("Data Non valida")
		return
	}
	else if (varnome === "" || varcognome === "" || varEmail === "" || varGender === "" || varCf === "" || varDataNascita === ""){
		alert("Campi mancanti")
		return
	}
	// FORMATTAZIONE JSON
	if(idClass===0){
		str = `{
			"name" : "${varnome}",
			"surname" : "${varcognome}",
			"cF" : "${varCf}",
			"gender" :"${varGender}",
			"email" : "${varEmail}",
			"birthday" : "${varDataNascita}",
			"sub": "${materia}"
		}`;
	}
	else{
		str = `{
			"name" : "${varnome}",
			"surname" : "${varcognome}",
			"cF" : "${varCf}",
			"gender" :"${varGender}",
			"email" : "${varEmail}",
			"birthday" : "${varDataNascita}",
			"idClass": "${idClass}"
		}`;
	}
	let data = await fetch(`./api/update/Person/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	card("Person")
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