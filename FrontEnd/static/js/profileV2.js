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
	else if ((username === "Admin") || (ruolo === "Admin") || (id === 1)) {
		alert("NON PUOI ESSERE QUI");
		window.location.href = "./login";
	}
}

const card = async (tab='')=>{
	let id = sessionStorage.getItem("userId");
	let carta = document.getElementById("carta");
	let stringRis=``;
	let ruolo = sessionStorage.getItem("ruolo");
	let data;
	let titolo = document.getElementById("titolo");
	let filtro = `FILTRO CHE DEVE DIRE DAVIDE`;
	let res;
	console.log("INGRESSO IN CARD");
	switch (tab) {
		case "People":
			data = await fetch(`./api/filter/${tab}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: filtro }
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			res = data;
			if (!res.hasOwnProperty('idPeople')){
				alert("ERRORE SULLA RACCOLTA DATI");
			}
			else {
				titolo.innerHTML=`${res.surname} ${res.name}`
				stringRis=`
				<li class="list-group-item text-bg-light border-dark">${res.cF}</li>
			    <li class="list-group-item text-bg-light border-dark">${res.gender}</li>
			    <li class="list-group-item text-bg-light border-dark">${res.email}</li>
			    <li class="list-group-item text-bg-light border-dark">${res.birthday}</li>
				`;
				if (ruolo === "docente"){
					stringRis+=`<li class="list-group-item text-bg-light border-dark">${res.sub}</li>`
				}
				else if(ruolo === "studente"){
					let strReq = `{
						data : {
							"idPeople" : ${id}
						}
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
					if (classe.hasOwnProperty('year')){
						stringRis+=`<li id="classeList" class="list-group-item text-bg-light border-dark">${classe.year}-${classe.carrel}</li>`;
					}
					else{
						alert("Errore sulla raccolta dati")
					}
				}
			}
			break;

		case "Classm":
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
			if (!res.hasOwnProperty('idPeople')){
				alert("ERRORE SULLA RACCOLTA DATI");
			}
			else {

			}
			break;
		
		case "Phone":
			
			break;
	
		case "Vehicles":
			
			break;
		
		case "Account":
			
			break;
		
		default:
			
			break;
		
	}
	carta.innerHTML=stringRis;
}
