'use strict';


const tabella = async(richiesta,list=[])=> {
	let divFiltro = document.getElementById("divFiltro");
	divFiltro.style.display="none";
	// SET VARIABILI COMUNI
	console.log("INGRESSO IN TABELLA")
	
	let div = document.getElementById("divTabellone");
	let headers = null;
	let data;
	let tableHeader = ``;
	let contentTable = ``;
	let str;
	if (richiesta.toLowerCase() === "people" || richiesta.toLowerCase() === "person"){
		//LISTA DEI CAMPI
		headers = ["","Name", "Surname", "CF", "Gender", "Email", "Birthday","Telefoni","Veicoli","",""];
		
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
			<td><p id="cf${person.idPeople}">${person.cf}</p></td>
			<td><p id="gender${person.idPeople}">${person.gender}</p></td>
			<td><p id="email${person.idPeople}">${person.email}</p></td>
			<td><p id="birthday${person.idPeople}">${person.birthday}</td>
			<td><button type="button" onclick="join('${person.idPeople}','Phone');">➡️</button></td>
			<td><button type="button" onclick="join('${person.idPeople}','Vehicle');">➡️</button></td>
			<td><button type="button" onclick="modifica('${person.idPeople}','person',0,'${person.sub!=null ? person.sub : ""}',${person.idClass!=null ? person.idClass : 0});">✏️</button></td>
			<td><button type="button" onclick="elimina('${person.idPeople}','person');">🗙</button></td>			
		  </tr>`
		  
		  contentTable += str;
		}
		richiesta="person";
	}
	else if(richiesta.toLowerCase() === 'entris'){
		console.log("Ingresso in entris")
		//LISTA DEI CAMPI
		headers = ["Account", "Data Ingresso", "Data Uscita"];
				
		//AGGIUNTA DEGLI HEADER DELLA TABELLA
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		//RACCOLTA ED INSERIMENTO DELLE VARIE RIGHE DELLA TABELLA
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/entris")
		}
		else {
			data = list
		}
		for (const ingresso of data) {
			str = `<tr>
			<td><button type="button" onclick="join('${ingresso.idAccount}','Account');">➡️</button></td>
			<td><p>${ingresso.dataIn}</p></td>
			<td><p>${ingresso.dataOut === null ? "-": ingresso.dataOut}</p></td>			
		</tr>`
		
		contentTable += str;
		}
	}
	else if (richiesta.toLowerCase() === 'phone'){
		//LISTA DEI CAMPI
		headers = ["","Prefix", "Number","Person","",""];
		
		//AGGIUNTA DEGLI HEADER DELLA TABELLA
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		//RACCOLTA ED INSERIMENTO DELLE VARIE RIGHE DELLA TABELLA
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/phone")

		}
		else {
			data = list
		}
		for (const phone of data) {
			str = `<tr id="phone${phone.idPhones}">
			<td> <input type="checkbox" id="${phone.idPhones}" name="cancella"></td>
			<td><p id="prefix${phone.idPhones}">${phone.prefix}</p></td>
			<td><p id="number${phone.idPhones}">${phone.number}</p></td>
			<td><button type="button" onclick="join('${phone.idPeople}','person');">➡️</button></td>
			<td><button type="button" onclick="modifica('${phone.idPhones}','phone',${phone.idPeople});">✏️</button></td>
			<td><button type="button" onclick="elimina('${phone.idPhones}','phone');">🗙</button></td>			
		  </tr>`
		  
		  contentTable += str;
		}
	}
	else if (richiesta.toLowerCase() === "classm"){
		headers = ["","Year", "Carrel", "Articulation","Active","Studenti","",""];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th  scope="col">${elem}</th>`;
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
			<tr id="class${classe.idClass}">
				<td> <input type="checkbox" id="${classe.idClass}" name="cancella"></td>
				<td> <p id="year${classe.idClass}">${classe.year}</p></td>
				<td> <p id="carrel${classe.idClass}">${classe.carrel}</p></td>
				<td> <p id="articulation${classe.idClass}">${classe.articulation}</p></td>
				<td> <p id="active${classe.idClass}">${classe.active}</p></td>
				<td> <button type="button" onclick="join('${classe.idClass}','person','idClass');">➡️</button></td>
				<td> <button type="button" onclick="modifica('${classe.idClass}','Classm');">✏️</button></td>
				<td> <button type="button" onclick="elimina('${classe.idClass}','Classm');">🗙</button></td>	
			</tr>`
		  contentTable += str;
		}
	}
	else if (richiesta.toLowerCase() === "account"){
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
			str = `<tr id="account${account.idAccount}">
			<td> <input type="checkbox" id="${account.idAccount}" name="cancella"></td>
			<td><p id="Nick${account.idAccount}">${account.nick}</p></td>
			<td><p id="Ruolo${account.idAccount}">${account.ruolo}</p></td>
			<td><p id="Valid${account.idAccount}">${account.valid}</p></td>
			<td><p id="DataReg${account.idAccount}">${account.dataReg}</p></td>
			<td><p id="DataExp${account.idAccount}">${account.dataExp}</p></td>
			<td><button type="button" onclick="verifica('${account.idAccount}');">✔️</button></td>
			<td><button type="button" onclick="elimina('${account.idAccount}','Account');">🗙</button></td>	
			</tr>`
		  contentTable += str;
		}
	}
	else if (richiesta.toLowerCase() === "vehicle"){
		headers = ["","Targa", "Tipo", "Proprietario","Persona","",""];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		if (list.length < 1 || list == undefined){
			data = await loadItems("./api/read/vehicle")
		}
		else {
			data = list
		}
		for (const vehicle of data) {
			str = `<tr id= vehicle${vehicle.idV}>
			<td> <input type="checkbox" id="${vehicle.idV}" name="cancella"></td>
			<td><p id="Targa${vehicle.idV}">${vehicle.plate}</p></td>
			<td><p id="Tipo${vehicle.idV}">${vehicle.type}</p></td>
			<td><p id="Proprietario${vehicle.idV}">${vehicle.owner}</p></td>
			<td><button type="button" onclick="join('${vehicle.idPeople}','person');">➡️</button></td>
			<td><button type="button" onclick="modifica('${vehicle.idV}','vehicle',${vehicle.idPeople});">✏️</button></td>
			<td><button type="button" onclick="elimina('${vehicle.idV}','vehicle');">🗙</button></td>	
			</tr>`
		  contentTable += str;
		}
	}
	let stringaBottoneValidAll=``
	if (richiesta.toLowerCase() === "account"){
		stringaBottoneValidAll=`<button type="button" class="btn btn-sm btn-primary" onClick="verifica('',${richiesta});">VALIDA SELEZIONATI</button>`
	}
	console.log(stringaBottoneValidAll)
	let stringaEliminaSelezionati = richiesta.toLowerCase() !== 'entris' ? `<button type="button" class="btn btn-sm btn-primary" onClick="elimina('','${richiesta}');">ELIMINA SELEZIONATI</button>`: ""; 
	let stringaTabella = `
	<table class="table table-sm">
	${tableHeader}
	${contentTable}
	</table>
	${stringaEliminaSelezionati}
	${stringaBottoneValidAll}
	`
	div.innerHTML=stringaTabella;

}

const verifica = async (id) =>{
	console.log(`ingresso in valida`)
	if(id === ""){
		let lista = getCheckedBoxes("cancella");
		console.log(lista)
		const data = await fetch(`./api/validate`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(lista)}
		)
		.then(res => res.json())
		.catch(e => console.error(e));
		let result = data;
		console.log(result);
		tabella("account")
	}
	else{
		let str =`[
			${id}
		]`;
		const data = await fetch(`./api/validate`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str}
		)
		.then(res => res.json())
		.catch(e => console.error(e));
		let result = data;
		console.log(result);
		
		tabella("account")
	}
} 

const canBeHere = () =>{
	let id = sessionStorage.getItem("userId");
	let username = sessionStorage.getItem("username");
	let ruolo = sessionStorage.getItem("ruolo");
	console.log(`id = ${id} username = ${username}`)
	if (id === null && username === null){
		alert("DEVI FARE PRIMA IL LOGIN");
		window.location.href = "./login";
	}
	else if ((username !== "Admin") || (ruolo !== "Admin") || (id !== "1")) {
		alert("NON PUOI ESSERE QUI");
		sessionStorage.clear()
		window.location.href = "./login";
	}
	window.setTimeout("tabella('Account')", 200);
}

window.onload=canBeHere();

const modifica = (id,tipo,idPeople=0,materia="",idClass=0)=>{
	let newRiga = ``;
	let oldriga = null;
	console.trace()
	if (tipo === "person"){
		oldriga = document.getElementById(`person${id}`);
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
			<td><button type="button" onclick="join('${id}','People','idPeople');">➡️</button></td>
			<td><button type="button" onclick="join('${id}','People','idPeople');">➡️</button></td>
			<td> <button type="button" onclick="confermaMod('${id}','person',0,'${materia}',${idClass});">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','person');">🗙</button></td>			
		</tr>`;

	}
	else if (tipo === "phone"){
		console.log("INGRESSO IN TELEFONI")
		oldriga = document.getElementById(`phone${id}`);
		// RECUPERO VALORI DA CONSERVARE
		let oldPrefix = document.getElementById(`prefix${id}`).innerHTML;
		let oldNumber = document.getElementById(`number${id}`).innerHTML;
		console.log(oldriga);

		// FORMATTAZIONE HTML DELLA RIGA
		newRiga= `
		<tr id="phone${id}">
			<td> <input type="checkbox" id="riga${id}" name="cancella"></td>
			<td> <input type="text" id="prefixIn${id}" value="${oldPrefix}" style=" max-width: 150px"></td>
			<td> <input type="text" id="numberIn${id}" value="${oldNumber}" style=" max-width: 150px"></td>
			<td> <button type="button" onclick="confermaMod('${id}','Phone',${idPeople});">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','Phone');">🗙</button></td>			
		</tr>`;
		if(idPeople<=0){
			alert("Errore nella modifica")
			return;
		}

	}
	else  if (tipo === "vehicle"){
		oldriga = document.getElementById(`vehicle${id}`);
		// RECUPERO VALORI DA CONSERVARE
		let oldTarga = document.getElementById(`Targa${id}`).innerHTML;
		let oldTipo = document.getElementById(`Tipo${id}`).innerHTML;
		let oldProprietario = document.getElementById(`Proprietario${id}`).innerHTML;
		console.log(oldriga);
		
		// FORMATTAZIONE HTML DELLA RIGA
		newRiga= `
		<tr id="person${id}">
			<td> <input type="checkbox" id="riga${id}" name="cancella"></td>
			<td> <input type="text" id="targaIn${id}" value="${oldTarga}" style=" max-width: 150px"></td>
			<td> <input type="text" id="tipoIn${id}" value="${oldTipo}" style=" max-width: 150px"></td>
			<td> <input type="text" id="proprietarioIn${id}" value="${oldProprietario}" style=" max-width: 180px"></td>
			<td><button type="button" onclick="join('${id}','People','idPeople');">➡️</button></td>
			<td> <button type="button" onclick="confermaMod('${id}','Vehicle',${idPeople});">✔️</button></td>
			<td> <button type="button" onclick="elimina('${id}','Vehicle');">🗙</button></td>			
		</tr>`;
		if(idPeople<=0){
			alert("Errore nella modifica")
			return;
		}

	}
	else if (tipo === "Classm"){
		
		oldriga = document.getElementById(`class${id}`);
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

	}
	else if (tipo === "Account"){
		console.log("INGRESSO EFFETTUATO")
		oldriga = document.getElementById(`account${id}`);
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

	}
	//INSERIMENTO DELLA NUOVA RIGA
	oldriga.innerHTML=newRiga;

}

const confermaMod = async (id,tab,idPeople=0,materia="",idClass=0) =>{
	console.log(`INGRESSO IN CONFERMAMOD ${tab}`)
	let str;
	if (tab === "person"){
		//SET VALORI
		
		let varnome = document.getElementById(`nomeIn${id}`).value;
		let varcognome = document.getElementById(`cognomeIn${id}`).value; 
		let varCf = document.getElementById(`cfIn${id}`).value;
		let varGender = document.getElementById(`genderIn${id}`).value;
		let varEmail = document.getElementById(`emailIn${id}`).value;
		let varDataNascita = document.getElementById(`birthdayIn${id}`).value;
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
		console.log(materia)
		if(materia==="" && idClass<=0){
			str = `{
				"name" : "${varnome}",
				"surname" : "${varcognome}",
				"cF" : "${varCf}",
				"gender" :"${varGender}",
				"email" : "${varEmail}",
				"birthday" : "${varDataNascita}"
			}`;
		}
		else if(materia==="" && idClass>0){
			str = `{
				"name" : "${varnome}",
				"surname" : "${varcognome}",
				"cF" : "${varCf}",
				"gender" :"${varGender}",
				"email" : "${varEmail}",
				"birthday" : "${varDataNascita}",
				"idClass" :${idClass}
			}`;
		}
		else if(materia!=="" && idClass<=0){
			str = `{
				"name" : "${varnome}",
				"surname" : "${varcognome}",
				"cF" : "${varCf}",
				"gender" :"${varGender}",
				"email" : "${varEmail}",
				"birthday" : "${varDataNascita}"
				"idClass" :${idClass},
				"sub" : ${materia}
			}`;
		}
		//INVIO

		console.log(str)

		
	}
	else if (tab === "Phone"){
		//SET VALORI
		let varPref = document.getElementById(`prefixIn${id}`).value;
		let varNumber = document.getElementById(`numberIn${id}`).value;
		
		// CONTROLLI
		if (idPeople<=0){
			alert("Errore nella modifica")
			return
		}
		else if(varPref === "" || varNumber === ""){
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
			"idPeople" : ${idPeople}
		}`;
		console.log(str)

	}
	else if (tab === "Vehicle"){
		//SET VALORI
		let varTarga = document.getElementById(`targaIn${id}`).value;
		let varTipo = document.getElementById(`tipoIn${id}`).value; 
		let varProp = document.getElementById(`proprietarioIn${id}`).value;
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
			"idPeople" : ${idPeople}
		}`;
		//INVIO

		console.log(str)
	}
	else if (tab === 'Classm'){
		console.log(`INGRESSO IN IF ${tab}`)

		//SET VALORI
		
		let varAnno = document.getElementById(`yearIn${id}`).value;
		let varSezione = document.getElementById(`carrelIn${id}`).value ;
		let varArticolazione = document.getElementById(`articulationIn${id}`).value;
		let varAttivo = document.getElementById(`activeIn${id}`).value;
		
		// CONTROLLI
		if ( varAnno === "" || varSezione === "" || varArticolazione === "" || varAttivo === ""){
			alert("campi vuoti");
			return
		}
		if (typeof varAnno !== 'number' && Number.isNaN(varAnno)) {
			alert("anno non valido")
			return
		}
		else if (varAttivo !== "YES" && varAttivo !== "NO" ){
			alert("errore inserimento validita' ");
			return
		}
		// FORMATTAZIONE JSON
		str = `{
			"year" : "${varAnno}",
			"carrel" : "${varSezione}",
			"articulation" : "${varArticolazione}",
			"active" : "${varAttivo}"
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
	tabella(tab);
}

const elimina = async (id="",tab) =>{
	console.log(`ingresso in elimina ${tab}`)
	if (id === "") {
		let lista = getCheckedBoxes("cancella");
		console.log(lista)
		if(id == 1 && tab =="account"){
			alert("NON PUOI ELIMINARE L'ADMIN")
		}
		else{
			const data = await fetch(`./api/delete/${tab}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(lista)}
			)
			.then(res => res.json())
			.catch(e => console.error(e));
			let result = data;
			console.log(result);
			tabella(tab)
			}
		}
		else {
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
	divFiltro.style.display="block";
	let strDiv;
	
	strDiv = `
			<div class="mb-3" >
				<h4>
					<label for="filter" class="form-label " >${strOut}</label>
				</h4>
				<input type="text" class="form-control" id="filter" placeholder="Insert ${campo}" required>
			</div>`;
	strDiv+=`<button type="button" onclick="filtra('${tab}','${campo}');">🔎</button>`;
	divFiltro.innerHTML=strDiv;
}

const filtra = async (tab,campo)=>{
	let filterData = document.getElementById("filter").value;
	let str = `{
		"${campo}":"${filterData}"
	}`
	let data = await fetch(`./api/filter/${tab}`, {
		method: 'PUT',
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
	if (tab === "Person"){
		tab="People"
	}
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
	console.log(`${checkboxesChecked}`)
	return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

const join = async (id,tabArrivo,campo="idPeople") =>{
	let str = `{
		"${campo}":${id}
	}`;
	let data = await fetch(`./api/filter/${tabArrivo}`, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
	tabella(tabArrivo,data);
}

const sortString=(a, b) => {
	const nameA = a.name.toUpperCase(); // ignore upper and lowercase
	const nameB = b.name.toUpperCase(); // ignore upper and lowercase
	if (nameA < nameB) {
	  return -1;
	}
	if (nameA > nameB) {
	  return 1;
	}
  
	// names must be equal
	return 0;
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