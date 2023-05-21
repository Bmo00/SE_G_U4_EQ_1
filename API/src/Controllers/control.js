const services = require('../Services/service')

const insertSensorRecord = async function(req,res){
    const { body } = req;
    if (
        !body.id_sensor ||
        !body.valor_actual ||
        !body.fecha_record    
    ) {        
        res.status(400)
           .send({
            status:"Error", data:{
                error:"Faltan datos"}
            })
        return 
    }
    const newSensor = {
        id_sensor: body.id_sensor,
        valor_actual: body.valor_actual, 
        fecha_record: body.fecha_record       
    };

    const resultado = await services.insertSensorRecord(newSensor)
    
    res
    .setHeader('content-type', "application/json")
    .status(200)
    .send(resultado)

}

const getAll_Records = async function(req,res){
    const resultado = await services.getAll_Records()
    res.status(200).send(resultado)
}

module.exports = {
    insertSensorRecord,
    getAll_Records
}
