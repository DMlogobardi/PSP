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
    let userId = sessionStorage.getItem("username");
	console.log(`prefisso =${prefissoTel} substring = ${prefissoTel.substring(0, 1)} `)
    if (userId === null){
        alert ("necessario prima il login");
    }
	else if(prefissoTel.substring(0,0)){
		alert("PREFISSO NON VALIDO");
	}
	else {
		let jsonDataTelefono=`{
			"number" : "${telNum}",
			"prefix" : "${prefissoTel}"
		}`;
		let jsonDataVeicolo = `{
			"Type" : "${tipo}",
			"Plate" : "${targa}",
			"Owner" : "${proprietario}"
		}`;
		console.log(`{"phone" : ${jsonDataTelefono}\n  "vehicle" : ${jsonDataVeicolo}}`);
		verify(jsonDataTelefono,jsonDataVeicolo,userId);
	}
};


const verify = async (jsonDataTelefono,jsonDataVeicolo,idUser=0) => {

		const data = await fetch(`./api/reg2/${idUser}}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				"phone" : jsonDataTelefono,
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
}

const getValueRadio = (id) => {
	var radios = document.getElementsByName(id);
	for (var i = 0, length = radios.length; i < length; i++) {
		if (radios[i].checked) {
			console.log(radios[i].value);
			return radios[i].value;
		}
	}
};