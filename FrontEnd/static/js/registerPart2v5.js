const canBeHere = () =>{
	let id = sessionStorage.getItem("userId");
	let username = sessionStorage.getItem("username");
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
	let id = sessionStorage.getItem("userId");
    if (id === null){
        alert ("necessario prima il login");
    }
	else if(prefissoTel.substring(0,0) === "+"){
		alert("PREFISSO NON VALIDO");
	}
	else {
		let jsonDataTelefono=`{
			"number" : "${telNum}",
			"prefix" : "${prefissoTel}"
		}`;
		let jsonDataVeicolo = `{
			"type" : "${tipo}",
			"plate" : "${targa}",
			"owner" : "${proprietario}"
		}`;
		verify(jsonDataTelefono,jsonDataVeicolo,id);
	}
};


const verify = async (jsonDataTelefono,jsonDataVeicolo,idUser=0) => {

		let str = `{
			"phone" : ${jsonDataTelefono },
			"vehicle" :${ jsonDataVeicolo}
		}`
		const data = await fetch(`./api/reg2/${idUser}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: str
		}
	)
	.then(res => res.json())
	.catch(e => console.error(e));
    let result = data;
	if (result.success === false){
		alert(result.message)
	}
	else{
		window.location.href = "./profile";
	}
}

const getValueRadio = (id) => {
	var radios = document.getElementsByName(id);
	for (var i = 0, length = radios.length; i < length; i++) {
		if (radios[i].checked) {
			return radios[i].value;
		}
	}
};