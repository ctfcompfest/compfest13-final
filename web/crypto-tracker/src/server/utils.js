const fs = require('fs')
const path = require('path')
const axios = require('axios')

const API_HOST = 'https://api.coingecko.com/api/v3'
const viewsDir = path.join(__dirname, 'views')

var errorMessage = {
    400: 'Bad Request',
    401: 'Unathorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    429: 'Too Many Request',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout'
}

var allowedCrypto = {
    'bitcoin': true,
    'ethereum': true,
    'monero': true,
    'dogecoin': true,
    'litecoin': true
}

var simpleCache = {}

function merge (dst, ...sources) {
    for (src of sources) {
        for (let key in src) {
            let s = src[key], d = dst[key]
            if (Object(s) == s && Object(d) === d) {
                dst[key] = merge(d, s)
                continue
            }
            dst[key] = src[key]
        }
    }
    return dst
}

function readTemplate(fname) {
    let fpath = path.join(viewsDir, fname)
    return fs.readFileSync(fpath).toString()
}

function parseData(data, opt) {
    let result = {}
    let attrs = ['id', 'symbol', 'name']
    if (opt['image'] == true) attrs.push('image')
    if (opt['detail'] == true) attrs.push('description')
    for (let attr of attrs) result[attr] = data[attr]
    result['price'] = data['market_data']['current_price']['idr']
    return result
}

async function getCryptoInfo(crypto, opt) {
    if (allowedCrypto[crypto] !== true) return
    
    if (simpleCache[crypto]) {
        let now = Date.now()
        if (now - simpleCache[crypto].timestamp < 10000) {
            return parseData(simpleCache[crypto].data, opt)        
        }
    }
    
    let result = {}
    await axios.get(API_HOST + `/coins/${crypto}`)
        .then(function (response) {
            let data = response.data
            simpleCache[crypto] = {
                'data': data,
                'timestamp': Date.now()
            }
            result = parseData(data, opt)
        })
        .catch(function (error) {
            throw new Error(error.response.data.error)
        })
    return result
}

module.exports = { allowedCrypto, errorMessage, readTemplate, merge, getCryptoInfo }