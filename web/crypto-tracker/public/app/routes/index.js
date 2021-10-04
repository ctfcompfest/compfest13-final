const express = require('express')
const router = express.Router()

const { merge, readTemplate, getCryptoInfo, allowedCrypto } = require('../utils')

router.get('/', function(req, res) {
    res.send(readTemplate('index.html'))
})

router.get('/crypto', function(req, res, next) {
    res.json({'status': 'ok', 'data': allowedCrypto})
})

router.post('/crypto', async function(req, res, next) {
    let options = {
        'image': false,
        'detail': false
    }
    let coins = req.body['cryptos'] || []
    merge(options, req.body['options'])
    
    try {
        let result = []
        for(let coin of coins) {
            result.push(await getCryptoInfo(coin, options))
        }
        res.json({ 'status': 'ok', 'data': result })
    } catch(err) {
        next(err)
    }

})

module.exports = router