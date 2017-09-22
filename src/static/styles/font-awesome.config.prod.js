const ExtractTextPlugin = require('extract-text-webpack-plugin');
const fontAwesomeConfig = require('./font-awesome.config');
const buildExtractStylesLoader = require('./font-awesome-helper');

fontAwesomeConfig.styleLoader = buildExtractStylesLoader(ExtractTextPlugin.extract(['css-loader', 'less-loader']));

module.exports = fontAwesomeConfig;
