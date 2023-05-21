const express = require('express')
const ruta = require('./Routes/routes')

const app = express()
const PORT = process.env.PORT || 3000;
app.use(express.json())

app.use("/api", ruta)


app.get("/",(req,res)=>{
    res.send(`<h1>Proyecto final Equipo 1</h1>`)
})

app.listen(PORT, function(){ //()=>{  //funcion flecha
    console.log(`Servidor escuchando en el Puerto: ${PORT}`);
}) 