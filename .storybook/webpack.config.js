const path = require('path');

const staticPath = path.resolve(__dirname, '..', 'src', 'sentry', 'static', 'sentry');
const componentPath = path.resolve(staticPath, 'app', 'components');

const [appConfig, legacyCssConfig] = require('../webpack.config');

console.log(legacyCssConfig);
module.exports = {
  module: {
    rules: [
      {
        test: /\.less$/,
        include: staticPath,
        loader: 'css-loader!less-loader'
      },
      {
        test: /\.(woff|woff2|ttf|eot|svg|png|gif|ico|jpg)($|\?)/,
        loader: 'file-loader?name=' + '[name].[ext]'
      }
    ]
  },
  resolve: {
    alias: {
      'sentry-ui': componentPath
    }
  }
};
