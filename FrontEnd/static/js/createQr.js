'use strict';
let nQr =0;

const createQR = async () => {
    if (nQr===0) {
        let id=212
        const timeElapsed = Date.now();
        let stringone=`${id}${timeElapsed}`;
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
  
