'use strict';
let nQr =0;




const createQR = async () => {
    if (nQr===0) {
        let id=sessionStorage.getItem("userId");
        //f"""abch!"iu"!"id"!ghgj!"gk"!"data"!fgdgd"""
    
        let dato = await loadItems(`./api/gk/${id}`);
        let gk = dato.gk;
        
        let now = new Date();


        //'%y/%m/%d %H:%M:%S'
        let dataFin = `${now.getFullYear()}/${now.getMonth()+1}/${now.getDate()} ${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`
        let stringone=`!${id}!${keyIMPORTANTE()}!${gk}!${dataFin}!${keyIMPORTANTE()}`;
        let qrcodeContainer = document.getElementById("qrcode");
        new QRCode(qrcodeContainer, stringone);
        nQr+=1;
        setTimeout(eliminaQR, 600000);
    }
};

const eliminaQR = () => {
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
