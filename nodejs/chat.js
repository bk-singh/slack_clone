ITS OK SLEEP PEACEFULLY
I ll take care.. :)





var http = require('http'); //server req.
var connect = require('connect');
var app = connect().use(function(req, res){res.setHeader("Access-Control-Allow-Origin", "http://58019769.ngrok.io");});
var server = http.createServer(app).listen(4000); //server config
var io = require('socket.io').listen(server); //socket.io .. a async network package.. read more about it in google
var cookie_reader = require('cookie'); // to access stored cookie .. i.e sessionid 
var querystring = require('querystring'); // dontknoe .. ll come back after finfiding the full code
 
var redis = require('redis'); //database req.
var sub = redis.createClient(); //connection to redis db
 
//Subscribe to the Redis chat channel
sub.subscribe('chat'); // like collections in mogo..
 
//Configure socket.io to store cookie set by Django

io.sockets.on('connection', function (socket) {
    socket.on('create', function(room) {
        socket.join(room);
      });

    //Grab message from Redis and send to client    
    //Client is sending message through socket.io
    socket.on('send_message', function (message) {
        var message1 = message.split("~");
        var chnl = message1[0];
        message1.shift();
        console.log(message1);
        values = querystring.stringify({
            comment: message1.toString(),
            channel: chnl,
        });
        
        var options = {
            host: 'http://58019769.ngrok.io/',
            path: '/node_api',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };
        
        //Send message to Django server
        var req = http.request(options, function(res){
            res.setEncoding('utf8');
            
            //Print out error message
            res.on('data', function(message){
                if(message != 'Everything worked :)'){
                    console.log('Message: ' + message);
                }
            });
        });
        
        req.write(values);
        req.end();
    });
});

sub.on('message', function(channel, message){
    var message1 = message.split("~");
    var chnl = message1[0];
     message1.shift();
    io.sockets.in(chnl).emit('message', message1.toString());
});