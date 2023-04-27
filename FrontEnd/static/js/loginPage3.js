'use strict';

// print items on Html page
const control = async () => {
	let nickname= document.getElementById("nicknameInput").value;
    let password= CryptoJS.SHA256(document.getElementById("passwordInput").value);
    console.log(`nick= ${nickname}, password=${password}`);
    verify(nickname,password);
};


const verify = async (nickname,password) => {
    const data = await fetch(`./api/log/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify( {
                    "Nick": `${nickname}`,
                    "Pass" : `${password.toString()}`
                }
            )
        }
    )
    .then(res => res.json())
    .catch(e => console.error(e));
    let result= data
    console.log(result)
    if (result.hasOwnProperty('userId')){
        sessionStorage.setItem("userId",result.userId);
        sessionStorage.setItem("username",result.username);
    }
    else
        alert(result.message)
};



const showPwd = async () => {
	var input = document.getElementById('passwordInput');
        if (input.type === "password") 
          input.type = "text";
        else 
          input.type = "password";
};

const changeWin = async (data) => {
	if (data.success === true)
        window.location.href = "./qr";
};
