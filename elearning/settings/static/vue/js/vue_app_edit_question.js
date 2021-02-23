(function(t){function e(e){for(var n,o,r=e[0],c=e[1],u=e[2],d=0,p=[];d<r.length;d++)o=r[d],Object.prototype.hasOwnProperty.call(s,o)&&s[o]&&p.push(s[o][0]),s[o]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(t[n]=c[n]);l&&l(e);while(p.length)p.shift()();return i.push.apply(i,u||[]),a()}function a(){for(var t,e=0;e<i.length;e++){for(var a=i[e],n=!0,r=1;r<a.length;r++){var c=a[r];0!==s[c]&&(n=!1)}n&&(i.splice(e--,1),t=o(o.s=a[0]))}return t}var n={},s={vue_app_edit_question:0},i=[];function o(e){if(n[e])return n[e].exports;var a=n[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=t,o.c=n,o.d=function(t,e,a){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},o.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(o.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)o.d(a,n,function(e){return t[e]}.bind(null,n));return a},o.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],c=r.push.bind(r);r.push=e,r=r.slice();for(var u=0;u<r.length;u++)e(r[u]);var l=c;i.push([6,"chunk-vendors"]),a()})({"027f":function(t,e,a){},2988:function(t,e,a){"use strict";a("f49f")},"316a":function(t,e,a){"use strict";a("027f")},3720:function(t,e,a){},"3a4a":function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"grid question-editor-grid"},[a("div",{staticClass:"grid-col"},[a("div",[a("h3",[t._v("Testo della domanda")]),a("vue-editor",{staticClass:"big-editor",attrs:{id:"questionText",editorToolbar:t.customToolbar},model:{value:t.questionTextData,callback:function(e){t.questionTextData=e},expression:"questionTextData"}})],1),t.categories.length>0?a("div",[a("h3",[t._v("Categoria")]),a("select",{directives:[{name:"model",rawName:"v-model",value:t.categoryData,expression:"categoryData"}],on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,(function(t){return t.selected})).map((function(t){var e="_value"in t?t._value:t.value;return e}));t.categoryData=e.target.multiple?a:a[0]}}},[a("option",{attrs:{disabled:"",value:""}},[t._v("Scegli la categoria")]),t._l(t.categories,(function(e,n){return a("option",{key:n,domProps:{value:Object.keys(e)[0]}},[t._v(" "+t._s(e[Object.keys(e)[0]])+" ")])}))],2)]):t._e(),a("div",[a("h3",[t._v("Risposte")]),t._l(t.answersData,(function(e,n){return a("div",{key:n,staticClass:"grid two-to-one-col-fr rem-1-gap",staticStyle:{"margin-bottom":"0.5rem"}},[a("div",[a("vue-editor",{staticClass:"answer-editor",attrs:{id:"answer_"+n,editorToolbar:t.customToolbar},model:{value:t.answersData[n],callback:function(e){t.$set(t.answersData,n,e)},expression:"answersData[index]"}})],1),a("div",{staticStyle:{"align-self":"center"}},[a("b-button",{staticStyle:{"align-self":"center"},attrs:{disabled:t.answersData.length<=2,variant:"danger"},on:{click:function(e){t.correctAnswerIndexData+1==n&&(t.correctAnswerIndexData=0),t.answersData.splice(n,1)}}},[t._v("Rimuovi")]),a("div",{staticClass:"radio-option"},[a("b-form-radio",{attrs:{name:String(n+1),value:n+1},model:{value:t.correctAnswerIndexData,callback:function(e){t.correctAnswerIndexData=e},expression:"correctAnswerIndexData"}},[t._v("Risposta corretta")])],1)],1)])})),a("b-button",{staticClass:"w-100",attrs:{variant:"outline-primary"},on:{click:function(e){return t.answersData.push("")}}},[a("b-icon",{staticClass:"inline-icon",staticStyle:{"margin-bottom":"2px"},attrs:{icon:"plus-circle"}}),t._v(" Aggiungi risposta")],1)],2),a("div",[a("h3",[t._v("Soluzione")]),a("vue-editor",{staticClass:"big-editor",attrs:{id:"solutionText",editorToolbar:t.customToolbar},model:{value:t.solutionData,callback:function(e){t.solutionData=e},expression:"solutionData"}})],1)]),a("div",{staticClass:"grid-col preview-col"},[a("div",{staticClass:"preview"},[a("h3",[t._v("Anteprima")]),a("QuestionPreview",{attrs:{text:t.questionTextWithoutParagraphTag,answers:t.answerTextsWithoutParagraphTag,correctAnswerIndex:t.correctAnswerIndexData,solution:t.solutionData}}),a("b-button",{staticClass:"w-100 mt-4",attrs:{variant:"outline-success",disabled:t.invalidForm},on:{click:function(e){return t.$emit("save",t.serializedQuestionData)}}},[a("font-awesome-icon",{staticClass:"mr-1",attrs:{icon:"check-circle"}}),t._v(" Salva domanda")],1)],1)])])},s=[],i=(a("d81d"),a("45fc"),a("a9e3"),a("5873")),o=a("ce79"),r=a("ecee"),c=a("c074");r["c"].add(c["c"]);var u={name:"QuestionEditor",components:{VueEditor:i["a"],QuestionPreview:o["a"]},props:{courseId:Number,questionId:{type:Number,default:-1},questionText:{type:String,default:""},answers:{type:Array,default:function(){return["",""]}},correctAnswerIndex:{type:Number,default:0},solution:{type:String,default:""},categories:{type:[Array,Number],default:function(){return[]}},category:{type:[String,Number],default:""}},mounted:function(){this.questionTextData=this.questionText,this.answersData=this.answers,this.correctAnswerIndexData=this.correctAnswerIndex,this.solutionData=this.solution,this.categoryData=String(this.category)},watch:{},data:function(){return{questionTextData:"",solutionData:"",answersData:[],previewElements:[],categoryData:"",correctAnswerIndexData:-1,customToolbar:[["bold","italic","underline"],[{list:"ordered"},{list:"bullet"}],["image"]]}},methods:{cleanup:function(){this.questionTextData=this.solutionData=this.categoryData="",this.answersData=["",""],this.correctAnswerIndexData=0}},computed:{questionTextWithoutParagraphTag:function(){return this.questionTextData.replaceAll(/<[/]?p>/gi,"")},answerTextsWithoutParagraphTag:function(){return this.answersData.map((function(t){return t.replaceAll(/<[/]?p>/gi,"")}))},solutionTextWithoutParagraphTag:function(){return this.solutionData.replaceAll(/<[/]?p>/gi,"")},serializedQuestionData:function(){var t={text:this.questionTextWithoutParagraphTag,solution_text:this.solutionTextWithoutParagraphTag,category:this.categoryData,answers:this.answerTextsWithoutParagraphTag,correct_answer_index:this.correctAnswerIndexData,course:this.courseId};return-1!=this.questionId&&(t.questionId=this.questionId),t},invalidForm:function(){return!this.questionTextData.length||this.answersData.some((function(t){return!t.length}))||this.categories.length&&!this.categoryData.length}}},l=u,d=(a("f859"),a("2877")),p=Object(d["a"])(l,n,s,!1,null,null,null);e["a"]=p.exports},6:function(t,e,a){t.exports=a("e145")},ca7b:function(t,e,a){"use strict";a("3720")},cb5a:function(t,e,a){},ce79:function(t,e,a){"use strict";var n=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{class:{"question-preview-box":t.styled}},[t._m(0),a("vue-mathjax",{attrs:{id:"question-preview-"+t.questionId,formula:t.text,safe:!1,options:t.mathjaxOptions}}),t._l(t.answers,(function(e,n){return a("p",{key:n,staticClass:"answer-paragraph answer-paragraph-full"},[a("strong",[t._v(t._s(parseInt(n+1))+".")]),t._v(" "),a("vue-mathjax",{attrs:{formula:e,safe:!1,options:t.mathjaxOptions}}),n+1==t.correctAnswerIndex?a("span",{staticClass:"comment"},[a("em",{staticClass:"text-muted"},[t._v("(Risposta corretta)")])]):t._e()],1)})),t._m(1),a("vue-mathjax",{attrs:{formula:t.solution,safe:!1,options:t.mathjaxOptions}})],2)},s=[function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("p",[a("strong",[t._v("Domanda")])])},function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("p",[a("strong",[t._v("Soluzione")])])}],i=(a("a9e3"),a("7b93")),o={name:"QuestionPreview",components:{"vue-mathjax":i["VueMathjax"]},props:{text:String,solution:String,answers:Array,correctAnswerIndex:Number,questionId:[String,Number],styled:{type:Boolean,default:!0}},mounted:function(){},data:function(){return{mathjaxOptions:{tex2jax:{inlineMath:[["$","$"],["\\(","\\)"]],displayMath:[["$$","$$"],["[","]"]],processEscapes:!0,processEnvironments:!0}}}},methods:{},computed:{}},r=o,c=(a("316a"),a("2877")),u=Object(c["a"])(r,n,s,!1,null,"1e27a754",null);e["a"]=u.exports},e145:function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var n=a("ba4c"),s=a.n(n),i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[t.loading?a("b-spinner",{staticStyle:{position:"fixed",top:"50%",left:"50%",color:"black"},attrs:{label:"Loading..."}}):t._e(),a("div",[a("p",{staticClass:"mt-4"},[a("span",{staticClass:"mr-2"},[a("font-awesome-icon",{staticClass:"mr-1",attrs:{icon:"search"}}),t._v(" Filtra per:")],1),this.categories.length?a("span",[a("select",{directives:[{name:"model",rawName:"v-model",value:t.filterByCategory,expression:"filterByCategory"}],on:{change:function(e){var a=Array.prototype.filter.call(e.target.options,(function(t){return t.selected})).map((function(t){var e="_value"in t?t._value:t.value;return e}));t.filterByCategory=e.target.multiple?a:a[0]}}},[a("option",{attrs:{disabled:"",value:""}},[t._v("Categoria")]),t._l(t.categories,(function(e,n){return a("option",{key:n,domProps:{value:Object.keys(e)[0]}},[t._v(" "+t._s(e[Object.keys(e)[0]])+" ")])}))],2)]):t._e()])]),a("div",{directives:[{name:"infinite-scroll",rawName:"v-infinite-scroll",value:t.loadMoreQuestions,expression:"loadMoreQuestions"}],staticClass:"mt-4 grid edit-question-grid rem-1-gap"},t._l(t.questionsData,(function(e){return a("div",{key:e.questionId,class:{"column-span-2":t.editingId==e.questionId,"successfully-edited":t.successfullyEditedId==e.questionId},attrs:{id:"q-"+e.questionId}},[t.editingId==e.questionId?a("QuestionEditor",{ref:"editor"+parseInt(e.questionId),refInFor:!0,staticClass:"distinct p-5 mb-5 mt-5",attrs:{"course-id":t.courseId,questionText:e.textSource,answers:e.answersSources,"correct-answer-index":e.correctAnswerIndex,questionId:e.questionId,categories:t.categories,category:e.category,solution:e.solutionSource},on:{save:t.saveQuestionToDatabase}}):a("CollapsableQuestionPreview",{attrs:{text:e.text,answers:e.answers,"correct-answer-index":e.correctAnswerIndex,questionId:e.questionId,solution:e.solution},on:{editQuestion:t.editQuestion}})],1)})),0)],1)},o=[],r=(a("4de4"),a("c740"),a("d81d"),a("a9e3"),a("2909")),c=a("5530"),u=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("div",{staticClass:"question-preview-box",class:{"preview-box":t.collapsed}},[a("div",{staticClass:"preview-text",class:{hidden:!t.collapsed}},[a("span",{domProps:{innerHTML:t._s(t.text)}}),t._l(t.answers,(function(e,n){return a("p",{key:n,staticClass:"mt-3 answer-paragraph answer-paragraph-preview"},[a("strong",[t._v(t._s(parseInt(n+1))+".")]),t._v(" "),a("span",{domProps:{innerHTML:t._s(e)}}),n+1==t.correctAnswerIndex?a("span",{staticClass:"comment"},[a("em",{staticClass:"text-muted"},[t._v("(Risposta corretta)")])]):t._e()])})),a("div",{staticClass:"preview-text-fade"})],2),a("QuestionPreview",{class:{hidden:t.collapsed},attrs:{text:t.text,solution:t.solution,answers:t.answers,correctAnswerIndex:t.correctAnswerIndex,questionId:t.questionId,styled:!1}}),a("div",{staticClass:"mt-4 pt-2",staticStyle:{"z-index":"2"}},[a("b-button",{staticClass:"mr-2",attrs:{variant:"outline-primary"},on:{click:function(e){t.collapsed=!t.collapsed}}},[a("font-awesome-icon",{staticClass:"mr-1",attrs:{icon:t.collapsed?"plus":"minus"}}),t._v(" "+t._s(t.collapsed?"Mostra di più":"Mostra di meno ")+" ")],1),a("b-button",{attrs:{variant:"outline-secondary"},on:{click:function(e){return t.$emit("editQuestion",t.questionId)}}},[a("font-awesome-icon",{staticClass:"mr-1",attrs:{icon:"edit"}}),t._v("Modifica ")],1)],1)],1)])},l=[],d=a("ce79"),p=a("ecee"),f=a("c074");p["c"].add(f["i"]),p["c"].add(f["h"]),p["c"].add(f["d"]);var h={name:"CollapsableQuestionPreview",components:{QuestionPreview:d["a"]},props:{text:String,solution:String,answers:Array,correctAnswerIndex:Number,questionId:[String,Number]},mounted:function(){},data:function(){return{collapsed:!0,mathjaxOptions:{tex2jax:{inlineMath:[["$","$"],["\\(","\\)"]],displayMath:[["$$","$$"],["[","]"]],processEscapes:!0,processEnvironments:!0}}}},methods:{},computed:{}},v=h,g=(a("2988"),a("2877")),m=Object(g["a"])(v,u,l,!1,null,"24eff1e0",null),x=m.exports,w=a("3a4a"),b=a("bc3a"),y=a.n(b),I=a("487a"),_=a.n(I);p["c"].add(f["k"]);var q={name:"EditQuestion",components:{CollapsableQuestionPreview:x,QuestionEditor:w["a"]},directives:{infiniteScroll:_.a},watch:{filterByCategory:function(){this.loadMoreQuestions(!0)}},props:{questions:Array,userId:Number,courseId:Number,categories:{type:Array,default:function(){return[]}},editQuestionApiUrl:String,openEditor:{type:Number,default:null}},mounted:function(){y.a.defaults.xsrfCookieName="csrftoken",y.a.defaults.xsrfHeaderName="X-CSRFTOKEN",this.questionsData=this.questions,null!=this.openEditor&&this.openInitialEditor()},data:function(){return{questionsData:[],loading:!1,editingId:null,successfullyEditedId:null,scrollToConfig:{easing:"linear",cancelable:!0,offset:-250},filterByCategory:""}},methods:{editQuestion:function(t){this.editingId=t,console.log(this.$refs)},saveQuestionToDatabase:function(t){var e=this;console.log(t),this.loading=!0,y.a.put(this.editQuestionApiUrl,t).then((function(t){console.log(t);var a=t.data;200==t.status&&(e.questionsData[e.questionsData.findIndex((function(t){return t.questionId===e.editingId}))]=a,e.showConfirmationAndCloseEditor()),e.loading=!1})).catch((function(t){console.log(t)}))},showConfirmationAndCloseEditor:function(){var t=this,e=this.$refs["editor"+this.editingId][0];e.cleanup(),this.$scrollTo("#q-"+this.editingId,0,this.scrollToConfig),this.successfullyEditedId=this.editingId,setTimeout((function(){t.successfullyEditedId=null}),3e3),this.editingId=null},openInitialEditor:function(){var t=this;-1==this.questionsData.findIndex((function(e){return e.questionId==t.openEditor}))&&y.a.get("http://127.0.0.1:8000/get_questions/"+this.courseId+"/1/"+(this.openEditor-1)+"/").then((function(e){t.loading=!1,console.log(e.data),t.questionsData.unshift(Object(c["a"])(Object(c["a"])({},e.data[0]),{},{extra:!0}))})).catch((function(t){console.log(t)})),setTimeout((function(){t.editQuestion(t.openEditor)}),1e3)},loadMoreQuestions:function(){var t=this,e=arguments.length>0&&void 0!==arguments[0]&&arguments[0],a=arguments.length>1&&void 0!==arguments[1]?arguments[1]:5;e&&(this.questionsData=[]),this.loading=!0,y.a.get("http://127.0.0.1:8000/get_questions/"+this.courseId+"/"+a+"/"+this.maxQuestionId+"/"+(this.filterByCategory.length?this.filterByCategory+"/":"")).then((function(e){var a;t.loading=!1,console.log(e.data),(a=t.questionsData).push.apply(a,Object(r["a"])(e.data))})).catch((function(t){console.log(t)}))}},computed:{maxQuestionId:function(){return this.questionsData.length?Math.max.apply(Math,Object(r["a"])(this.questionsData.filter((function(t){return!t.extra})).map((function(t){return parseInt(t.questionId)})))):0}}},D=q,C=(a("ca7b"),Object(g["a"])(D,i,o,!1,null,null,null)),T=C.exports,A=a("5f5b"),j=a("b1e0"),S=a("ad3d"),E=a("f13c");s.a.use(A["a"]),s.a.use(j["a"]),s.a.use(E),s.a.component("font-awesome-icon",S["a"]),s.a.config.productionTip=!1,new s.a({el:"#app",components:{"edit-question":T,"vue-scrollto":E}})},f49f:function(t,e,a){},f859:function(t,e,a){"use strict";a("cb5a")}});