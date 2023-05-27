'use strict';
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
				<li class="list-group-item text-bg-light border-dark"><b>NOME</b>: ${res.name}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>COGNOME</b>: ${res.surname}</li>
				<li class="list-group-item text-bg-light border-dark"><b>CF</b>: ${res.cf}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>SESSO</b>: ${res.gender}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>EMAIL</b>: ${res.email}</li>
			    <li class="list-group-item text-bg-light border-dark"><b>DATA DI NASCITA</b>: ${res.birthday}</li>
				`;
				if (ruolo === "docente"){
					stringRis+=`<li class="list-group-item text-bg-light border-dark"><b>MATERIA</b>: ${res.sub}</li>`
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
						stringRis+=`<li id="classeList" class="list-group-item text-bg-light border-dark"><b>CLASSE</b>: ${resClasse.year}-${resClasse.carrel}</li>`;
					}
					else{
						alert("Errore sulla raccolta dati")
					}
				}
			}
			break;

		case "Phone":
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
					<li class="list-group-item text-bg-light border-dark"> ${tel.prefix} ${tel.number} <span style="display: inline-block; width: 2ch;">&#9;</span> <button type="button" onclick="elimina('','phone');">✏️</button>
					<button type="button" onclick="elimina('','phone');">🗙</button></li>
					`;
				}
			}
			break;
	
		case "Vehicle":
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
					<li class="list-group-item text-bg-light border-dark"><b>TIPO</b> : ${veicolo.type}<br>
					<b>TARGA</b> : ${veicolo.plate}<br>
					<b>PROPRIETARIO</b>: ${veicolo.owner}<br>
					<button type="button" onclick="elimina('','phone');">✏️</button>
					<button type="button" onclick="elimina('','phone');">🗙</button>
					</li>
					`;
				}
			}
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
			    <li class="list-group-item text-bg-light border-dark"><b>DATA REGISTRAZIONE</b>: ${res.dataReg}</li>
				`;
			}
			break;
		
		default:
			
			break;
		
	}
	carta.innerHTML=stringRis;
}

window.onload=canBeHere();