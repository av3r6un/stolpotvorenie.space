if(!self.define){let e,l={};const i=(i,s)=>(i=new URL(i+".js",s).href,l[i]||new Promise((l=>{if("document"in self){const e=document.createElement("script");e.src=i,e.onload=l,document.head.appendChild(e)}else e=i,importScripts(i),l()})).then((()=>{let e=l[i];if(!e)throw new Error(`Module ${i} didn’t register its module`);return e})));self.define=(s,n)=>{const r=e||("document"in self?document.currentScript.src:"")||location.href;if(l[r])return;let u={};const o=e=>i(e,r),t={module:{uri:r},exports:u,require:o};l[r]=Promise.all(s.map((e=>t[e]||o(e)))).then((e=>(n(...e),u)))}}define(["./workbox-a91ef639"],(function(e){"use strict";e.setCacheNameDetails({prefix:"cp"}),self.addEventListener("message",(e=>{e.data&&"SKIP_WAITING"===e.data.type&&self.skipWaiting()})),e.precacheAndRoute([{url:"/css/app.c63d9900.css",revision:null},{url:"/fonts/AngstVF.34fe4e2d.woff",revision:null},{url:"/fonts/FontAwesome.cee4fe66.ttf",revision:null},{url:"/fonts/KreadonVF.1d6d8549.ttf",revision:null},{url:"/img/arrow-left.ebcac9fc.svg",revision:null},{url:"/img/arrow-right.e3759249.svg",revision:null},{url:"/img/attendence.7de30660.svg",revision:null},{url:"/img/delete.4705f32c.svg",revision:null},{url:"/img/login.4c221cc3.svg",revision:null},{url:"/img/logo-full.f8f0f6bd.svg",revision:null},{url:"/img/logo-short.4865540d.svg",revision:null},{url:"/img/logout.41f2e4ea.svg",revision:null},{url:"/img/moon.b2ad361a.svg",revision:null},{url:"/img/plus.12fb2e8d.svg",revision:null},{url:"/img/schedule.44d889a7.svg",revision:null},{url:"/img/sun.250e718c.svg",revision:null},{url:"/img/teachers.c49baedd.svg",revision:null},{url:"/img/user-edit.49f97f1b.svg",revision:null},{url:"/img/user-groups.430db289.svg",revision:null},{url:"/img/user-settings.a37076a5.svg",revision:null},{url:"/img/users.c8111be4.svg",revision:null},{url:"/index.html",revision:"f30a88202065a6dc55dc1ff5ace81917"},{url:"/js/app.a977592e.js",revision:null},{url:"/js/chunk-vendors.72e875bb.js",revision:null},{url:"/manifest.json",revision:"667e31c37690cef15e85d683f0b9ee01"},{url:"/robots.txt",revision:"b6216d61c03e6ce0c9aea6ca7808f7ca"}],{}),e.registerRoute(new e.NavigationRoute(e.createHandlerBoundToURL("index.html")))}));
//# sourceMappingURL=service-worker.js.map