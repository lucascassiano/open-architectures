var redbird = require('redbird');

const proxy = redbird({
    port: 80,
    resolvers: [
        // uses the same priority as default resolver, so will be called after default resolver
        // function (host, url, req) {
        //     // if (/\.example\.com/.test(host)) {
        //     //     return 'http://127.0.0.1:9999'
        //     // }
        //     console.log("req", req);
        //     console.log("host", host)
        // },
        // function (host, url, req) {
        //     console.log('--------------')
        //     console.log(url, host);
        //     if (/\.streamlit/.test(host)) {
        //         console.log("-----session----")
        //         console.log(req);
        //         console.log("///----session----///")
        //         return 'http://127.0.0.1:5000'
        //     }
        // }
    ]
});
proxy.register('localhost', 'http://localhost:5000');

proxy.register('localhost/streamlit/stream', 'http://localhost:8501/stream');
// {
//     onRequest: (req, res, target) => {
//         console.log(req);
//         // console.log("cassiano");
//         // return res;
//         // called before forwarding is occurred, you can modify req.headers for example
//         // return undefined to forward to default target
//     }
// }
// );

console.log("hello proxy");

// redbird.register('localhost/streamlit', 'http://localhost:8501/streamlit');
// redbird.register('localhost/static', 'http://localhost:8501/streamlit/static');
// redbird.register('localhost/streamlit/static', 'http://localhost:8501/streamlit/vendor');

// proxy.register("optimalbits.com", "localhost:5000");