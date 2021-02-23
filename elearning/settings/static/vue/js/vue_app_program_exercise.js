(function(t){function e(e){for(var o,a,i=e[0],c=e[1],u=e[2],p=0,f=[];p<i.length;p++)a=i[p],Object.prototype.hasOwnProperty.call(n,a)&&n[a]&&f.push(n[a][0]),n[a]=0;for(o in c)Object.prototype.hasOwnProperty.call(c,o)&&(t[o]=c[o]);l&&l(e);while(f.length)f.shift()();return s.push.apply(s,u||[]),r()}function r(){for(var t,e=0;e<s.length;e++){for(var r=s[e],o=!0,i=1;i<r.length;i++){var c=r[i];0!==n[c]&&(o=!1)}o&&(s.splice(e--,1),t=a(a.s=r[0]))}return t}var o={},n={vue_app_program_exercise:0},s=[];function a(e){if(o[e])return o[e].exports;var r=o[e]={i:e,l:!1,exports:{}};return t[e].call(r.exports,r,r.exports,a),r.l=!0,r.exports}a.m=t,a.c=o,a.d=function(t,e,r){a.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:r})},a.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},a.t=function(t,e){if(1&e&&(t=a(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(a.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)a.d(r,o,function(e){return t[e]}.bind(null,o));return r},a.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return a.d(e,"a",e),e},a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},a.p="";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=e,i=i.slice();for(var u=0;u<i.length;u++)e(i[u]);var l=c;s.push([7,"chunk-vendors"]),r()})({"5dc7":function(t,e,r){},7:function(t,e,r){t.exports=r("fc94")},e7d0:function(t,e,r){"use strict";r("5dc7")},fc94:function(t,e,r){"use strict";r.r(e);r("e260"),r("e6cf"),r("cca6"),r("a79d");var o=r("ba4c"),n=r.n(o),s=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"row"},[r("div",{staticClass:"col-8"},[t.loading?r("b-spinner",{staticStyle:{position:"fixed",top:"50%",left:"50%",color:"white"},attrs:{label:"Loading..."}}):t._e(),r("h2",[t._v("Esercizio")]),r("p",[t._v(t._s(t.text))]),r("prism-editor",{staticClass:"my-editor h-350",attrs:{highlight:t.highlighter,"line-numbers":""},model:{value:t.userProgram,callback:function(e){t.userProgram=e},expression:"userProgram"}}),r("br"),r("b-button",{staticStyle:{"margin-bottom":"10px"},attrs:{id:"submit",disabled:0==t.userProgram.length,variant:"outline-primary"},on:{click:function(e){return t.submit()}}},[t._v("Invia")])],1),r("div",{staticClass:"col-4"},[r("h4",[t._v("Test case")]),r("p",{staticClass:"text-muted"},[t._v("Il programma potrebbe venire testato anche con altri input non presenti in questa lista.")]),r("ul",{staticClass:"testcase-list"},t._l(t.publicTestCases,(function(e,o){return r("li",{key:o,staticClass:"test-case"},[r("strong",[t._v("Input")]),r("pre",[t._v(t._s(e.input.replace("=","\n")))]),r("strong",[t._v("Output")]),r("pre",[t._v(t._s(e.output))])])})),0)]),r("b-modal",{attrs:{size:"xl",id:"outcome-modal"},scopedSlots:t._u([{key:"modal-header",fn:function(e){return[r("h1",[t._v("Risultati")])]}},{key:"default",fn:function(e){return[r("div",{staticClass:"container"},[r("div",{staticClass:"row"},[r("div",{staticClass:"col-10"},[r("p",[r("strong",[t._v("Test case superati:")]),t._v(" "),r("span",{staticClass:"score"},[t._v(t._s(t.outcomeObj.positiveCases))]),t._v(" / "+t._s(t.outcomeObj.totalCases)+" ")])]),r("div",{staticClass:"col-10"},[r("p",[r("strong",[t._v("Esito: ")]),t.outcomeObj.passing?r("span",{staticClass:"passed"},[r("strong",[t._v("superato")])]):r("span",{staticClass:"failed"},[r("strong",[t._v("non superato")])])])])])])]}},{key:"modal-footer",fn:function(e){e.ok,e.cancel;var o=e.hide;return[r("b-button",{attrs:{size:"md",variant:"dark"},on:{click:function(t){return o("ok")}}},[t._v(" Chiudi ")])]}}])})],1)},a=[],i=(r("a9e3"),r("e57a")),c=(r("cabf"),r("8c7a")),u=(r("cb55"),r("416b"),r("84bf"),r("bc3a")),l=r.n(u),p={name:"ProgramExercise",props:{text:String,publicTestCases:Array,exerciseId:Number},mounted:function(){l.a.defaults.xsrfCookieName="csrftoken",l.a.defaults.xsrfHeaderName="X-CSRFTOKEN"},components:{"prism-editor":i["a"]},data:function(){return{userProgram:"",loading:!1,outcomeObj:{},code:""}},methods:{submit:function(){var t=this,e=JSON.stringify(this.userProgram);console.log(e),this.loading=!0,l.a.post("http://127.0.0.1:8000/eval_progsol/"+this.exerciseId+"/",e).then((function(e){t.outcomeObj=e.data,t.$root.$emit("bv::show::modal","outcome-modal","#submit"),console.log(e),t.loading=!1})).catch((function(t){alert(t),console.log(t)}))},highlighter:function(t){return Object(c["highlight"])(t,c["languages"].js)}}},f=p,d=(r("e7d0"),r("2877")),b=Object(d["a"])(f,s,a,!1,null,"5ff2252a",null),m=b.exports,v=r("5f5b");n.a.use(v["a"]),n.a.config.productionTip=!1,new n.a({el:"#app",components:{"program-exercise":m}})}});