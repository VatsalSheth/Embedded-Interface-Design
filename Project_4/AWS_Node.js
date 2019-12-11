/*******************************************************************************************************
 * File Name: AWS_Node.js
 * Description: This code implements AWS SQS reads and updates MySQL
 * Date: 12/11/2019
 * References: https://www.w3schools.com/
 * 
 * ****************************************************************************************************/


var mysql = require('mysql');
var AWS = require('aws-sdk');
var util = require('util')
const fs = require('fs');

AWS.config.update({region:'us-east-1'})

// Create an SQS service object
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

var queueURL = "https://sqs.us-east-1.amazonaws.com/996000685317/wand_queue";
var params = {                                                                //Setting attributes
 MaxNumberOfMessages: 1,
 QueueUrl: queueURL,
 VisibilityTimeout: 1,
 AttributeNames: [
    "SentTimestamp"
 ],
 MessageAttributeNames: [
    "All"
 ]
};

params_s = {
  QueueUrl: queueURL,
  AttributeNames: ['ApproximateNumberOfMessages']
};

params_length = {
  QueueUrl: queueURL,
  AttributeNames: ['ApproximateNumberOfMessages']
};

USER="vatsal"
PASWWD="12345"
DATABASE="Magic_Wand"
TABLE="Stats"


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
  setInterval(sqs_receive, 3000);
  //sleep(3000)
	//sqs_receive();
}); 



//Function to create a table of the latest value in the wand_queue.
function sqs_receive()
{  
    sqs.getQueueAttributes(params_s, function(err, data) {

    if (err) console.log(err, err.stack); // an error occurred

    else 
    {
      var i = data.Attributes.ApproximateNumberOfMessages;
      console.log(i);
      if(i <= 0 )      
      {
        
      }
      else
      {
      while(i > 0)
      {
        console.log("In while loop");
        //Receiving message from queue named queue
        sqs.receiveMessage(params, function(err, data) {
        if (err)
        {
          console.log("Receive Error", err);
        }
        else if (data.Messages)
        {
          
          console.log(data.Messages.length);    
          if (data.Messages.length === 0)
          {
            console.log("No new data available");
        
          }
          else
          {
            console.log("Message Received");
            
            var data_body = data.Messages[0].Body;                                               //Accessing Body
            var data_value = data.Messages[0].MessageAttributes.name.StringValue;                //Acessing String value for Attribute
          
            
            console.log("Body Message: " + data_body);
            console.log("Value Message: " + data_value);
            var sql = "INSERT INTO Stats (Command, Status) VALUES ('%s', '%s')"
            var result = util.format(sql,data_body, data_value);
            con.query(result, function (err, result) {
                if (err) throw err;
                console.log("1 Record inserted");
              });
                
            
            
            //Setting attribute to delete a message from the "wand_queue" queue
            var deleteParams = {
              QueueUrl: queueURL,
              ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            
            //Deleting message from the queue.
            sqs.deleteMessage(deleteParams, function(err, data) {
              if (err) {
                console.log("Delete Error", err);
              } else {
                console.log("Message Deleted", data);
              }
            });
          }
        }
         }); 
          i--;
       }
    }
  }
  });
}

