module.exports = {
  style: {
    postcssOptions: {
      plugins: [
        require('tailwindcss'),
        require('autoprefixer'),
      ],
    },
  },
  jest: {
    configure: {
      moduleNameMapper: {
        '^react-router-dom$': '<rootDir>/node_modules/react-router-dom/dist/index.js',
        '^react-router/dom$': '<rootDir>/node_modules/react-router/dist/development/dom-export.js',
        '^react-router$': '<rootDir>/node_modules/react-router/dist/development/index.js',
      },
    },
  },
};