const path = require("path");
module.exports = {
  chainWebpack: (config) => {
    config.resolve.alias.set(
      "vue$",
      // If using the runtime only build
      path.resolve(__dirname, "node_modules/vue/dist/vue.runtime.esm.js")
      // Or if using full build of Vue (runtime + compiler)
      // path.resolve(__dirname, 'node_modules/vue/dist/vue.esm.js')
    );
    config.plugin("html").tap((args) => {
      args[0].title = "NMBS";
      return args;
    });
  },
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
    },
  },
  productionSourceMap: false, // this makes the build a little faster for me
  parallel: true, // same ^
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.(csv|tsv)$/i,
          use: ["csv-loader"],
        },
      ],
    },
  },
};
