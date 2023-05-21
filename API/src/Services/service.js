const bd = require("../Models/models")

const insertSensorRecord = async function(JsonObj){
    id = JsonObj.id_sensor
    valor_actual = JsonObj.valor_actual
    fecha_record = JsonObj.fecha_record
    const resp = await bd.InsertSensorRecord(id, valor_actual, fecha_record)
    return resp
}


const getAll_Records = async function(){
    const resp = await bd.GetAllSensorRecords()
    return resp
}

module.exports = {
    insertSensorRecord,
    getAll_Records
}
