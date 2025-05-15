const express = require('express');
const app = express();
const PORT = 3000;
const multer = require('multer')


// Middleware
app.use(express.static('./public')); // Serves static files

const upload = multer({ // file form handling
        storage: multer.memoryStorage(),
        fileFilter: (req, file, cb) => { // filters only PDF uploads
            if (file.mimetype === 'application/pdf') {
              cb(null, true);
            } else {
              cb(new Error('Only PDFs allowed'), false);
            }
          },
        limits: { fileSize: 10 * 1024 * 1024 } // max 10MB
    });


// Router Handlers
app.post('/submit', upload.single('pdfFile'), (req, res) => { // form submit right here fr    
    console.log("Submit Pressed")
    
});

app.listen(PORT, () => { // runs it right here fr
    console.log("Running Server")
});