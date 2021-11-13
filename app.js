const express = require('express');
const app = express();
const {exec} = require('child_process')
const fs = require('fs')

const uploadImage = require('./middlewares/uploadImage')

const cors = require('cors')
const corsOptions = {
    origin: '*',
    methods: ['GET', 'POST', 'PUT']

};

app.use(cors(corsOptions));

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.get('/', function(req,res) {
  res.send("Nandish vasant server")
})

app.post('/api/maleria', uploadImage.single('maleria'), function(req, res) {
  if(req.file === undefined){  
    console.log("Image not found!")
    return res.send({
        success: false,
        code: 400,
        message: null
    })
  }

  try{
      var child = exec('python3 ' + __dirname + '/Malarial/backendScript.py ' + req.file.filename)
      child.stdout.on('data', (data) => res.send({
        success: true,
        code: 200,
        message: "Operation successful",
        response: JSON.parse(data)
    }))
  } catch (err) {
      console.log(err)
      return res.send({
          success: false,
          code: 502,
          message:'Internal server error'
      })
  }
});

app.post('/api/size', uploadImage.single('size'), function(req, res) {
  if(req.file === undefined){  
    console.log("Image not found!")
    return res.send({
        success: false,
        code: 400,
        message: null
    })
  }

  console.log("excuting script")

  try{
      console.log('python3 ' + __dirname + '/Malarial/backendScript2.py ' + req.file.filename)
      var child = exec('python3 ' + __dirname + '/Malarial/backendScript2.py ' + req.file.filename)
      child.stdout.on('data', (data) => res.send({
        success: true,
        code: 200,
        message: "Operation successful",
        response: JSON.parse(data)
    }))
  } catch (err) {
      console.log(err)
      return res.send({
          success: false,
          code: 502,
          message:'Internal server error'
      })
  }
});


app.get('/images/:img', function (req, res) {
  const pathToImg = __dirname + '/Malarial/images/'+ req.params.img
  try{
      if(!fs.existsSync(pathToImg)) return res.send({
          success: false,
          status: 404,
          message: "File not found",
          response: "Invalid path to file or file does not exist"
      })

      return res.sendFile(pathToImg)
  } catch (err) {
    console.log(err)
      return res.send({
          success: false,
          status: 500,
          message: "Internal server error",
          response: null
      })
  }
},)

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  return res.send("404 - Not found")
});

const PORT = 9000
app.listen(PORT, () => console.log(`Listening on port ${PORT}`))

module.exports = app;
