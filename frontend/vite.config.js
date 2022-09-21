import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	// build: {
    //     target: ['edge89', 'chrome89', 'firefox89', 'safari15'],
    // },
    // optimizeDeps: {
    //     esbuildOptions: {
    //         target: ['edge89', 'chrome89', 'firefox89', 'safari15'],
    //     },
    // },
};

export default config;
