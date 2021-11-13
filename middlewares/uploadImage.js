const multer = require("multer")

const __basedir = __dirname.substr(0, __dirname.lastIndexOf('/'))

var imageFilter = (req, file, cb) => {
    cb(null, true)
}

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, __basedir + '/Malarial/images/')
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + '-file-' + Math.round(Math.random() * 1E9)
        cb(null, uniqueSuffix + '-' + file.originalname.replace(/ /g, ''))
    }
})

var uploadFile = multer({ storage: storage, fileFilter: imageFilter, limits: 1024 * 1024 * 20 });

module.exports = uploadFile;