if(!self.define){let e,i={};const n=(n,l)=>(n=new URL(n+".js",l).href,i[n]||new Promise((i=>{if("document"in self){const e=document.createElement("script");e.src=n,e.onload=i,document.head.appendChild(e)}else e=n,importScripts(n),i()})).then((()=>{let e=i[n];if(!e)throw new Error(`Module ${n} didn’t register its module`);return e})));self.define=(l,s)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(i[r])return;let o={};const u=e=>n(e,r),t={module:{uri:r},exports:o,require:u};i[r]=Promise.all(l.map((e=>t[e]||u(e)))).then((e=>(s(...e),o)))}}define(["./workbox-6567b62a"],(function(e){"use strict";e.setCacheNameDetails({prefix:"stolpotvorenie.space"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.0bc5bd54.css",revision:null},{url:"/fonts/AngstVF.34fe4e2d.woff",revision:null},{url:"/fonts/ZTNeueRalewe-Bold.3214ad3b.otf",revision:null},{url:"/fonts/ZTNeueRalewe-Medium.4dc6a032.otf",revision:null},{url:"/fonts/ZTNeueRalewe-SemiBold.a5b30272.otf",revision:null},{url:"/img/instagram.771ccae8.svg",revision:null},{url:"/img/left_curtain.02302fa7.png",revision:null},{url:"/img/noise.75bd9227.png",revision:null},{url:"/img/right_curtain.1588ca01.png",revision:null},{url:"/img/telegram.d75b5309.svg",revision:null},{url:"/img/vk.a497bfdd.svg",revision:null},{url:"/index.html",revision:"8b55f882b54b69af5cbfd50015081cf1"},{url:"/js/app.09c1cd25.js",revision:null},{url:"/js/chunk-vendors.92cfa0bb.js",revision:null},{url:"/manifest.json",revision:"9cf942969dec1c1a4e0edc6481b25dff"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{})}));
//# sourceMappingURL=service-worker.js.map
