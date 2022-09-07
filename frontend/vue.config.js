const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  // webpack-dev-server 相关配置
  devServer: {
    proxy: {
        '^/api': {
            target: process.env.VUE_APP_URL,//接口的前缀
            ws:true,//代理websocked
            changeOrigin:true,//虚拟的站点需要更管origin
            pathRewrite:{
                //'^/api':''//重写路径
            }
        }
    }
}
});
