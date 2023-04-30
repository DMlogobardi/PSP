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
	let tipo = getValueRadio("tipoVeicolo");
	let targa = document.getElementById("targaInput").value;
    let proprietario =document.getElementById("propInput").value;
	let prefissoTel = document.getElementById("prefInput").value;
	let telNum = document.getElementById("numInput").value;
    let userId = null;
    try {
        let userId = sessionStorage.getItem("userId");
    } catch (error) {
        console.log("ID NON PRESENTE")
    }

    if (userId === null){
        alert ("necessario prima il login");
    }
	else if(prefissoTel.substring(0, 1)){
		alert("PREFISSO NON VALIDO");
	}
	else {
		let jsonDataTelefono=`{
			"number" : "${telNum}",
			"prefix" : "${prefissoTel}",
			"idPeople" : "${userId}"
		}`;
		let jsonDataVeicolo = `{
			"Type" : "${tipo}",
			"Plate" : "${targa}",
			"Owner" : ${proprietario},
			"idPeople" : ${userId}
		}`;
		console.log(`json Telefono= ${jsonDataTelefono}\njson Account = ${jsonDataVeicolo}`);
		verify(jsonDataTelefono,jsonDataVeicolo,idUser);
	}
};


const verify = async (jsonDataTelefono,jsonDataVeicolo,idUser=0) => {

		const data = await fetch(`./api/reg2/${idUser}}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"phone": jsonDataTelefono,
				"vehicle" : jsonDataVeicolo
			})
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
    let result = data;
	console.log(result);
	if (result.success === false){
		alert(result.message)
	}
	/*
	{
		success:booleano
		message:""
	}	
	*/ 
}



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