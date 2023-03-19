'use strict';

const switchRole = (ruolo) => {
    let container = document.getElementById("classOrSub");
	if (ruolo === `doc`){
        container.innerHTML=`
            <h4>
                <label for="subInput" class="form-label" >Materia</label>
            </h4>
            <input type="text" class="form-control" id="subInput"  placeholder="Insert subject" required>
        `
    }
    else{
        container.innerHTML=`
        <h4>    
            <label for="classInput" class="form-label" >Classe</label>
        </h4>
            <input type="text" class="form-control" id="classInput"  placeholder="Insert class" required>
        `
    }
}



const control = async () => {
    let nome= document.getElementById("nomeInput").value;
    let cognome= document.getElementById("cognomeInput").value;
    let cf= document.getElementById("cfInput").value.length === 16 ? document.getElementById("cfInput").value: null;
    let DataN= document.getElementById("dateInput").value;
    let email= document.getElementById("emailInput").value;
    let ruolo = getValueRadio("ruolo");
    let genere = getValueRadio("gender");
    let classe = ruolo==="doc" ? null : document.getElementById("classInput").value;
    let materia = ruolo==="doc" ? document.getElementById("subInput").value : null;
	let nickname= document.getElementById("nicknameInput").value;
    let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
    let today = new Date();
    if(cf === null){
        alert("CF NON VALIDO");
    }
    else if (DataN > today){
        alert("CF NON VALIDO");
    } 
    else {
        let jsonDataPerson=`{
            "name" : ${nome},
            "surname" : ${cognome},
            "classm" : ${classe},
            "cf" : ${cf},
            "gender" : ${genere},
            "email" : ${email},
            "birthday" : ${DataN},
            "sub" : ${materia}
        }`

        let jsonAccount = `{
            "nickname" : ${nickname},
            "password" : ${password}
        }`;
        console.log(`json Persone= ${jsonDataPerson}\njson Account = ${jsonAccount}`);
        verify(jsonDataPerson,jsonAccount)
    }
};


const verify = async (jsonPerson,jsonAccount) => {
    const data = await fetch(`./api`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "People": jsonPerson,
                "account" : jsonAccount
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
            break;
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


