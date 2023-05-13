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


const tabella = async (richiesta) => {
	let div = document.getElementById("divTabellone");
    let headers = null;
	let data;
	let result;
	let tableHeader = ``;
	let contentTable = ``;
	if (richiesta === "People"){
		headers = ["Name", "Surname", "CF", "Gender", "Email", "Birthday"];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		data = await loadItems("./api/read/person")
		for (const person of data) {
			str = `<tr>
			<td>${person.name}</td>
			<td>${person.surname}</td>
			<td>${person.cf}</td>
			<td>${person.gender}</td>
			<td>${person.email}</td>
			<td>${person.birthday}</td>
		  </tr>`
		  contentTable += str;
		}
	}
	else if (richiesta === "Classm"){
		headers = ["Year", "Carrel", "Articulation"];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		data = await loadItems("./class")
		for (const classe of data) {
			str = `<tr>
			<td>${classe.Year}</td>
			<td>${classe.Carrel}</td>
			<td>${classe.Articulation}</td>
			</tr>`
		  contentTable += str;
		}
	}
	else if (richiesta === "Account"){
		headers = ["Nick", "Ruolo", "Validità","Data Registrazione","Data Eliminazione"];
		for (const elem of headers) {
			console.log(`elemento = ${elem}`);
			str = `<th scope="col">${elem}</th>`;
			tableHeader += str;
		}
		data = await loadItems("./api/read/account")
		for (const account of data) {
			str = `<tr>
			<td>${account.Nick}</td>
			<td>${account.Ruolo}</td>
			<td>${account.valid}</td>
			<td>${account.DataReg}</td>
			<td>${account.DataExp}</td>
			</tr>`
		  contentTable += str;
		}
	}
	let stringaTabella = `<table class="table table-sm">
	${tableHeader}
	${contentTable}
	</table>`
	div.innerHTML=stringaTabella;

}

