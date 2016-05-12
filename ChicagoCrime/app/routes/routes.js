
var path = require('path');
var fs = require('fs');
var moment = require('moment');
var http = require('http');



module.exports = function(app,io) {

    app.get('/api/getData/:category', function(req, res) {

        fs.readFile(req.params.category+".csv",'ascii',function(err,data){
        if (err) 
        {
            res.send(err);
        }
        res.send(data);
        });
    });


    app.get('/api/getCrimeInfo/:date', function(req,res){



    }    
 
     app.get('/',function(req,res,next){    
        res.sendFile("index.html",{ root: path.join(__dirname, '/../../public/dashboard') });
    });


    
        
};