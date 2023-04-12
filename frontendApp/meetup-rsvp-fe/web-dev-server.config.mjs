// import { hmrPlugin, presets } from '@open-wc/dev-server-hmr';
import { importMapsPlugin } from '@web/dev-server-import-maps';
/** Use Hot Module replacement by adding --hmr to the start command */
const hmr = process.argv.includes('--hmr');

export default /** @type {import('@web/dev-server').DevServerConfig} */ ({
  open: '/demo/',
  /** Use regular watch mode if HMR is not enabled. */
  watch: !hmr,
  /** Resolve bare module imports */
  nodeResolve: {
    exportConditions: ['browser', 'development'],
  },

  /** Compile JS for older browsers. Requires @web/dev-server-esbuild plugin */
  // esbuildTarget: 'auto'

  /** Set appIndex to enable SPA routing */
  // appIndex: 'demo/index.html',

  plugins: [
    /** Use Hot Module Replacement by uncommenting. Requires @open-wc/dev-server-hmr plugin */
    // hmr && hmrPlugin({ exclude: ['**/*/node_modules/**/*'], presets: [presets.litElement] }),
    importMapsPlugin({
      inject: {
        importMap: {
          // import the already built version, because not every subdependency is an esm module, thus this path can change sometimes
          imports: {
            'socket.io-client':
              './../node_modules/socket.io-client/dist/socket.io.esm.min.js',
          },
        },
      },
    }),
  ],

  // See documentation for all available options
});
