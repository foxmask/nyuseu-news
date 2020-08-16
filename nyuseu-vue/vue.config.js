baseUrl = process.env.NYUSEU_BASE_URL || '/'
module.exports = {
    publicPath: process.env.NODE_ENV !== 'production'
      ? '/'
      : 'http://0.0.0.0:8001' + baseUrl + process.env.NYUSEU_BASE_URL,
    outputDir: '../public',
    indexPath: '../public/index.html',
    filenameHashing: false,
    devServer: {
      proxy: {
          '/api/nyuseu': {
              target: 'http://localhost:8001'
          }
      }
    }
  }
  