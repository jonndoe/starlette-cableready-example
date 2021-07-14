import { createConsumer } from "@rails/actioncable"


console.log('Entered ruby-ws-conn.js');


//This will ready a consumer that'll connect against /cable on ' +
//'your server by default. The connection won't be established until
//you've also specified at least one subscription you're interested in having.
//export default createConsumer()
//createConsumer();


// Specify a different URL to connect to
createConsumer('https://ws.example.com/cable')

let consumer = createConsumer();
consumer.subscriptions.create({ channel: "ChatChannel", room: "Best Room" });

// Use a function to dynamically generate the URL
//createConsumer(getWebSocketURL)

//function getWebSocketURL {
//  const token = localStorage.get('auth-token')
//  return `https://ws.example.com/cable?token=${token}`
//}