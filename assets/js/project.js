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

function onOpen(evt) {
  const uriString = "CONNECTED TO:  " + wsUri;
  writeToScreen(uriString);
  document.getElementById("output").className = 'text-green';
}

function writeToScreen(string) {
  document.getElementById("output").innerHTML = string;
}

websocket.onmessage = (e) => {
    //result = JSON.parse(e.data).result;
    let result = JSON.parse(e.data).expression;
    document.getElementById("results").value += "Server: " + result + "\n";
}

websocket.onclose = (e) => {
    console.log("Socket closed!");
}

document.querySelector('#expression').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#submit ').click();
    }
};

document.querySelector("#submit").onclick = (e) => {
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

window.addEventListener("load", init, false);



CableReady.perform('morph')

