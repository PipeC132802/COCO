
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