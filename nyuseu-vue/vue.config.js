baseUrl = process.env.NYUSEU_BASE_URL || '/'
module.exports = {
    publicPath: process.env.NODE_ENV !== 'production'
      ? '/'
      : 'http://127.0.0.1:8001' + baseUrl,
    outputDir: '../nyuseu_server/static',
    indexPath: '../templates/index.html',
    filenameHashing: false,
    devServer: {
      proxy: {
          '/api/nyuseu/': {
              target: 'http://localhost:8001'
          }
      }
    }
  }
