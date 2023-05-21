const express = require('express')

const controlador = require('../Controllers/control')

const router = express.Router()

router

.get('/registros', controlador.getAll_Records)

.post('/', controlador.insertSensorRecord)

module.exports = router
