//project.js
'use strict'


import CableReady from 'cable_ready'
console.log('Entered project.js file!!!');

//let wsUri = "ws://echo.websocket.org/";
//let wsUri = "ws://localhost:8003/ws/cr-sync/";
let wsUri = "ws://localhost:8000/ws"
let output;

let websocket = new WebSocket(wsUri);
function init() {
  output = document.getElementById("output");
  testWebSocket();
}

function testWebSocket() {
  websocket.onopen = function(evt) {
    onOpen(evt)
  };
}

function onOpen() {
  const uriString = "CONNECTED TO:  " + wsUri;
  writeToScreen(uriString);
  document.getElementById("output").className = 'text-green';
}

function writeToScreen(string) {
  document.getElementById("output").innerHTML = string;
}

websocket.onmessage = (e) => {
    //let result = JSON.parse(e.data).expression;
    let result = JSON.parse(e.data);
    if (result.expression) {
        document.getElementById("results").value += "Server: " + result.expression + "\n";
    }
    else {
        document.getElementById("bar-width").innerHTML = result.setAttribute[0].value;
        CableReady.perform(result);
    }
}

websocket.onclose = () => {
    console.log("Socket closed!");
}

document.querySelector('#expression').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#submit ').click();
    }
};

document.querySelector("#submit").onclick = () => {
    let inputfield = document.querySelector("#expression");
    let expression = inputfield.value;
    websocket.send(JSON.stringify(
        {
            expression: expression
        }
    ))
    document.querySelector("#results").value += "You: " + expression + "\n";
    inputfield.value = "";
}

function sleepFor(sleepDuration){
    let now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){
        /* Do nothing */
    }
}

function sleepThenAct(){
    sleepFor(50);
    console.log("Hello, JavaScript sleep!");
}

document.querySelector("#load-bar").onclick = () => {
    //sleepThenAct();
    document.getElementById("bar-width").innerHTML = 'width: 10%';
    let messageToServer = 'yes';
    websocket.send(JSON.stringify(
        {
            loadprogreesbar: messageToServer
        }
    ));
    console.log('Message to server send!')
}

document.querySelector("#reset-bar").onclick = () => {
    //document.getElementById("progress-bar").style.width = "10%";
    document.getElementById("bar-width").innerHTML = 'width: 10%';
    CableReady.perform({setAttribute: [{selector: "#progress-bar", name: "style", value: "width: 10%"}]});
    console.log('Initial bar width set by CR')
}

window.addEventListener("load", init, false);

//let payload = {setAttribute: [{selector: "#progress-bar", name: "style", value: "width: 60%"}]}
//let payloadComplete = {"identifier": "{\"channel\":\"StimulusReflex::Channel\"}", "type": "message", "cableReady": true, "operations": {"setAttribute": [{"selector": "#progress-bar", "name": "style", "value": "width: 110%"}]}}
//CableReady.perform(payload);
