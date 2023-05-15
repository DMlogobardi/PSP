'use strict';


const canBeHere = () =>{
	let id = sessionStorage.getItem("userId");
	let username = sessionStorage.getItem("username");
	console.log(`id = ${id} username = ${username}`)
	if (id === null && username === null){
		alert("DEVI FARE PRIMA IL LOGIN");
		window.location.href = "./login";
	}

}
window.onload=canBeHere();


const tabella= async(richiesta,list=[])=> {
	// SET VARIABILI COMUNI
	let div = document.getElementById("divTabellone");
	let headers = null;
	let data;
	let result;
	let tableHeader = ``;
	let contentTable = ``;
	let str;
	if (richiesta === "People"){
		//LISTA DEI CAMPI
		headers = ["","Name", "Surname", "CF", "Gender", "Email", "Birthday","",""];
		
		//AGGIUNTA DEGLI HEADER DELLA TABELLA
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		//RACCOLTA ED INSERIMENTO DELLE VARIE RIGHE DELLA TABELLA
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/person")
		}
		else {
			data = list
		}
		for (const person of data) {
			str = `<tr id="person${person.idPeople}">
			<td> <input type="checkbox" id="${person.idPeople}" name="cancella"></td>
			<td><p id="nome${person.idPeople}">${person.name}</p></td>
			<td><p id="cognome${person.idPeople}">${person.surname}</p></td>
			<td><p id="cf${person.idPeople}">${person.cF}</p></td>
			<td><p id="gender${person.idPeople}">${person.gender}</p></td>
			<td><p id="email${person.idPeople}">${person.email}</p></td>
			<td><p id="birthday${person.idPeople}">${person.birthday}</td>
			<td><button type="button" onclick="modifica('${person.idPeople}','People');">✏️</button></td>
			<td><button type="button" onclick="elimina('${person.idPeople}','People');">🗙</button></td>			
		  </tr>`
		  
		  contentTable += str;
		}
	}
	else if (richiesta === "Classm"){
		headers = ["","Year", "Carrel", "Articulation","Active","",""];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/classm")
		}
		else {
			data = list
		}
		for (const classe of data) {
			str = `
			<tr id="class${classe.IdClass}">
				<td> <input type="checkbox" id="${classe.IdClass}" name="cancella"></td>
				<td> <p id="year${classe.IdClass}">${classe.year}</p></td>
				<td> <p id="carrel${classe.IdClass}">${classe.carrel}</p></td>
				<td> <p id="articulation${classe.IdClass}">${classe.articulation}</p></td>
				<td> <p id="active${classe.IdClass}">${classe.active}</p></td>
				<td> <button type="button" onclick="modifica('${classe.IdClass}','Classm');">✏️</button></td>
				<td> <button type="button" onclick="elimina('${classe.IdClass}','Classm');">🗙</button></td>	
			</tr>`
		  contentTable += str;
		}
	}
	else if (richiesta === "Account"){
		headers = ["","Nick", "Ruolo", "Validità","Data Registrazione","Data Eliminazione","",""];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/account")
		}
		else {
			data = list
		}
		for (const account of data) {
			str = `<tr id= account${account.IdAccount}>
			<td> <input type="checkbox" id="${account.IdAccount}" name="cancella"></td>
			<td><p id="Nick${account.idPeople}">${account.nick}</p></td>
			<td><p id="Ruolo${account.idPeople}">${account.ruolo}</p></td>
			<td><p id="Valid${account.idPeople}">${account.valid}</p></td>
			<td><p id="DataReg${account.idPeople}">${account.dataReg}</p></td>
			<td><p id="DataExp${account.idPeople}">${account.dataExp}</p></td>
			<td><button type="button" onclick="modifica('${account.idPeople}','account');">✏️</button></td>
			<td><button type="button" onclick="elimina('${account.idPeople}','account');">🗙</button></td>	
			</tr>`
		  contentTable += str;
		}
	}
	let stringaTabella = `<table class="table table-sm">
	${tableHeader}
	${contentTable}
	</table>
	<button type="button" onClick="elimina('','${richiesta}');">ELIMINA SELEZIONATI</button>
	`
	div.innerHTML=stringaTabella;

}


const modifica = (id,tipo)=>{
	let newRiga = ``;
	if (tipo === "People"){
		
		let oldriga = document.getElementById(`person${id}`);
		// RECUPERO VALORI DA CONSERVARE
		let oldnome = document.getElementById(`nome${id}`).innerHTML;
		let oldcognome = document.getElementById(`cognome${id}`).innerHTML;
		let oldgender = document.getElementById(`gender${id}`).innerHTML;
		let oldcf = document.getElementById(`cf${id}`).innerHTML;
		let oldemail = document.getElementById(`email${id}`).innerHTML;
		let oldbirthday = document.getElementById(`birthday${id}`).innerHTML;
		console.log(oldriga);

		// FORMATTAZIONE HTML DELLA RIGA
		newRiga= `
		<tr id="person${id}">
			<td> <input type="checkbox" id="riga${id}" name="cancella"></td>
			<td> <input type="text" id="nomeIn${id}" value="${oldnome}" style=" max-width: 150px"></td>
			<td> <input type="text" id="cognomeIn${id}" value="${oldcognome}" style=" max-width: 150px"></td>
			<td> <input type="text" id="cfIn${id}" value="${oldcf}" style=" max-width: 180px"></td>
			<td> <input type="text" id="genderIn${id}" value="${oldgender}" style=" max-width: 25px"></td>
			<td> <input type="text" id="emailIn${id}" value="${oldemail}"></td>
			<td> <input type="text" id="birthdayIn${id}" value="${oldbirthday}" style=" max-width: 100px"></td>
			<td> <button type="button" onclick="confermaMod('${id}','People');">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','People');">🗙</button></td>			
		</tr>`;

		//INSERIMENTO DELLA NUOVA RIGA
	  	oldriga.innerHTML=newRiga;
	}
	else if (tipo === "Classm"){
		
		let oldriga = document.getElementById(`class${id}`);
		// RECUPERO VALORI DA CONSERVARE
		let oldYear = document.getElementById(`year${id}`).innerHTML;
		let oldActive = document.getElementById(`active${id}`).innerHTML;
		let oldCarrel = document.getElementById(`carrel${id}`).innerHTML;
		let oldArticulation = document.getElementById(`articulation${id}`).innerHTML;

		console.log(oldriga);

		// FORMATTAZIONE HTML DELLA RIGA
		newRiga= `
		<tr id="person${id}">
			<td> <input type="checkbox" id="riga${id}" name="cancella"></td>
			<td> <input type="text" id="yearIn${id}" value="${oldYear}" style=" max-width: 20px"></td>
			<td> <input type="text" id="carrelIn${id}" value="${oldCarrel}" style=" max-width: 20px"></td>
			<td> <input type="text" id="articulationIn${id}" value="${oldArticulation}" style=" max-width: 180px"></td>
			<td> <input type="text" id="activeIn${id}" value="${oldActive}" style=" max-width: 180px"></td>
			<td> <button type="button" onclick="confermaMod('${id}','Classm');">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','Classm');">🗙</button></td>			
		</tr>`;

		//INSERIMENTO DELLA NUOVA RIGA
	  	oldriga.innerHTML=newRiga;
	}
	else if (tipo === "account"){
		
		let oldriga = document.getElementById(`account${id}`);
		// RECUPERO VALORI DA CONSERVARE
		let oldNick = document.getElementById(`Nick${id}`).innerHTML;
		let oldRuolo = document.getElementById(`Ruolo${id}`).innerHTML;
		let oldValid = document.getElementById(`Valid${id}`).innerHTML;
		let oldDataReg = document.getElementById(`DataReg${id}`).innerHTML;
		let oldDataExp = document.getElementById(`DataExp${id}`).innerHTML;
		console.log(oldriga);

		// FORMATTAZIONE HTML DELLA RIGA
		newRiga= `
		<tr id="person${id}">
			<td> <input type="checkbox" id="riga${id}" name="cancella"></td>
			<td> <input type="text" id="NickIn${id}" value="${oldNick}" style=" max-width: 150px"></td>
			<td> <input type="text" id="RuoloIn${id}" value="${oldRuolo}" style=" max-width: 150px"></td>
			<td> <input type="text" id="ValidIn${id}" value="${oldValid}" style=" max-width: 180px"></td>
			<td> <input type="text" id="DataRegIn${id}" value="${oldDataReg}" style=" max-width: 25px"></td>
			<td> <input type="text" id="DataExpIn${id}" value="${oldDataExp}"></td>
			<td> <button type="button" onclick="confermaMod('${id}','account');">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','account');">🗙</button></td>			
		</tr>`;

		//INSERIMENTO DELLA NUOVA RIGA
	  	oldriga.innerHTML=newRiga;
	}
}


const confermaMod = async (id,tab) =>{
	console.log(`INGRESSO IN CONFERMAMOD ${tab}`)
	if (tab === "People"){
		//SET VALORI
		let valori = [
			document.getElementById(`nomeIn${id}`).value,
			document.getElementById(`cognomeIn${id}`).value, 
			document.getElementById(`cfIn${id}`).value,
			document.getElementById(`genderIn${id}`).value,
			document.getElementById(`emailIn${id}`).value,
			document.getElementById(`birthdayIn${id}`).value
		]
		// CONTROLLI

		// FORMATTAZIONE JSON
		let str = `{
			"name" : "${valori[0]}",
			"surname" : "${valori[1]}"
			"cF" : "${valori[2]}",
			"gender" :"${valori[3]}",
			"email" : "${valori[4]}",
			"birthday" : "${valori[5]}"
		}`;
		//INVIO

		console.log(str)

		
	}

	else if (tab === 'Classm'){
		console.log(`INGRESSO IN IF ${tab}`)

		//SET VALORI
		let valori = [
			document.getElementById(`yearIn${id}`).value,
			document.getElementById(`carrelIn${id}`).value, 
			document.getElementById(`articulationIn${id}`).value,
			document.getElementById(`activeIn${id}`).value
		]
		// CONTROLLI

		// FORMATTAZIONE JSON
		let str = `{
			"year" : "${valori[0]}",
			"carrel" : "${valori[1]}",
			"articulation" : "${valori[2]}",
			"active" : "${valori[3]}"
		}`;
		//INVIO
		console.log(str)

	}

	else if (tab === 'account'){
		//SET VALORI
		let valori = [
			document.getElementById(`NickIn${id}`).value,
			document.getElementById(`RuoloIn${id}`).value, 
			document.getElementById(`ValidIn${id}`).value,
			document.getElementById(`DataRegIn${id}`).value,
			document.getElementById(`DataExpIn${id}`).value
		]
		// CONTROLLI

		// FORMATTAZIONE JSON
		let str = `{
			"nick" : "${valori[0]}",
			"ruolo" : "${valori[1]}"
			"valid" : "${valori[2]}",
			"dataReg" :"${valori[3]}",
			"dataExp" : "${valori[4]}"
		}`;
		//INVIO
		console.log(str)
		
	}
	data = await fetch(`./api/update/${tab}/${id}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	tabella(tab);
}

const elimina = async (id,tab) =>{
	console.log("ingresso in elimina")
	if(id === ""){
		let lista = getCheckedBoxes("cancella");
		console.log(lista)
		const data = await fetch(`./api/delete/${tab}`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			},
			body: lista}
		)
		.then(res => res.json())
		.catch(e => console.error(e));
		let result = data;
		console.log(result);
		tabella(tab)
	}
	else{
		let str =`[
			${id}
		]`;
		const data = await fetch(`./api/delete/${tab}`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str}
		)
		.then(res => res.json())
		.catch(e => console.error(e));
		let result = data;
		console.log(result);
		tabella(tab)
	}
}

const filter = (tab,campo,strOut) =>{
	let divFiltro = document.getElementById("divFiltro");
	let strDiv;
	switch (campo) {
		case 'birthday':
			strDiv = `
				<div class="mb-3">
					<h4>
						<label for="dateInput" class="form-label " >Data di nascita</label>
					</h4>
					<input type="date" class="form-control" id="dateInput" max="${annoAttuale}-${meseAttuale}-${giornoAttuale}" required>
				</div>`;
			break;

		case 'gender':
				strDiv = `
				<div class="mb-3">
                    <div class="sceltaGenere">
                        <h4>
                            <label for="sceltaGenere" >Sesso</label><br>
                        </h4>
                        <input type="radio" id="Uomo" name="gender" value="M" checked>
                        <label for="Uomo">Uomo</label><br>
                        <input type="radio" id="Donna" name="gender" value="F">
                        <label for="Donna">Donna</label><br>
                    </div>
                </div>`;
			break;

		case 'ruolo':
			strDiv = `<div class="sceltaRuolo">
			<h4>
				<label for="sceltaGenere" >Ruolo</label><br>
			</h4>
			<input type="radio" id="doc" name="ruolo" value="docente" onclick="switchRole('doc')" checked>
			<label for="doc">Docente</label><br>
			<input type="radio" id="stud" name="ruolo" value="studente" onclick="switchRole('stud')">
			<label for="stud">Studente</label><br>
			<input type="radio" id="ata" name="ruolo" value="ata" onclick="switchRole('ata')">
			<label for="ata">Personale ata</label><br>
		</div>`;
			break;

		case 'year':
			strDiv = `<input type="number" id="yearFilter" min="1" max="5" placeholder="Inserisci l'anno da cercare">`
			break;
		
		default:
			strDiv = `
			<div class="mb-3" >
				<h4>
					<label for="filter" class="form-label " >${strOut}</label>
				</h4>
				<input type="text" class="form-control" id="filter" placeholder="Insert ${campo}" required>
			</div>`;
			break;
	}
	strDiv+=`<button type="button" onclick="filtra('${tab}','${campo}');">🔎</button>`;
	divFiltro.innerHTML=strDiv;
}

const filtra = async (tab,campo)=>{
	let filterData = document.getElementById(filter).value;
	let str = `{
		"${campo}":"${filterData}"
	}`
	data = await fetch(`./api/filter/${tab}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	tabella(tab,data);
}

const getCheckedBoxes = (chkboxName)=>{
	var checkboxes = document.getElementsByName(chkboxName);
	var checkboxesChecked = [];
	
	for (var i=0; i<checkboxes.length; i++) {
	
	   if (checkboxes[i].checked) {
		  checkboxesChecked.push(checkboxes[i].id);
	   }
	}

	return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}