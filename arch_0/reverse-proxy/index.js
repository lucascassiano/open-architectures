var redbird = require('redbird');

const proxy = redbird({
    port: 80,
});

DOCKER = process.env.DOCKER
if (DOCKER) {
    console.log("running as Docker Container");
    // var docker = require('redbird').docker;
    // docker(redbird).register('localhost', 'http://server:5000');
    // docker(redbird).register("localhost/streamlit/stream", 'http://streamlit-app:8501/stream');
    // docker(redbird).register("preview.api.com", 'company/api:v[3-9].*');
    proxy.register('localhost', 'http://server:5000');
    proxy.register('localhost/streamlit/stream', 'http://streamlit-app:8501/stream');
}
else {
    proxy.register('localhost', 'http://localhost:5000');
    proxy.register('localhost/streamlit/stream', 'http://localhost:8501/stream');
}

