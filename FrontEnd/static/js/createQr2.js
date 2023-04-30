'use strict';
let nQr =0;

const loadItems = async (url) =>{ await fetch(url)
    .then(res => res.json())
    .catch(e => console.error(e));
}

const createQR = async () => {
    if (nQr===0) {
        let id=sessionStorage.getItem("userId");
        //f"""abch!"iu"!"id"!ghgj!"gk"!"data"!fgdgd"""
        let gk = null;
        try {
            let dato = loadItems(`./api/gk/${id}`);
            gk = dato.gk;
        } catch (error) {
            console.log("ERRORE NELLA GK");
        }
        const now = Date.now();
        let stringone=`!${id}!${keyIMPORTANTE()}!${gk}!${now}!${keyIMPORTANTE()}`;
        console.log(stringone);
        let qrcodeContainer = document.getElementById("qrcode");
        new QRCode(qrcodeContainer, stringone);
        nQr+=1;
        setTimeout(eliminaQR, 3 * 1000);
    }
};

const eliminaQR = () => {
    alert('Hello after 4 seconds');
    document.getElementById("qrcode").innerHTML="";
    nQr=0;
};


const keyIMPORTANTE=()=> {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < 5) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}
