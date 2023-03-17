const webpack = require('webpack');
resolve.fallback: {
    "http": require.resolve("stream-http"),
    "crypto": require.resolve("crypto-browserify")
};
module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.REACT_APP_NAME': JSON.stringify(env.REACT_APP_NAME),
    }),
  ],
};
config.node = {
  fs: 'empty',
}
