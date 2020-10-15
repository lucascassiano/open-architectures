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
    proxy.register('localhost/streamlit/static', 'http://streamlit-app:8501/static');
    proxy.register('localhost/streamlit/health*', 'http://streamlit-app:8501/healthz');
    proxy.register('localhost/streamlit/stream', 'http://streamlit-app:8501/stream');
    proxy.register('localhost/static', 'http://streamlit-app:8501/static');

    //vue.js
    proxy.register('localhost/app', 'http://vue-app:8080');
}
else {

    proxy.register('localhost', 'http://localhost:5000');

    proxy.register('localhost/streamlit/static', 'http://localhost:8501/static');
    proxy.register('localhost/streamlit/healthz', 'http://localhost:8501/healthz');
    proxy.register('localhost/streamlit/stream', 'http://localhost:8501/stream');

    //vue.js
    proxy.register('localhost/app', 'http://localhost:8080');
}

