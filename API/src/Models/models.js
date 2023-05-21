const {getConnection} = require('./conexion')
const sql = require('mssql')


const InsertSensorRecord = async function(id_sensor, valor_actual, fecha_record) {
    console.log("id_sensor:", id_sensor, "valor_actual:", valor_actual, "fecha_record:", fecha_record);
  
    try {
      const conexion = await getConnection();
  
      if (!conexion) {
        throw new Error("No se ha podido conectar con la base de datos.");
      }
  
      const result = await conexion
        .request()
        .input("id_sensor", sql.Int, id_sensor)
        .input("valor_actual", sql.Int, valor_actual)
        .input("fecha_record", sql.DateTime, fecha_record)
        .execute("InsertSensorRecord");
  
      return "{\"Resultado\": \"Insercion Correcta\"}";
    } catch (error) {
      console.error("Ha ocurrido un error:", error.message);
    }
  };
  

const GetAllSensorRecords = async function(){    
    const conexion = await getConnection()
    const result = await conexion
    .request().execute('GetAllSensorRecords')
    //console.log(result.recordset)
    return result.recordset
} 
 
module.exports = {
    InsertSensorRecord,
    GetAllSensorRecords
}
