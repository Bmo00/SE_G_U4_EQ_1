const sql = require('mssql');

const config = {
    user: 'sa',
    password: 'willy',
    server: 'localhost',
    database: 'proyecto',
    options: {
        encrypt: true,
        trustServerCertificate: true
    }
};

const getConnection = async function () {
    try {
        const conexion = await sql.connect(config);
        console.log('Conexion exitosa');
        return conexion;
    } catch (error) {
        console.log(error);
    }
};


async function testConnection() {
    try {
        const connection = await getConnection();

    } catch (error) {
        console.log('Ha ocurrido un error:', error.message);
    }
}

testConnection();

module.exports = {
    getConnection
}
