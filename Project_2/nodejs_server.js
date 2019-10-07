/*******************************************************************************************************
 * File Name: Project1.py
 * Description: This code implements NodeJs Server. It conncects to SQL database and returns entry as per
 * query received through websocket as JSON string
 * Date: 09/23/2019
 * References: https://www.w3schools.com/
 * 
 * ****************************************************************************************************/
var mysql = require('mysql');
const http = require('http');
const WebSocketServer = require('websocket').server;

USER="satya"
PASWWD="satya123"
DATABASE="example"
TABLE="environment"

//HTTP server
const server = http.createServer();
server.listen(9898);

//Websocket server
const wsServer = new WebSocketServer({
    httpServer: server
});

//Connector for mysql database
var con = mysql.createConnection({
  host: "localhost",
  user: USER,
  password: PASWWD,
  database: DATABASE
});

//Connection attempt to mysql
con.connect(function(err) {
	if (err) throw err;
	console.log("Connected!");
}); 

//Connection request from websocket client
wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    
    connection.on('message', function(message) {
      if(message.utf8Data == "Refresh") {
	con.query("SELECT * FROM environment ORDER BY id DESC LIMIT 1", function (err, result, fields) {
		if (err) throw err;
		var send_json = JSON.stringify(result);
		connection.sendUTF(send_json);
	});
      }
      else if(message.utf8Data == "Table") {
	con.query("SELECT * FROM environment ORDER BY id DESC LIMIT 10", function (err, result, fields) {
		if (err) throw err;
		var send_json = JSON.stringify(result);
		connection.sendUTF(send_json);
	});
      }
    });
    
    //Client Disconnected
    connection.on('close', function(reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});


