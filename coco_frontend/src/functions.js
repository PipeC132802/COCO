
export function sendNotificationViaWS(sockedData, wsBase, channel) {
    let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
    var websocket = new WebSocket(
        protocol + wsBase + "/ws/notifications/" + channel + "/"
    );
    websocket.onopen = () => websocket.send(JSON.stringify(sockedData));
    websocket.onmessage = ({ data }) => {
        websocket.close();
    };
}

var CryptoJS = require("crypto-js");
export function encrypt(msg, value2Key) {
    var key = CryptoJS.SHA256(value2Key.toString()); //hashing the key using SHA256
    var encryptedString = CryptoJS.AES.encrypt(msg.toString(), key.toString()).toString();
    return encryptedString;
}

export function decript(value2Key, msgEncrypted) {
    var key = CryptoJS.SHA256(value2Key).toString();
    var bytes = CryptoJS.AES.decrypt(
        msgEncrypted,
        key
    );
    var originalText = bytes.toString(CryptoJS.enc.Utf8);
    return originalText;
}