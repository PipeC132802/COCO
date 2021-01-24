
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

export function codeLetters2Numbers(word){
   let array = word.split()
   let output = "";
   for (let index = 0; index < array.length; index++) {
       output += word.codePointAt(index);
   }
   return output
}