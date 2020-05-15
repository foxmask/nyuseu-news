module.exports = {
  publicPath: process.env.NODE_ENV !== 'production'
    ? '/'
    : 'http://0.0.0.0:8003' + process.env.NYUSEU_BASE_URL,
  outputDir: '../public',
  indexPath: '../public/index.html',
  filenameHashing: false,
  devServer: {
    proxy: {
        '/api/nyuseu': {
            target: 'http://0.0.0.0:8002'
        }
    }
  }
}
