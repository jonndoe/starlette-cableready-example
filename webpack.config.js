const path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const exclusions = /node_modules/;

module.exports = [
  {
    entry: {
      app: "./assets/app.js",
    },
    output: {
      path: path.resolve(__dirname, "static"), // Should be in STATICFILES_DIRS
      publicPath: "/static/",                  // Should match Django STATIC_URL
      filename: "[name].js",                   // No filename hashing, Django takes care of this
      chunkFilename: "[id]-[chunkhash].js",    // DO have Webpack hash chunk filename
    },
    devServer: {
      port: 8081,
      writeToDisk: true,             // Write files to disk in dev mode, so Django can serve the assets
    },
    module: {
      rules: [
        {
          test: /.*/,
          include: path.resolve(__dirname, "assets/img"),
          exclude: exclusions,
          options: {
            context: path.resolve(__dirname, "assets/"),
            name: "[path][name].[ext]",
          },
          loader: "file-loader",
        },
        {
          test: /\.css$/,
          exclude: exclusions,
          use: [
            MiniCssExtractPlugin.loader,
            { loader: "css-loader" },
          ],
        },
      ],
    },
    plugins: [
      new CleanWebpackPlugin({ cleanStaleWebpackAssets: false }),
      new MiniCssExtractPlugin(),
    ],
  },
];
