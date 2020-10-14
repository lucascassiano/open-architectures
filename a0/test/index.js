var redbird = require('redbird')({port: 80});

// // OPTIONAL: Setup your proxy but disable the X-Forwarded-For header
// var proxy = require('redbird')({port: 80, xfwd: false});

// Route to any global ip
redbird.register('localhost', 'http://localhost:5000');
redbird.register('localhost/streamlit', 'http://localhost:8501/streamlit');
redbird.register('localhost/static', 'http://localhost:8501/streamlit/static');
// redbird.register('localhost/streamlit/static', 'http://localhost:8501/streamlit/vendor');

// proxy.register("optimalbits.com", "localhost:5000");