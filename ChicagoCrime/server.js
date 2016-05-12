// server.js

// BASE SETUP
// =============================================================================

var express    = require('express');        // call express
var app        = express();         // define our app using express
var bodyParser = require('body-parser');
var http = require('http');
var server = http.createServer(app);
var io = require('socket.io').listen(server);
var port = process.env.PORT || 8080;        // set our port

//--------------
// START THE SERVER

server.listen(port);
console.log('Magic happens on port ' + port);
           
//configure app to use bodyParser()
//this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));

// ROUTES FOR OUR API
require('./app/routes/routes.js')(app,io);



    
    
    
    
    

