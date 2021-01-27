const BundleTracker = require("webpack-bundle-tracker");
const path = require('path')

const pages = {
    'vue_app_test': {
        entry: './src/test.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_question_history': {
        entry: './src/questionhistory.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_test_history': {
        entry: './src/testhistory.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_course_dashboard': {
        entry: './src/coursedashboard.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_course_cp': {
        entry: './src/coursecp.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_create_question': {
        entry: './src/createquestion.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_program_exercise': {
        entry: './src/programexercise.js',
        chunks: ['chunk-vendors']
    },
    'vue_app_course_setup': {
        entry: './src/coursesetup.js',
        chunks: ['chunk-vendors']
    },

    /*'vue_app_02': {
        entry: './src/newhampshir.js',
        chunks: ['chunk-vendors']
    },*/
}

module.exports = {
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? ''
        : 'http://localhost:8080/',
    outputDir: '../django_vue_mpa/static/vue/',

    chainWebpack: config => {

        config.optimization
            .splitChunks({
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-vendors",
                        chunks: "all",
                        priority: 1
                    },
                },
            });

        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../vue_frontend/webpack-stats.json'}]);

        config.resolve.alias
            .set('__STATIC__', 'static')
            .set(
                'vue$',
                // If using the runtime only build
                path.resolve(__dirname, 'node_modules/vue/dist/vue.js')
                // Or if using full build of Vue (runtime + compiler)
                // path.resolve(__dirname, 'node_modules/vue/dist/vue.esm.js')
              )

        config.devServer
            .public('http://localhost:8080')
            .host('localhost')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})

    }
};